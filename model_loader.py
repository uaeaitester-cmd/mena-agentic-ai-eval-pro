#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Model Loader for MENA Bias Evaluation Pipeline
Handles local and remote model loading with caching
"""

import os
import torch
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    AutoConfig
)
import logging

logger = logging.getLogger(__name__)


class ModelLoader:
    """Advanced model loader with fallback strategies"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model_name = config['model']['name']
        self.local_path = config['model'].get('local_path')
        self.cache_dir = config['model'].get('cache_dir', '.model_cache')
        self.device = config['model'].get('device', 'cpu')
        
    def load_model_and_tokenizer(self) -> Tuple[Optional[Any], Optional[Any]]:
        """
        Load model and tokenizer with multiple fallback strategies
        
        Returns:
            Tuple of (model, tokenizer) or (None, None) if all strategies fail
        """
        
        # Strategy 1: Try local model with config
        if self.local_path and os.path.exists(self.local_path):
            logger.info(f"Attempting to load local model from {self.local_path}")
            result = self._load_local_with_config()
            if result[0] is not None:
                return result
        
        # Strategy 2: Try HuggingFace Hub
        logger.info(f"Attempting to load from HuggingFace Hub: {self.model_name}")
        result = self._load_from_hub()
        if result[0] is not None:
            return result
        
        # Strategy 3: Use cached model if available
        logger.info("Attempting to use cached model")
        result = self._load_from_cache()
        if result[0] is not None:
            return result
        
        # All strategies failed - return None for dummy mode
        logger.warning("All model loading strategies failed. Using dummy mode.")
        return None, None
    
    def _load_local_with_config(self) -> Tuple[Optional[Any], Optional[Any]]:
        """Load model from local path with proper config"""
        try:
            # Try to load config from HuggingFace
            config = AutoConfig.from_pretrained(
                self.model_name,
                cache_dir=self.cache_dir
            )
            
            # Load tokenizer
            tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                cache_dir=self.cache_dir
            )
            
            # Load model architecture
            model = AutoModelForSequenceClassification.from_config(config)
            
            # Load weights from local file
            state_dict = torch.load(
                self.local_path,
                map_location=torch.device(self.device)
            )
            
            model.load_state_dict(state_dict, strict=False)
            model.eval()
            
            logger.info("✅ Successfully loaded local model with config")
            return model, tokenizer
            
        except Exception as e:
            logger.error(f"Local loading failed: {e}")
            return None, None
    
    def _load_from_hub(self) -> Tuple[Optional[Any], Optional[Any]]:
        """Load model directly from HuggingFace Hub"""
        try:
            tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                cache_dir=self.cache_dir
            )
            
            model = AutoModelForSequenceClassification.from_pretrained(
                self.model_name,
                cache_dir=self.cache_dir
            )
            
            model.to(self.device)
            model.eval()
            
            logger.info("✅ Successfully loaded model from HuggingFace Hub")
            return model, tokenizer
            
        except Exception as e:
            logger.error(f"HuggingFace Hub loading failed: {e}")
            return None, None
    
    def _load_from_cache(self) -> Tuple[Optional[Any], Optional[Any]]:
        """Load model from cache directory"""
        try:
            cache_path = Path(self.cache_dir)
            if not cache_path.exists():
                return None, None
            
            # Look for cached model
            model_dirs = list(cache_path.glob("models--*"))
            if not model_dirs:
                return None, None
            
            # Try to load from most recent cache
            latest_cache = max(model_dirs, key=lambda p: p.stat().st_mtime)
            
            tokenizer = AutoTokenizer.from_pretrained(str(latest_cache))
            model = AutoModelForSequenceClassification.from_pretrained(str(latest_cache))
            
            model.to(self.device)
            model.eval()
            
            logger.info("✅ Successfully loaded model from cache")
            return model, tokenizer
            
        except Exception as e:
            logger.error(f"Cache loading failed: {e}")
            return None, None