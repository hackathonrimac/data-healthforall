#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LAMBDAS_DIR="$ROOT_DIR/lambdas"
SHARED_DIR="$ROOT_DIR/shared"
DIST_DIR="$ROOT_DIR/dist"
REQUIREMENTS_FILE="$ROOT_DIR/requirements.txt"

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

for lambda_dir in "$LAMBDAS_DIR"/*; do
  [ -d "$lambda_dir" ] || continue
  name="$(basename "$lambda_dir")"
  build_dir="$DIST_DIR/$name"
  mkdir -p "$build_dir"

  rsync -a --exclude '__pycache__' "$lambda_dir/" "$build_dir/" >/dev/null
  rsync -a --exclude '__pycache__' "$SHARED_DIR/" "$build_dir/shared/" >/dev/null

  if [ -s "$REQUIREMENTS_FILE" ]; then
    pip install -r "$REQUIREMENTS_FILE" --target "$build_dir" >/dev/null
  fi

  (cd "$build_dir" && zip -qr "../${name}.zip" .)
  rm -rf "$build_dir"
  echo "Packaged ${name} → dist/${name}.zip"
done
