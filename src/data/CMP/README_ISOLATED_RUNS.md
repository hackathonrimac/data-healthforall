# Isolated Runs by Specialty

The crawler now supports running one specialty at a time with sequential processing (1 worker).

## Quick Start

### 1. List all specialties
```bash
python3 crawler.py --list-specialties
```

This will show all available specialties with their indices:
```
  0. ADMINISTRACIÓN DE HOSPITALES (ID: 00003)
  1. ADMINISTRACIÓN DE SALUD (ID: 00062)
  2. ADMINISTRACIÓN EN SALUD (ID: 0000000219)
  ...
```

### 2. Run a single specialty
```bash
python3 -u crawler.py --specialty-index 0 --delay 1.0
```

The `-u` flag ensures unbuffered output so you see progress in real-time.

### 3. Using the helper script
```bash
./run_specialty.sh 0 1.0
```

This runs specialty index 0 with a 1.0 second delay.

## Features

- **Sequential processing**: 1 worker (default) - easier to monitor
- **Duplicate checking**: Enabled by default - skips existing doctors
- **Periodic saves**: Saves every 10 records and every 60 seconds
- **Isolated runs**: Process one specialty at a time
- **Real-time output**: Use `-u` flag for unbuffered output

## Example Workflow

```bash
# 1. List specialties to find what you want
python3 crawler.py --list-specialties | grep -i "CARDIOLOGÍA"

# 2. Find the index (e.g., 15)

# 3. Run that specialty
python3 -u crawler.py --specialty-index 15 --delay 1.0

# 4. Check progress
tail -f doctors_data.csv
```

## Command Options

```bash
python3 crawler.py \
  --specialty-index 0 \      # Process only this specialty
  --max-workers 1 \           # Sequential (default)
  --delay 1.0 \              # Delay between requests
  --save-interval 10 \        # Save every 10 records
  --save-time-interval 60     # Save every 60 seconds
```

## Benefits

1. **Easier monitoring**: See progress for one specialty at a time
2. **Better error handling**: If one specialty fails, others aren't affected
3. **Resume-friendly**: Can easily resume from any specialty
4. **Less server load**: Sequential processing is gentler on the server
5. **Clear progress**: Know exactly which specialty is being processed

## Processing Multiple Specialties

To process multiple specialties sequentially:

```bash
# Process specialties 0-4 one at a time
for i in {0..4}; do
  echo "Processing specialty $i..."
  python3 -u crawler.py --specialty-index $i --delay 1.0
  echo "Completed specialty $i"
  sleep 2
done
```

Or use the range option:
```bash
python3 -u crawler.py --start 0 --max 5 --delay 1.0
```

