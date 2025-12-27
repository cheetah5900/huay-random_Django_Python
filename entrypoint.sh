#!/bin/bash
set -e

# Define database paths
DB_SOURCE="/app/db.sqlite3"
DB_TARGET="${DB_PATH}"

# Check if target database exists; if not, copy the initial one
if [ ! -f "$DB_TARGET" ]; then
    echo "Database not found in volume. Copying initial database from image..."
    # Ensure the directory exists
    mkdir -p $(dirname "$DB_TARGET")
    cp "$DB_SOURCE" "$DB_TARGET"
    echo "Database initialized."
else
    echo "Existing database found in volume. Using it."
fi

# Run the waitress server
exec python run_waitress.py
