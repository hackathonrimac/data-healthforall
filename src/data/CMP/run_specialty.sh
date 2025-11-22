#!/bin/bash
# Helper script to run crawler for a specific specialty

SPECIALTY_INDEX=$1
DELAY=${2:-1.0}

if [ -z "$SPECIALTY_INDEX" ]; then
    echo "Usage: ./run_specialty.sh <specialty_index> [delay]"
    echo "Example: ./run_specialty.sh 0 1.0"
    echo ""
    echo "To see all specialties, run:"
    echo "  python3 crawler.py --list-specialties"
    exit 1
fi

echo "Running crawler for specialty index: $SPECIALTY_INDEX"
echo "Delay: $DELAY seconds"
echo ""

python3 -u crawler.py \
    --specialty-index "$SPECIALTY_INDEX" \
    --max-workers 2 \
    --delay "$DELAY" \
    --save-interval 10

