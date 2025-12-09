#!/bin/bash
# Run All Script - Weather and Fashion Sales Analysis
# Executes complete end-to-end workflow
# Author: Lynn
# Date: December 2025

set -e  # Exit on error

echo "=========================================="
echo "Weather and Fashion Sales Analysis"
echo "Complete Workflow Execution"
echo "=========================================="
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ] && [ -z "$CONDA_DEFAULT_ENV" ]; then
    echo "WARNING: No virtual environment detected"
    echo "It's recommended to activate your environment first:"
    echo "  conda activate weatherfashion"
    echo "  OR"
    echo "  source venv/bin/activate"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create necessary directories
echo "Creating directory structure..."
mkdir -p data/raw/noaa data/raw/census data/processed data/processed/cleaned data/output logs
echo "✓ Directories created"
echo ""

# Check for API keys
echo "Checking API key configuration..."
if grep -q "YOUR_NOAA_API_TOKEN_HERE" scripts/01_acquire_noaa_data.py; then
    echo "ERROR: NOAA API token not configured!"
    echo "Please edit scripts/01_acquire_noaa_data.py and add your API token"
    exit 1
fi
echo "✓ API keys configured"
echo ""

# Step 1: Data Acquisition
echo "=========================================="
echo "Step 1: Acquiring Data"
echo "=========================================="
echo ""

echo "Acquiring NOAA weather data..."
python scripts/01_acquire_noaa_data.py
echo "✓ NOAA data acquired"
echo ""

echo "Acquiring Census retail sales data..."
python scripts/02_acquire_census_data.py
echo "✓ Census data acquired"
echo ""

# Step 2: Data Integration
echo "=========================================="
echo "Step 2: Integrating Datasets"
echo "=========================================="
echo ""

python scripts/03_integrate_data.py
echo "✓ Data integrated"
echo ""

# Step 3: Quality Assessment
echo "=========================================="
echo "Step 3: Assessing Data Quality"
echo "=========================================="
echo ""

python scripts/04_assess_quality.py
echo "✓ Quality assessment complete"
echo ""

# Step 4: Data Cleaning
echo "=========================================="
echo "Step 4: Cleaning Data"
echo "=========================================="
echo ""

python scripts/05_clean_data.py
echo "✓ Data cleaned"
echo ""

# Step 5: Analysis and Visualization
echo "=========================================="
echo "Step 5: Analysis and Visualization"
echo "=========================================="
echo ""

python scripts/06_analyze_visualize.py
echo "✓ Analysis complete"
echo ""

# Summary
echo "=========================================="
echo "Workflow Complete!"
echo "=========================================="
echo ""
echo "Output files are available in:"
echo "  - data/output/ (analysis results and visualizations)"
echo "  - data/processed/cleaned/ (cleaned datasets)"
echo ""
echo "Key outputs:"
echo "  - Quality Report: data/output/quality_assessment_report.json"
echo "  - Analysis Summary: data/output/analysis_summary.json"
echo "  - Visualizations: data/output/*.png"
echo ""
echo "Next steps:"
echo "  1. Review outputs in data/output/"
echo "  2. Upload data to Box for sharing"
echo "  3. Create GitHub release with 'final-project' tag"
echo "  4. Consider archiving on Zenodo for DOI"
echo ""
