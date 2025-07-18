#!/bin/bash

# Serve documentation script for JSONCrack Sphinx Extension

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}JSONCrack Sphinx Extension Documentation Server${NC}"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "docs/conf.py" ]; then
    echo -e "${RED}Error: Must be run from the project root directory${NC}"
    exit 1
fi

# Build main documentation
echo -e "${YELLOW}Building main documentation...${NC}"
cd docs
sphinx-build -b html . _build/html
cd ..

# Build examples documentation
echo -e "${YELLOW}Building examples documentation...${NC}"
cd examples/docs
sphinx-build -b html . _build/html
cd ../..

# Start server
echo -e "${GREEN}Starting development server...${NC}"
echo "Main documentation: http://localhost:8000"
echo "Examples documentation: http://localhost:8001"
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"

# Function to cleanup background processes
cleanup() {
    echo -e "\n${YELLOW}Stopping servers...${NC}"
    kill $PID1 $PID2 2>/dev/null || true
    echo -e "${GREEN}Servers stopped${NC}"
}

# Set trap to cleanup on exit
trap cleanup EXIT

# Start servers in background
cd docs/_build/html && python -m http.server 8000 > /dev/null 2>&1 &
PID1=$!

cd ../../examples/docs/_build/html && python -m http.server 8001 > /dev/null 2>&1 &
PID2=$!

# Wait for user input
echo -e "${GREEN}Servers started successfully!${NC}"
echo "Press Enter to stop..."
read

# Cleanup will be handled by trap
