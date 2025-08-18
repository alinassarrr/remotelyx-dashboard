#!/bin/bash

# Script to run database migrations for RemotelyX Dashboard
# Usage: ./run_migration.sh [migration_name] [up|down]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}RemotelyX Dashboard - Database Migration Runner${NC}"
echo "=================================================="

# Check if Python virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/pyvenv.cfg" ] || [ ! -d "venv/lib" ]; then
    echo -e "${YELLOW}Installing dependencies...${NC}"
    pip install -r requirements.txt
fi

# Set default migration
MIGRATION_NAME=${1:-"add_scraped_job_fields"}
DIRECTION=${2:-"up"}

# Check if migration file exists
MIGRATION_FILE="migrations/${MIGRATION_NAME}.py"

if [ ! -f "$MIGRATION_FILE" ]; then
    echo -e "${RED}❌ Migration file not found: $MIGRATION_FILE${NC}"
    echo "Available migrations:"
    ls -1 migrations/*.py 2>/dev/null | sed 's/migrations\//  - /' | sed 's/\.py$//' || echo "  (no migrations found)"
    exit 1
fi

echo -e "${BLUE}Running migration: ${MIGRATION_NAME} (${DIRECTION})${NC}"
echo ""

# Run the migration
if [ "$DIRECTION" = "down" ]; then
    python "$MIGRATION_FILE" down
else
    python "$MIGRATION_FILE"
fi

echo ""
echo -e "${GREEN}✅ Migration completed successfully!${NC}"

# Deactivate virtual environment
deactivate 