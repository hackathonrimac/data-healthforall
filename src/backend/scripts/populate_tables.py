#!/usr/bin/env python3
"""Populate DynamoDB tables with sample data for testing."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import boto3

# Add parent directory to path to import sample_data
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared import sample_data


def populate_table(dynamodb, table_name: str, items: list, key_name: str):
    """Populate a DynamoDB table with items."""
    try:
        table = dynamodb.Table(table_name)
        
        print(f"\n📋 Populating {table_name}...")
        
        for item in items:
            table.put_item(Item=item)
            print(f"  ✓ Added {item.get(key_name)}")
        
        print(f"✅ Successfully populated {table_name} with {len(items)} items")
        return True
    
    except Exception as e:
        print(f"❌ Error populating {table_name}: {str(e)}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Populate DynamoDB tables with sample data (using hackathon profile)"
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
        "--tables",
        nargs="+",
        choices=["doctors", "clinics", "especialidades", "subespecialidades", "seguros", "ubigeo", "all"],
        default=["all"],
        help="Tables to populate. Default: all"
    )
    
    args = parser.parse_args()
    
    # Always use hackathon profile
    profile = "hackathon"
    
    # Initialize boto3 session
    session = boto3.Session(profile_name=profile, region_name=args.region)
    dynamodb = session.resource("dynamodb")
    
    env = args.env
    tables_to_populate = args.tables
    
    if "all" in tables_to_populate:
        tables_to_populate = ["doctors", "clinics", "especialidades", "subespecialidades", "seguros", "ubigeo"]
    
    print(f"\n🚀 Starting data population for environment: {env}")
    print(f"📍 Region: {args.region}")
    print(f"👤 Profile: {profile}")
    print(f"📊 Tables: {', '.join(tables_to_populate)}")
    
    results = {}
    
    # Populate each table based on selection
    if "clinics" in tables_to_populate:
        results["clinics"] = populate_table(
            dynamodb,
            f"clinics-{env}",
            sample_data.CLINICS,
            "clinicaId"
        )
    
    if "doctors" in tables_to_populate:
        results["doctors"] = populate_table(
            dynamodb,
            f"doctors-{env}",
            sample_data.DOCTORS,
            "doctorId"
        )
    
    if "especialidades" in tables_to_populate:
        results["especialidades"] = populate_table(
            dynamodb,
            f"especialidades-{env}",
            sample_data.SPECIALTIES,
            "especialidadId"
        )
    
    if "subespecialidades" in tables_to_populate:
        results["subespecialidades"] = populate_table(
            dynamodb,
            f"subespecialidades-{env}",
            sample_data.SUBSPECIALTIES,
            "subEspecialidadId"
        )
    
    if "seguros" in tables_to_populate:
        results["seguros"] = populate_table(
            dynamodb,
            f"seguros-{env}",
            sample_data.INSURERS,
            "seguroId"
        )
    
    if "ubigeo" in tables_to_populate:
        results["ubigeo"] = populate_table(
            dynamodb,
            f"ubigeo-{env}",
            sample_data.UBIGEOS,
            "ubigeoId"
        )
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    successful = sum(1 for v in results.values() if v)
    failed = len(results) - successful
    
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All tables populated successfully!")
        return 0
    else:
        print("\n⚠️  Some tables failed to populate. Check errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

