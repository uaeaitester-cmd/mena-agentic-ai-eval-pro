#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Input Validation Module for MENA Bias Evaluation Pipeline
Ensures data quality and prevents errors
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional
import yaml


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class ConfigValidator:
    """Validator for configuration files"""
    
    @staticmethod
    def validate_config(config_path: str) -> Dict[str, Any]:
        """
        Validate and load configuration file
        
        Args:
            config_path: Path to YAML config file
            
        Returns:
            Validated configuration dictionary
            
        Raises:
            ValidationError: If configuration is invalid
        """
        config_file = Path(config_path)
        
        if not config_file.exists():
            raise ValidationError(f"Config file not found: {config_path}")
        
        if config_file.suffix not in ['.yaml', '.yml']:
            raise ValidationError(f"Config file must be YAML: {config_path}")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Validate required sections
        required_sections = ['model', 'data', 'bias', 'visualization', 'report']
        for section in required_sections:
            if section not in config:
                raise ValidationError(f"Missing required config section: {section}")
        
        # Validate model config
        if 'name' not in config['model']:
            raise ValidationError("Model name not specified in config")
        
        # Validate data paths
        if 'input_dir' not in config['data'] or 'output_dir' not in config['data']:
            raise ValidationError("Input/output directories not specified in config")
        
        return config


class DataFrameValidator:
    """Validator for DataFrame inputs"""
    
    @staticmethod
    def validate_dataframe(
        df: pd.DataFrame,
        required_columns: List[str],
        min_rows: int = 1,
        max_nulls_ratio: float = 0.1
    ) -> None:
        """
        Validate DataFrame structure and content
        
        Args:
            df: DataFrame to validate
            required_columns: List of required column names
            min_rows: Minimum number of rows required
            max_nulls_ratio: Maximum ratio of null values allowed (0-1)
            
        Raises:
            ValidationError: If validation fails
        """
        
        # Check if DataFrame is empty
        if df is None or len(df) == 0:
            raise ValidationError("DataFrame is empty")
        
        # Check minimum rows
        if len(df) < min_rows:
            raise ValidationError(
                f"DataFrame has {len(df)} rows, minimum required: {min_rows}"
            )
        
        # Check required columns
        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            raise ValidationError(f"Missing required columns: {missing_cols}")
        
        # Check for excessive null values
        for col in required_columns:
            null_ratio = df[col].isnull().sum() / len(df)
            if null_ratio > max_nulls_ratio:
                raise ValidationError(
                    f"Column '{col}' has {null_ratio:.1%} null values "
                    f"(max allowed: {max_nulls_ratio:.1%})"
                )
        
        # Check for duplicate rows
        if df.duplicated().sum() > len(df) * 0.5:
            raise ValidationError(
                f"DataFrame has too many duplicate rows: {df.duplicated().sum()}"
            )
    
    @staticmethod
    def validate_text_column(
        df: pd.DataFrame,
        column: str,
        min_length: int = 1,
        max_length: int = 10000
    ) -> None:
        """
        Validate text column in DataFrame
        
        Args:
            df: DataFrame containing the column
            column: Name of text column
            min_length: Minimum text length
            max_length: Maximum text length
            
        Raises:
            ValidationError: If validation fails
        """
        
        if column not in df.columns:
            raise ValidationError(f"Column '{column}' not found in DataFrame")
        
        # Check data type
        if not pd.api.types.is_string_dtype(df[column]):
            raise ValidationError(f"Column '{column}' must be string type")
        
        # Check text lengths
        lengths = df[column].str.len()
        
        too_short = (lengths < min_length).sum()
        if too_short > 0:
            raise ValidationError(
                f"{too_short} texts in '{column}' are shorter than {min_length} characters"
            )
        
        too_long = (lengths > max_length).sum()
        if too_long > 0:
            raise ValidationError(
                f"{too_long} texts in '{column}' are longer than {max_length} characters"
            )
        
        # Check for empty strings
        empty_count = (df[column].str.strip() == '').sum()
        if empty_count > 0:
            raise ValidationError(
                f"{empty_count} texts in '{column}' are empty or whitespace-only"
            )
    
    @staticmethod
    def validate_categorical_column(
        df: pd.DataFrame,
        column: str,
        allowed_values: Optional[List[str]] = None,
        min_categories: int = 2
    ) -> None:
        """
        Validate categorical column in DataFrame
        
        Args:
            df: DataFrame containing the column
            column: Name of categorical column
            allowed_values: List of allowed category values (None = any)
            min_categories: Minimum number of unique categories
            
        Raises:
            ValidationError: If validation fails
        """
        
        if column not in df.columns:
            raise ValidationError(f"Column '{column}' not found in DataFrame")
        
        unique_values = df[column].unique()
        
        # Check minimum categories
        if len(unique_values) < min_categories:
            raise ValidationError(
                f"Column '{column}' has {len(unique_values)} categories, "
                f"minimum required: {min_categories}"
            )
        
        # Check allowed values
        if allowed_values is not None:
            invalid_values = set(unique_values) - set(allowed_values)
            if invalid_values:
                raise ValidationError(
                    f"Column '{column}' contains invalid values: {invalid_values}"
                )


