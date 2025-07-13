#!/bin/bash
# Quick script to serve documentation locally

echo "Starting local documentation server..."
echo "Documentation will be available at: http://localhost:8000"
echo "Press Ctrl+C to stop"

cd examples/docs/_build/html
python -m http.server 8000
