#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Format Export Utilities for MENA Bias Evaluation Pipeline
Export results to Excel, JSON, Parquet, CSV, and more
"""

import pandas as pd
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ExportManager:
    """
    Unified export manager for multiple formats
    
    Supported formats:
    - Excel (.xlsx) with multiple sheets and formatting
    - JSON (pretty and compact)
    - Parquet (efficient columnar storage)
    - CSV (standard and UTF-8)
    - Markdown (for documentation)
    - HTML (interactive tables)
    """
    
    def __init__(self, output_dir: str = "exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
        self.metadata = {
            'export_timestamp': datetime.now().isoformat(),
            'pipeline_version': '1.0.0'
        }
        
        logger.info(f"✅ Export Manager initialized: {self.output_dir}")
    
    def export_to_excel(
        self,
        data: Dict[str, pd.DataFrame],
        filename: str = "results.xlsx",
        include_charts: bool = True
    ) -> Path:
        """
        Export multiple DataFrames to Excel with formatting
        
        Args:
            data: Dictionary of sheet_name -> DataFrame
            filename: Output filename
            include_charts: Whether to include charts (future feature)
        
        Returns:
            Path to exported file
        """
        output_path = self.output_dir / filename
        
        # Create Excel writer with xlsxwriter engine
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            workbook = writer.book
            
            # Add formats
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BD',
                'border': 1
            })
            
            # Write each DataFrame to a sheet
            for sheet_name, df in data.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Get worksheet
                worksheet = writer.sheets[sheet_name]
                
                # Format header
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                
                # Auto-adjust column width
                for i, col in enumerate(df.columns):
                    max_length = max(
                        df[col].astype(str).map(len).max(),
                        len(str(col))
                    )
                    worksheet.set_column(i, i, min(max_length + 2, 50))
            
            # Add metadata sheet
            metadata_df = pd.DataFrame([
                {'Key': k, 'Value': v} for k, v in self.metadata.items()
            ])
            metadata_df.to_excel(writer, sheet_name='Metadata', index=False)
        
        logger.info(f"📊 Excel exported: {output_path}")
        return output_path
    
    def export_to_json(
        self,
        data: Dict[str, Any],
        filename: str = "results.json",
        pretty: bool = True
    ) -> Path:
        """
        Export data to JSON
        
        Args:
            data: Dictionary to export
            filename: Output filename
            pretty: Whether to use pretty printing
        
        Returns:
            Path to exported file
        """
        output_path = self.output_dir / filename
        
        # Add metadata
        export_data = {
            'metadata': self.metadata,
            'data': data
        }
        
        # Write JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            else:
                json.dump(export_data, f, ensure_ascii=False)
        
        logger.info(f"📄 JSON exported: {output_path}")
        return output_path
    
    def export_to_parquet(
        self,
        df: pd.DataFrame,
        filename: str = "results.parquet",
        compression: str = 'snappy'
    ) -> Path:
        """
        Export DataFrame to Parquet format
        
        Args:
            df: DataFrame to export
            filename: Output filename
            compression: Compression algorithm (snappy, gzip, brotli)
        
        Returns:
            Path to exported file
        """
        output_path = self.output_dir / filename
        
        df.to_parquet(
            output_path,
            compression=compression,
            index=False
        )
        
        logger.info(f"📦 Parquet exported: {output_path}")
        return output_path
    
    def export_to_csv(
        self,
        df: pd.DataFrame,
        filename: str = "results.csv",
        encoding: str = 'utf-8-sig'
    ) -> Path:
        """
        Export DataFrame to CSV
        
        Args:
            df: DataFrame to export
            filename: Output filename
            encoding: File encoding (utf-8-sig for Excel compatibility)
        
        Returns:
            Path to exported file
        """
        output_path = self.output_dir / filename
        
        df.to_csv(output_path, index=False, encoding=encoding)
        
        logger.info(f"📝 CSV exported: {output_path}")
        return output_path
    
    def export_to_markdown(
        self,
        data: Dict[str, pd.DataFrame],
        filename: str = "results.md"
    ) -> Path:
        """
        Export DataFrames to Markdown format
        
        Args:
            data: Dictionary of section_name -> DataFrame
            filename: Output filename
        
        Returns:
            Path to exported file
        """
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            # Write title
            f.write("# MENA Bias Evaluation Results\n\n")
            
            # Write metadata
            f.write("## Metadata\n\n")
            for key, value in self.metadata.items():
                f.write(f"- **{key}**: {value}\n")
            f.write("\n")
            
            # Write each DataFrame
            for section_name, df in data.items():
                f.write(f"## {section_name}\n\n")
                f.write(df.to_markdown(index=False))
                f.write("\n\n")
        
        logger.info(f"📑 Markdown exported: {output_path}")
        return output_path
    
    def export_to_html(
        self,
        data: Dict[str, pd.DataFrame],
        filename: str = "results.html",
        title: str = "MENA Bias Evaluation Results"
    ) -> Path:
        """
        Export DataFrames to HTML with styling
        
        Args:
            data: Dictionary of section_name -> DataFrame
            filename: Output filename
            title: Page title
        
        Returns:
            Path to exported file
        """
        output_path = self.output_dir / filename
        
        # Create HTML
        html_parts = []
        
        # HTML header with styling
        html_parts.append(f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-left: 4px solid #3498db;
            padding-left: 10px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            background-color: white;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        th {{
            background-color: #3498db;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }}
        td {{
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }}
        tr:hover {{
            background-color: #f2f2f2;
        }}
        .metadata {{
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    
    <div class="metadata">
        <h3>Metadata</h3>
""")
        
        # Add metadata
        for key, value in self.metadata.items():
            html_parts.append(f"        <p><strong>{key}:</strong> {value}</p>\n")
        
        html_parts.append("    </div>\n")
        
        # Add each DataFrame
        for section_name, df in data.items():
            html_parts.append(f"    <h2>{section_name}</h2>\n")
            html_parts.append(df.to_html(index=False, classes='results-table'))
            html_parts.append("\n")
        
        # Close HTML
        html_parts.append("</body>\n</html>")
        
        # Write file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(''.join(html_parts))
        
        logger.info(f"🌐 HTML exported: {output_path}")
        return output_path
    
    def export_all_formats(
        self,
        dataframes: Dict[str, pd.DataFrame],
        base_filename: str = "results"
    ) -> Dict[str, Path]:
        """
        Export to all supported formats
        
        Args:
            dataframes: Dictionary of DataFrames to export
            base_filename: Base name for output files
        
        Returns:
            Dictionary of format -> file path
        """
        logger.info("📤 Exporting to all formats...")
        
        exported_files = {}
        
        # Excel
        try:
            path = self.export_to_excel(dataframes, f"{base_filename}.xlsx")
            exported_files['excel'] = path
        except Exception as e:
            logger.error(f"Excel export failed: {e}")
        
        # JSON
        try:
            json_data = {
                name: df.to_dict(orient='records')
                for name, df in dataframes.items()
            }
            path = self.export_to_json(json_data, f"{base_filename}.json")
            exported_files['json'] = path
        except Exception as e:
            logger.error(f"JSON export failed: {e}")
        
        # Markdown
        try:
            path = self.export_to_markdown(dataframes, f"{base_filename}.md")
            exported_files['markdown'] = path
        except Exception as e:
            logger.error(f"Markdown export failed: {e}")
        
        # HTML
        try:
            path = self.export_to_html(dataframes, f"{base_filename}.html")
            exported_files['html'] = path
        except Exception as e:
            logger.error(f"HTML export failed: {e}")
        
        # CSV (first DataFrame only)
        try:
            first_df = list(dataframes.values())[0]
            path = self.export_to_csv(first_df, f"{base_filename}.csv")
            exported_files['csv'] = path
        except Exception as e:
            logger.error(f"CSV export failed: {e}")
        
        logger.info(f"✅ Exported to {len(exported_files)} formats")
        
        return exported_files


# Example usage
if __name__ == "__main__":
    print("📤 Testing Export Utilities\n")
    
    # Create sample data
    results_df = pd.DataFrame({
        'Model': ['Model_A', 'Model_B', 'Model_C'],
        'Accuracy': [0.85, 0.88, 0.82],
        'F1_Score': [0.83, 0.86, 0.80],
        'Bias_Score': [0.12, 0.08, 0.15]
    })
    
    metrics_df = pd.DataFrame({
        'Metric': ['Demographic Parity', 'Equalized Odds', 'Disparate Impact'],
        'Value': [0.08, 0.12, 0.85],
        'Threshold': [0.10, 0.10, 0.80],
        'Passed': [True, False, True]
    })
    
    # Initialize exporter
    exporter = ExportManager()
    
    # Export to all formats
    dataframes = {
        'Results': results_df,
        'Metrics': metrics_df
    }
    
    exported = exporter.export_all_formats(dataframes, "test_export")
    
    print("\n✅ Files exported:")
    for format_name, path in exported.items():
        print(f"  {format_name}: {path}")
    
    print("\n✅ Test completed!")