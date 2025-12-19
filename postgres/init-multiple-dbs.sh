#!/bin/bash
set -e
set -u

DB_OWNER="wow_user"

function create_db_if_not_exists() {
  local db="$1"
  echo "Checking if database '$db' exists..."
  if psql -U "$POSTGRES_USER" -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='${db}'" | grep -q 1; then
    echo "Database '$db' already exists, skipping."
  else
    echo "Creating database '$db' with owner '$DB_OWNER'..."
    psql -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE \"$db\" OWNER \"$DB_OWNER\";"
    echo "Database '$db' created successfully with owner '$DB_OWNER'!"
  fi
}
if [ -n "${POSTGRES_MULTIPLE_DATABASES:-}" ]; then
  echo "Multiple database creation requested: $POSTGRES_MULTIPLE_DATABASES"
  for db in $(echo "$POSTGRES_MULTIPLE_DATABASES" | tr ',' ' '); do
    create_db_if_not_exists "$db"
  done
  echo "All requested databases handled."
fi