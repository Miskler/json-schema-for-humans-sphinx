#!/bin/bash

# Local CI test script - simulates GitHub Actions workflow locally

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting Local CI Test Suite${NC}"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}Error: Must be run from the project root directory${NC}"
    exit 1
fi

# Step 1: Install dependencies
echo -e "${YELLOW}📦 Installing dependencies...${NC}"
pip install -r requirements-dev.txt

# Step 2: Code quality checks
echo -e "${YELLOW}🔍 Running linting...${NC}"
make lint

echo -e "${YELLOW}🏷️  Running type checking...${NC}"
make type-check

# Step 3: Run tests
echo -e "${YELLOW}🧪 Running tests with coverage...${NC}"
make test

# Step 4: Build package
echo -e "${YELLOW}📦 Building package...${NC}"
make build

# Step 5: Build documentation
echo -e "${YELLOW}📚 Building documentation...${NC}"
make build-all-docs

# Step 6: Generate badges
echo -e "${YELLOW}🏆 Generating badges...${NC}"
make generate-badges

# Step 7: Check distribution
echo -e "${YELLOW}✅ Checking package distribution...${NC}"
twine check dist/*

# Success
echo -e "${GREEN}✅ All CI tests passed successfully!${NC}"
echo "=================================="
echo -e "${GREEN}🎉 Ready for deployment!${NC}"

# Show coverage summary
if [ -f "coverage.xml" ]; then
    echo -e "${BLUE}📊 Coverage Summary:${NC}"
    coverage report --show-missing
fi

# Show test results
if [ -f "test_results.txt" ]; then
    echo -e "${BLUE}🧪 Test Results:${NC}"
    tail -5 test_results.txt
fi

echo -e "${BLUE}📈 Generated files:${NC}"
ls -la coverage.svg 2>/dev/null || echo "No coverage badge generated"
ls -la dist/ 2>/dev/null || echo "No distribution files"
ls -la docs/_build/html/index.html 2>/dev/null || echo "No documentation built"
ls -la examples/docs/_build/html/index.html 2>/dev/null || echo "No examples built"
