#!/bin/bash
# Create beautiful reports index page

cat > _site/reports.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>JSONCrack Sphinx Extension - Reports</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 40px;
            background: #f8f9fa;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        h1 { 
            color: #2563eb;
            text-align: center;
            margin-bottom: 40px;
            font-size: 2.5em;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 40px;
        }
        .card { 
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 30px;
            background: white;
            transition: all 0.3s ease;
            border-left: 4px solid #2563eb;
        }
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }
        .card h2 { 
            margin-top: 0;
            color: #1f2937;
            font-size: 1.5em;
        }
        .card p {
            color: #6b7280;
            line-height: 1.6;
            margin-bottom: 20px;
        }
        .badge { 
            display: inline-block;
            padding: 8px 16px;
            border-radius: 6px;
            color: white;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        .badge:hover { 
            transform: translateY(-1px);
            text-decoration: none;
        }
        .badge.primary { background: #2563eb; }
        .badge.success { background: #10b981; }
        .badge.info { background: #06b6d4; }
        .meta {
            text-align: center;
            margin-top: 40px;
            padding-top: 30px;
            border-top: 1px solid #e5e7eb;
            color: #6b7280;
        }
        .badges {
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 20px;
        }
        .badges img {
            height: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 JSONCrack Sphinx Extension</h1>
        <p style="text-align: center; font-size: 1.1em; color: #6b7280;">
            Comprehensive reports and documentation for the JSONCrack Sphinx Extension
        </p>
        
        <div class="grid">
            <div class="card">
                <h2>📚 Main Documentation</h2>
                <p>Complete documentation including installation, configuration, and usage guides.</p>
                <a href="index.html" class="badge primary">View Documentation</a>
            </div>
            
            <div class="card">
                <h2>📊 Coverage Report</h2>
                <p>Detailed code coverage analysis from automated tests.</p>
                <a href="coverage/index.html" class="badge success">View Coverage</a>
            </div>
            
            <div class="card">
                <h2>🔬 Live Examples</h2>
                <p>Interactive examples and usage demonstrations.</p>
                <a href="examples/index.html" class="badge info">View Examples</a>
            </div>
        </div>
        
        <div class="meta">
            <p>Generated on: $(date)</p>
            <div class="badges">
                <img src="https://github.com/miskler/jsoncrack-for-sphinx/actions/workflows/test.yml/badge.svg" alt="Tests">
                <img src="coverage.svg" alt="Coverage">
                <img src="https://img.shields.io/pypi/v/jsoncrack-for-sphinx.svg" alt="PyPI">
                <img src="https://img.shields.io/pypi/pyversions/jsoncrack-for-sphinx.svg" alt="Python">
            </div>
        </div>
    </div>
</body>
</html>
EOF

echo "✅ Reports page created at _site/reports.html"
