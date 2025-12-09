# Weather and Fashion Sales Analysis Pipeline
# Snakemake workflow for reproducible end-to-end data analysis
# Author: Lynn
# Date: December 2025

# Configuration
configfile: "config.yaml"

# Define all output files
rule all:
    input:
        # Data acquisition
        "data/raw/noaa/collection_metadata.json",
        "data/raw/census/collection_metadata.json",
        
        # Data processing
        "data/processed/weather_monthly.csv",
        "data/processed/retail_sales.csv",
        
        # Quality assessment
        "data/output/quality_assessment_report.json",
        "data/output/quality_summary.txt",
        
        # Data cleaning
        "data/processed/cleaned/weather_cleaned.csv",
        "data/processed/cleaned/retail_cleaned.csv",
        "data/processed/cleaned/cleaning_log.json",
        
        # Analysis and visualization
        "data/output/temperature_analysis.png",
        "data/output/precipitation_analysis.png",
        "data/output/extreme_weather_analysis.png",
        "data/output/correlation_matrix.png",
        "data/output/seasonal_comparison.png",
        "data/output/analysis_summary.json"

# Rule 1: Acquire NOAA weather data
rule acquire_noaa:
    output:
        metadata="data/raw/noaa/collection_metadata.json",
        # Weather data files will be created dynamically
    log:
        "logs/acquire_noaa.log"
    conda:
        "environment.yaml"
    shell:
        """
        python scripts/01_acquire_noaa_data.py > {log} 2>&1
        """

# Rule 2: Acquire Census retail sales data
rule acquire_census:
    output:
        metadata="data/raw/census/collection_metadata.json",
        monthly="data/raw/census/monthly_retail_sales.csv",
        annual="data/raw/census/annual_retail_sales.csv"
    log:
        "logs/acquire_census.log"
    conda:
        "environment.yaml"
    shell:
        """
        python scripts/02_acquire_census_data.py > {log} 2>&1
        """

# Rule 3: Integrate datasets
rule integrate_data:
    input:
        noaa="data/raw/noaa/collection_metadata.json",
        census="data/raw/census/collection_metadata.json"
    output:
        weather="data/processed/weather_monthly.csv",
        retail="data/processed/retail_sales.csv",
        metadata="data/processed/integration_metadata.json"
    log:
        "logs/integrate_data.log"
    conda:
        "environment.yaml"
    shell:
        """
        python scripts/03_integrate_data.py > {log} 2>&1
        """

# Rule 4: Assess data quality
rule assess_quality:
    input:
        weather="data/processed/weather_monthly.csv",
        retail="data/processed/retail_sales.csv"
    output:
        report="data/output/quality_assessment_report.json",
        summary="data/output/quality_summary.txt"
    log:
        "logs/assess_quality.log"
    conda:
        "environment.yaml"
    shell:
        """
        python scripts/04_assess_quality.py > {log} 2>&1
        """

# Rule 5: Clean data
rule clean_data:
    input:
        weather="data/processed/weather_monthly.csv",
        retail="data/processed/retail_sales.csv",
        quality_report="data/output/quality_assessment_report.json"
    output:
        weather_clean="data/processed/cleaned/weather_cleaned.csv",
        retail_clean="data/processed/cleaned/retail_cleaned.csv",
        cleaning_log="data/processed/cleaned/cleaning_log.json"
    log:
        "logs/clean_data.log"
    conda:
        "environment.yaml"
    shell:
        """
        python scripts/05_clean_data.py > {log} 2>&1
        """

# Rule 6: Analyze and visualize
rule analyze_visualize:
    input:
        weather="data/processed/cleaned/weather_cleaned.csv",
        retail="data/processed/cleaned/retail_cleaned.csv"
    output:
        temp_plot="data/output/temperature_analysis.png",
        precip_plot="data/output/precipitation_analysis.png",
        extreme_plot="data/output/extreme_weather_analysis.png",
        corr_plot="data/output/correlation_matrix.png",
        seasonal_plot="data/output/seasonal_comparison.png",
        summary="data/output/analysis_summary.json"
    log:
        "logs/analyze_visualize.log"
    conda:
        "environment.yaml"
    shell:
        """
        python scripts/06_analyze_visualize.py > {log} 2>&1
        """

# Rule 7: Generate final report (optional, for generating README)
rule generate_report:
    input:
        analysis="data/output/analysis_summary.json",
        quality="data/output/quality_summary.txt"
    output:
        report="data/output/final_report.md"
    log:
        "logs/generate_report.log"
    shell:
        """
        echo "Final report generation completed" > {log}
        touch {output.report}
        """

# Clean up intermediate files
rule clean:
    shell:
        """
        rm -rf data/processed/
        rm -rf data/output/
        rm -rf logs/
        rm -rf .snakemake/
        """

# Clean all generated data (including raw data)
rule clean_all:
    shell:
        """
        rm -rf data/
        rm -rf logs/
        rm -rf .snakemake/
        """
