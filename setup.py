#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup configuration for MENA Bias Evaluation Pipeline
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = [
        line.strip()
        for line in requirements_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]

# Read dev requirements
dev_requirements_file = Path(__file__).parent / "requirements-dev.txt"
dev_requirements = []
if dev_requirements_file.exists():
    dev_requirements = [
        line.strip()
        for line in dev_requirements_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#") and not line.startswith("-r")
    ]

setup(
    name="mena-bias-evaluation",
    version="1.0.0",
    description="Comprehensive bias detection toolkit for Arabic/Persian sentiment analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/mena-bias-evaluation",
    license="MIT",
    
    packages=find_packages(exclude=["tests", "tests.*", "docs"]),
    py_modules=["pipeline", "logger", "validators"],
    
    python_requires=">=3.10",
    
    install_requires=requirements,
    
    extras_require={
        "dev": dev_requirements,
        "test": [
            "pytest>=8.0.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
        ],
    },
    
    entry_points={
        "console_scripts": [
            "mena-eval=pipeline:main",
        ],
    },
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Natural Language :: Arabic",
        "Natural Language :: Persian",
    ],
    
    keywords=[
        "nlp",
        "bias-detection",
        "fairness",
        "arabic",
        "persian",
        "sentiment-analysis",
        "machine-learning",
        "ai-ethics",
    ],
    
    project_urls={
        "Bug Reports": "https://github.com/yourusername/mena-bias-evaluation/issues",
        "Source": "https://github.com/yourusername/mena-bias-evaluation",
        "Documentation": "https://mena-bias-evaluation.readthedocs.io",
    },
    
    include_package_data=True,
    zip_safe=False,
)