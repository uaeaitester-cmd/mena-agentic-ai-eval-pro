#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Structured Logging Module for MENA Bias Evaluation Pipeline
Provides consistent logging across the application
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
import json


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""
    
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'       # Reset
    }
    
    def format(self, record):
        if sys.platform == 'win32':
            # Windows console may not support colors
            return super().format(record)
        
        log_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        record.levelname = f"{log_color}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)


class JSONFormatter(logging.Formatter):
    """Formatter for structured JSON logging"""
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


def setup_logger(
    name: str = 'mena_pipeline',
    level: str = 'INFO',
    log_file: str = 'pipeline.log',
    enable_console: bool = True,
    enable_json: bool = False
) -> logging.Logger:
    """
    Setup and configure logger
    
    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file
        enable_console: Whether to log to console
        enable_json: Whether to use JSON formatting for file logs
    
    Returns:
        Configured logger instance
    """
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = ColoredFormatter(
            '%(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        if enable_json:
            file_formatter = JSONFormatter()
        else:
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


class PipelineLogger:
    """Context manager for pipeline stage logging"""
    
    def __init__(self, logger: logging.Logger, stage_name: str):
        self.logger = logger
        self.stage_name = stage_name
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.info(f"Starting: {self.stage_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (datetime.now() - self.start_time).total_seconds()
        
        if exc_type is None:
            self.logger.info(
                f"Completed: {self.stage_name} (Duration: {duration:.2f}s)"
            )
        else:
            self.logger.error(
                f"Failed: {self.stage_name} (Duration: {duration:.2f}s) - {exc_val}"
            )
        
        return False  # Don't suppress exceptions


# Default logger instance
default_logger = setup_logger()


# Convenience functions
def log_metric(name: str, value: float, unit: str = ''):
    """Log a metric value"""
    default_logger.info(f"METRIC: {name} = {value} {unit}")


def log_config(config: dict):
    """Log configuration dictionary"""
    default_logger.debug(f"Configuration: {json.dumps(config, indent=2)}")


def log_dataframe_info(df, name: str = 'DataFrame'):
    """Log information about a DataFrame"""
    default_logger.info(f"{name}: shape={df.shape}, memory={df.memory_usage().sum() / 1024:.2f}KB")


if __name__ == "__main__":
    # Test logging
    logger = setup_logger('test', level='DEBUG')
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    with PipelineLogger(logger, "Test Stage"):
        import time
        time.sleep(1)
        logger.info("Processing...")
    
    log_metric("accuracy", 0.95, "%")
    print("✅ Logger test completed!")