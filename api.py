#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REST API for MENA Bias Evaluation Pipeline
FastAPI-based web service for bias analysis
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import pandas as pd
import io
import yaml
from pathlib import Path
import logging

# Import pipeline components
from pipeline import (
    OODALoop,
    predict_sentiment,
    analyze_bias,
    calculate_fairness_metrics
)
from model_loader import ModelLoader
from validators import DataFrameValidator
from logger import setup_logger

# Setup
logger = setup_logger('api', level='INFO')
app = FastAPI(
    title="MENA Bias Evaluation API",
    description="REST API for detecting bias in Arabic/Persian sentiment models",
    version="1.0.0"
)

# Load config
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Load model
model_loader = ModelLoader(config)
model, tokenizer = model_loader.load_model_and_tokenizer()

logger.info("✅ API initialized successfully")


# Request/Response Models
class TextInput(BaseModel):
    """Single text input for analysis"""
    text: str = Field(..., min_length=1, max_length=10000, description="Text to analyze")


class BatchTextInput(BaseModel):
    """Batch text input for analysis"""
    texts: List[str] = Field(..., min_items=1, max_items=1000, description="List of texts")


class PredictionResponse(BaseModel):
    """Prediction response"""
    text: str
    sentiment: str
    confidence: Optional[float] = None


class BiasAnalysisResponse(BaseModel):
    """Bias analysis response"""
    total_samples: int
    bias_results: Dict[str, Any]
    fairness_metrics: Dict[str, float]
    ooda_summary: Dict[str, Any]


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    version: str


# Endpoints

@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "version": "1.0.0"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy" if model is not None else "degraded",
        "model_loaded": model is not None,
        "version": "1.0.0"
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict_single(input_data: TextInput):
    """
    Predict sentiment for a single text
    
    - **text**: Input text (1-10000 characters)
    
    Returns sentiment prediction
    """
    try:
        predictions = predict_sentiment([input_data.text], model, tokenizer)
        
        return {
            "text": input_data.text,
            "sentiment": predictions[0],
            "confidence": None  # Could add confidence scores
        }
    
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/batch", response_model=List[PredictionResponse])
async def predict_batch(input_data: BatchTextInput):
    """
    Predict sentiment for multiple texts
    
    - **texts**: List of texts (1-1000 items)
    
    Returns list of predictions
    """
    try:
        predictions = predict_sentiment(input_data.texts, model, tokenizer)
        
        return [
            {
                "text": text,
                "sentiment": pred,
                "confidence": None
            }
            for text, pred in zip(input_data.texts, predictions)
        ]
    
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/bias", response_model=BiasAnalysisResponse)
async def analyze_bias_endpoint(file: UploadFile = File(...)):
    """
    Analyze bias in uploaded CSV file
    
    - **file**: CSV file with columns: text, sentiment, region, gender, age_group
    
    Returns comprehensive bias analysis
    """
    try:
        # Read uploaded file
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # Validate DataFrame
        DataFrameValidator.validate_dataframe(
            df,
            required_columns=['text', 'sentiment', 'region', 'gender', 'age_group'],
            min_rows=10
        )
        
        # OODA Loop
        ooda = OODALoop()
        observation = ooda.observe(df)
        
        # Predict
        predictions = predict_sentiment(df['text'].tolist(), model, tokenizer)
        
        # Orient
        ground_truth = df['sentiment'].values
        orientation = ooda.orient(predictions, ground_truth)
        
        # Decide
        decision = ooda.decide(orientation)
        
        # Act
        action = ooda.act(decision)
        
        # Bias analysis
        bias_results = analyze_bias(df, predictions)
        
        return {
            "total_samples": len(df),
            "bias_results": bias_results,
            "fairness_metrics": bias_results.get('fairness', {}),
            "ooda_summary": {
                "accuracy": orientation['accuracy'],
                "severity": decision['severity'],
                "recommended_actions": decision['recommended_actions']
            }
        }
    
    except Exception as e:
        logger.error(f"Bias analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/report/download")
async def download_report():
    """
    Download latest PDF report
    
    Returns PDF file
    """
    report_path = Path(config['data']['output_dir']) / config['report']['filename']
    
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="Report notif __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 7860))  
    uvicorn.run(app, host="0.0.0.0", port=port)