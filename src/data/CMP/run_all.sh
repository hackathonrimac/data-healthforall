#!/bin/bash
# Run all specialties one by one, starting from the second specialty (index 1)

DELAY=${1:-1.0}
START_FROM=${2:-1}

echo "Starting crawl of all specialties..."
echo "Starting from specialty index: $START_FROM (skipping first $START_FROM specialty/ies)"
echo "Delay: $DELAY seconds"
echo ""
echo "Press Ctrl+C to stop (you can resume later)"
echo ""

python3 -u run_all_specialties.py \
    --delay "$DELAY" \
    --save-interval 10 \
    --start-from "$START_FROM"

