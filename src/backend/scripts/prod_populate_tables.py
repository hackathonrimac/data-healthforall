#!/usr/bin/env python3
"""
Populate DynamoDB tables with production data from transformed JSONL files.

This script reads the transformed data files and populates DynamoDB tables
with the actual production data, avoiding duplicates.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

import boto3
from botocore.exceptions import ClientError


# Path to transformed data directory
TRANSFORMED_DATA_DIR = Path(__file__).parent.parent.parent / "data" / "final_tables" / "transformed"

# Table configurations: (file_name, table_name_suffix, partition_key)
TABLE_CONFIGS = [
    ("doctores.jsonl", "doctors", "doctorId"),
    ("clinicas.jsonl", "clinics", "clinicaId"),
    ("especialidades.jsonl", "especialidades", "especialidadId"),
    ("grupos.jsonl", "grupos", "grupoId"),
    ("ubigeo.jsonl", "ubigeo", "ubigeoId"),
]


def load_jsonl_file(file_path: Path) -> List[Dict[str, Any]]:
    """Load items from a JSONL file."""
    items = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def clear_table(dynamodb, table_name: str, partition_key: str) -> int:
    """Clear all items from a DynamoDB table."""
    table = dynamodb.Table(table_name)
    
    print(f"  🗑️  Clearing existing data from {table_name}...")
    
    # Scan and delete all items
    deleted_count = 0
    scan_kwargs = {
        'ProjectionExpression': partition_key
    }
    
    try:
        while True:
            response = table.scan(**scan_kwargs)
            items = response.get('Items', [])
            
            if not items:
                break
            
            # Batch delete items
            with table.batch_writer() as batch:
                for item in items:
                    batch.delete_item(Key={partition_key: item[partition_key]})
                    deleted_count += 1
            
            # Check if there are more items to scan
            if 'LastEvaluatedKey' not in response:
                break
            
            scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
        
        print(f"  ✓ Deleted {deleted_count} existing items")
        return deleted_count
    
    except ClientError as e:
        print(f"  ⚠️  Error clearing table: {e}")
        return deleted_count


def batch_write_items(dynamodb, table_name: str, items: List[Dict[str, Any]], partition_key: str) -> tuple[int, int, int]:
    """
    Write items to DynamoDB in batches, avoiding duplicates.
    Returns (successful_count, skipped_count, deduped_count).
    """
    table = dynamodb.Table(table_name)
    successful = 0
    skipped = 0
    
    # Deduplicate items by partition key (keep last occurrence)
    unique_items = {}
    for item in items:
        key = item.get(partition_key)
        unique_items[key] = item
    
    original_count = len(items)
    deduped_count = original_count - len(unique_items)
    
    if deduped_count > 0:
        print(f"  ⚠️  Found {deduped_count} duplicate(s) in source data - keeping last occurrence")
    
    # DynamoDB batch_writer automatically handles batching and retries
    with table.batch_writer() as batch:
        for item in unique_items.values():
            try:
                batch.put_item(Item=item)
                successful += 1
            except Exception as e:
                print(f"  ⚠️  Error writing item {item.get(partition_key)}: {e}")
                skipped += 1
    
    return successful, skipped, deduped_count


def populate_table(
    dynamodb,
    table_name: str,
    file_path: Path,
    partition_key: str,
    clear_first: bool = False
) -> bool:
    """Populate a single DynamoDB table from a JSONL file."""
    try:
        if not file_path.exists():
            print(f"  ⚠️  File not found: {file_path}")
            return False
        
        print(f"\n📋 Processing {table_name}...")
        
        # Clear table if requested
        if clear_first:
            clear_table(dynamodb, table_name, partition_key)
        
        # Load data from JSONL file
        items = load_jsonl_file(file_path)
        print(f"  📄 Loaded {len(items)} items from {file_path.name}")
        
        if not items:
            print(f"  ⚠️  No items to populate")
            return True
        
        # Batch write items
        print(f"  ⬆️  Writing items to DynamoDB...")
        successful, skipped, deduped = batch_write_items(dynamodb, table_name, items, partition_key)
        
        print(f"  ✅ Successfully wrote {successful} items")
        if deduped > 0:
            print(f"  📝 Deduplicated {deduped} duplicate(s) from source")
        if skipped > 0:
            print(f"  ⚠️  Skipped {skipped} items due to errors")
        
        return True
    
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ResourceNotFoundException':
            print(f"  ❌ Table {table_name} does not exist. Deploy infrastructure first.")
        else:
            print(f"  ❌ AWS Error: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error populating {table_name}: {e}")
        return False


def verify_table_exists(dynamodb_client, table_name: str) -> bool:
    """Verify that a table exists."""
    try:
        dynamodb_client.describe_table(TableName=table_name)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            return False
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Populate DynamoDB tables with production data from transformed JSONL files"
    )
    parser.add_argument(
        "--env",
        type=str,
        default="dev",
        choices=["dev", "prod"],
        help="Environment (dev or prod). Default: dev"
    )
    parser.add_argument(
        "--region",
        type=str,
        default="us-east-1",
        help="AWS region. Default: us-east-1"
    )
    parser.add_argument(
        "--profile",
        type=str,
        default="hackathon",
        help="AWS profile. Default: hackathon"
    )
    parser.add_argument(
        "--tables",
        nargs="+",
        choices=["doctors", "clinics", "especialidades", "grupos", "ubigeo", "all"],
        default=["all"],
        help="Tables to populate. Default: all"
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear existing data before populating (DESTRUCTIVE)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually writing to DynamoDB"
    )
    
    args = parser.parse_args()
    
    # Validate transformed data directory exists
    if not TRANSFORMED_DATA_DIR.exists():
        print(f"❌ Transformed data directory not found: {TRANSFORMED_DATA_DIR}")
        print("   Run transform_data.py first to generate transformed data files.")
        return 1
    
    # Initialize AWS session
    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    dynamodb = session.resource("dynamodb")
    dynamodb_client = session.client("dynamodb")
    
    env = args.env
    tables_to_populate = args.tables
    
    # Map table choices to configs
    table_map = {
        "doctors": ("doctores.jsonl", "doctors", "doctorId"),
        "clinics": ("clinicas.jsonl", "clinics", "clinicaId"),
        "especialidades": ("especialidades.jsonl", "especialidades", "especialidadId"),
        "grupos": ("grupos.jsonl", "grupos", "grupoId"),
        "ubigeo": ("ubigeo.jsonl", "ubigeo", "ubigeoId"),
    }
    
    if "all" in tables_to_populate:
        tables_to_populate = list(table_map.keys())
    
    print("=" * 80)
    print("🚀 PRODUCTION DATA POPULATION")
    print("=" * 80)
    print(f"📍 Environment: {env}")
    print(f"📍 Region: {args.region}")
    print(f"👤 Profile: {args.profile}")
    print(f"📊 Tables: {', '.join(tables_to_populate)}")
    print(f"🗑️  Clear first: {args.clear}")
    print(f"🔍 Dry run: {args.dry_run}")
    print(f"📁 Data source: {TRANSFORMED_DATA_DIR}")
    
    if args.clear:
        print("\n⚠️  WARNING: --clear flag is set. This will DELETE ALL EXISTING DATA!")
        if not args.dry_run:
            confirm = input("   Type 'yes' to continue: ")
            if confirm.lower() != 'yes':
                print("   Aborted.")
                return 0
    
    # Verify all tables exist first
    print("\n🔍 Verifying tables exist...")
    missing_tables = []
    for table_choice in tables_to_populate:
        file_name, table_suffix, partition_key = table_map[table_choice]
        table_name = f"{table_suffix}-{env}"
        
        if not verify_table_exists(dynamodb_client, table_name):
            missing_tables.append(table_name)
    
    if missing_tables:
        print(f"\n❌ The following tables do not exist:")
        for table in missing_tables:
            print(f"   - {table}")
        print("\n   Run deploy_backend.sh first to create the infrastructure.")
        return 1
    
    print("   ✅ All tables exist")
    
    if args.dry_run:
        print("\n🔍 DRY RUN - No data will be written")
        for table_choice in tables_to_populate:
            file_name, table_suffix, partition_key = table_map[table_choice]
            table_name = f"{table_suffix}-{env}"
            file_path = TRANSFORMED_DATA_DIR / file_name
            
            if file_path.exists():
                items = load_jsonl_file(file_path)
                print(f"   Would populate {table_name} with {len(items)} items from {file_name}")
            else:
                print(f"   ⚠️  File not found: {file_path}")
        
        print("\n✅ Dry run complete. Run without --dry-run to actually populate tables.")
        return 0
    
    # Populate tables
    results = {}
    
    for table_choice in tables_to_populate:
        file_name, table_suffix, partition_key = table_map[table_choice]
        table_name = f"{table_suffix}-{env}"
        file_path = TRANSFORMED_DATA_DIR / file_name
        
        results[table_name] = populate_table(
            dynamodb,
            table_name,
            file_path,
            partition_key,
            clear_first=args.clear
        )
    
    # Print summary
    print("\n" + "=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    successful = sum(1 for v in results.values() if v)
    failed = len(results) - successful
    
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All tables populated successfully!")
        print("\n💡 Next steps:")
        print("   - Verify data in AWS Console or using AWS CLI")
        print("   - Test your API endpoints")
        return 0
    else:
        print("\n⚠️  Some tables failed to populate. Check errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

