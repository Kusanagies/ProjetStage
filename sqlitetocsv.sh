#!/usr/bin/env bash

# Check for input file argument
if [ -z "$1" ]; then
  echo "Usage: $0 path_to_sqlite_file"
  exit 1
fi

SQLITE_FILE="$1"
CSV_DIR="csvfiles"

# Create output directory
mkdir -p "$CSV_DIR"

# Get all table names except metadata/system tables
TABLES=$(sqlite3 "$SQLITE_FILE" "SELECT tbl_name FROM sqlite_master WHERE type='table' AND tbl_name NOT LIKE 'metadata%' AND tbl_name NOT LIKE 'sqlite_%' AND tbl_name != 'dataset_profile';")

COUNTER=1

# Loop through tables and export each to numbered CSV
for T in $TABLES; do
  echo "Exporting table: $T → $COUNTER.csv"
  sqlite3 "$SQLITE_FILE" <<EOF
.headers on
.mode csv
.output $CSV_DIR/$COUNTER.csv
SELECT * FROM "$T";
EOF
  ((COUNTER++))
done

echo "✅ Export completed: $(($COUNTER - 1)) CSV files in $CSV_DIR/"

#chmod +x sqlitetocsv.sh
#./sqlitetocsv.sh benchmark.sqlite 
#Choisir le bon fichier sqlite à charger