class ModelValidator:
    """Validator for model files and outputs"""
    
    @staticmethod
    def validate_model_file(model_path: str, min_size_mb: float = 1.0) -> None:
        """
        Validate model file exists and has reasonable size
        
        Args:
            model_path: Path to model file
            min_size_mb: Minimum expected file size in MB
            
        Raises:
            ValidationError: If validation fails
        """
        
        model_file = Path(model_path)
        
        if not model_file.exists():
            raise ValidationError(f"Model file not found: {model_path}")
        
        # Check file size
        size_mb = model_file.stat().st_size / (1024 * 1024)
        if size_mb < min_size_mb:
            raise ValidationError(
                f"Model file is suspiciously small: {size_mb:.2f}MB "
                f"(expected >{min_size_mb}MB)"
            )
    
    @staticmethod
    def validate_predictions(
        predictions: List[str],
        expected_length: int,
        allowed_labels: List[str]
    ) -> None:
        """
        Validate model predictions
        
        Args:
            predictions: List of prediction labels
            expected_length: Expected number of predictions
            allowed_labels: List of valid label values
            
        Raises:
            ValidationError: If validation fails
        """
        
        if len(predictions) != expected_length:
            raise ValidationError(
                f"Expected {expected_length} predictions, got {len(predictions)}"
            )
        
        invalid_preds = set(predictions) - set(allowed_labels)
        if invalid_preds:
            raise ValidationError(
                f"Predictions contain invalid labels: {invalid_preds}"
            )
        
        # Check for suspicious patterns (e.g., all same prediction)
        unique_ratio = len(set(predictions)) / len(predictions)
        if unique_ratio < 0.1:  # Less than 10% diversity
            raise ValidationError(
                f"Predictions lack diversity: only {unique_ratio:.1%} unique values"
            )


class PathValidator:
    """Validator for file paths"""
    
    @staticmethod
    def validate_directory(dir_path: str, create_if_missing: bool = False) -> Path:
        """
        Validate directory exists or create it
        
        Args:
            dir_path: Path to directory
            create_if_missing: Whether to create directory if it doesn't exist
            
        Returns:
            Path object
            
        Raises:
            ValidationError: If directory invalid and not created
        """
        
        directory = Path(dir_path)
        
        if not directory.exists():
            if create_if_missing:
                directory.mkdir(parents=True, exist_ok=True)
            else:
                raise ValidationError(f"Directory not found: {dir_path}")
        
        if not directory.is_dir():
            raise ValidationError(f"Path is not a directory: {dir_path}")
        
        return directory
    
    @staticmethod
    def validate_file(file_path: str, extensions: Optional[List[str]] = None) -> Path:
        """
        Validate file exists and has correct extension
        
        Args:
            file_path: Path to file
            extensions: List of allowed extensions (e.g., ['.csv', '.txt'])
            
        Returns:
            Path object
            
        Raises:
            ValidationError: If file invalid
        """
        
        file = Path(file_path)
        
        if not file.exists():
            raise ValidationError(f"File not found: {file_path}")
        
        if not file.is_file():
            raise ValidationError(f"Path is not a file: {file_path}")
        
        if extensions is not None:
            if file.suffix.lower() not in [ext.lower() for ext in extensions]:
                raise ValidationError(
                    f"File has invalid extension: {file.suffix} "
                    f"(allowed: {extensions})"
                )
        
        return file


# Convenience function for complete validation
def validate_pipeline_inputs(
    config_path: str,
    data_path: Optional[str] = None,
    model_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Validate all pipeline inputs
    
    Args:
        config_path: Path to configuration file
        data_path: Path to input data CSV (optional)
        model_path: Path to model file (optional)
        
    Returns:
        Dictionary with validation results
        
    Raises:
        ValidationError: If any validation fails
    """
    
    results = {
        'config': None,
        'data_valid': False,
        'model_valid': False,
        'errors': []
    }
    
    # Validate config
    try:
        results['config'] = ConfigValidator.validate_config(config_path)
    except ValidationError as e:
        results['errors'].append(f"Config validation failed: {e}")
        raise
    
    # Validate data if provided
    if data_path:
        try:
            PathValidator.validate_file(data_path, extensions=['.csv'])
            df = pd.read_csv(data_path)
            DataFrameValidator.validate_dataframe(
                df,
                required_columns=['text', 'sentiment'],
                min_rows=10
            )
            results['data_valid'] = True
        except Exception as e:
            results['errors'].append(f"Data validation failed: {e}")
    
    # Validate model if provided
    if model_path:
        try:
            ModelValidator.validate_model_file(model_path, min_size_mb=10)
            results['model_valid'] = True
        except Exception as e:
            results['errors'].append(f"Model validation failed: {e}")
    
    return results


if __name__ == "__main__":
    # Test validators
    print("Testing validators...")
    
    # Test DataFrame validator
    test_df = pd.DataFrame({
        'text': ['test1', 'test2', 'test3'],
        'sentiment': ['positive', 'negative', 'neutral']
    })
    
    try:
        DataFrameValidator.validate_dataframe(
            test_df,
            required_columns=['text', 'sentiment']
        )
        print("✅ DataFrame validation passed")
    except ValidationError as e:
        print(f"❌ DataFrame validation failed: {e}")
    
    print("✅ Validator tests completed!")