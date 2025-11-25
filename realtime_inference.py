#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real-time Inference Engine for MENA Bias Evaluation Pipeline
High-performance streaming inference with batching and caching
"""

import asyncio
import time
from typing import List, Dict, Any, Optional
from collections import deque
from dataclasses import dataclass
from datetime import datetime
import threading
import logging

import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification

logger = logging.getLogger(__name__)


@dataclass
class InferenceRequest:
    """Single inference request"""
    id: str
    text: str
    timestamp: float
    callback: Optional[callable] = None


@dataclass
class InferenceResult:
    """Inference result"""
    request_id: str
    text: str
    sentiment: str
    confidence: float
    processing_time: float
    timestamp: float


class InferenceQueue:
    """Thread-safe queue for inference requests"""
    
    def __init__(self, maxsize: int = 1000):
        self.queue = deque(maxlen=maxsize)
        self.lock = threading.Lock()
    
    def put(self, item: InferenceRequest):
        """Add item to queue"""
        with self.lock:
            self.queue.append(item)
    
    def get_batch(self, batch_size: int) -> List[InferenceRequest]:
        """Get batch of items from queue"""
        with self.lock:
            batch = []
            while len(batch) < batch_size and self.queue:
                batch.append(self.queue.popleft())
            return batch
    
    def size(self) -> int:
        """Get queue size"""
        with self.lock:
            return len(self.queue)
    
    def is_empty(self) -> bool:
        """Check if queue is empty"""
        with self.lock:
            return len(self.queue) == 0


class RealtimeInferenceEngine:
    """
    Real-time inference engine with intelligent batching
    
    Features:
    - Automatic batching for efficiency
    - Request queue management
    - Dynamic batch sizing
    - Performance monitoring
    - GPU/CPU optimization
    """
    
    def __init__(
        self,
        model_name: str,
        device: str = "cpu",
        batch_size: int = 32,
        max_queue_size: int = 1000,
        max_wait_time: float = 0.1  # seconds
    ):
        self.model_name = model_name
        self.device = device
        self.batch_size = batch_size
        self.max_wait_time = max_wait_time
        
        # Initialize queue
        self.queue = InferenceQueue(maxsize=max_queue_size)
        
        # Load model and tokenizer
        logger.info(f"Loading model: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.to(device)
        self.model.eval()
        
        # Label mapping
        self.id2label = {0: 'negative', 1: 'neutral', 2: 'positive'}
        
        # Performance metrics
        self.total_requests = 0
        self.total_processing_time = 0
        self.batch_count = 0
        
        # Control flags
        self.running = False
        self.worker_thread = None
        
        logger.info("✅ Realtime Inference Engine initialized")
    
    def start(self):
        """Start the inference worker thread"""
        if self.running:
            logger.warning("Engine already running")
            return
        
        self.running = True
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()
        logger.info("🚀 Inference worker started")
    
    def stop(self):
        """Stop the inference worker thread"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
        logger.info("🛑 Inference worker stopped")
    
    def _worker(self):
        """Background worker that processes batches"""
        logger.info("Worker thread started")
        
        while self.running:
            # Wait for requests or timeout
            if self.queue.is_empty():
                time.sleep(0.01)  # Small sleep to avoid busy waiting
                continue
            
            # Wait for batch to fill or timeout
            start_wait = time.time()
            while (time.time() - start_wait < self.max_wait_time and 
                   self.queue.size() < self.batch_size):
                time.sleep(0.001)
            
            # Get batch
            batch = self.queue.get_batch(self.batch_size)
            
            if batch:
                self._process_batch(batch)
    
    def _process_batch(self, batch: List[InferenceRequest]):
        """Process a batch of requests"""
        start_time = time.time()
        
        # Extract texts
        texts = [req.text for req in batch]
        
        # Tokenize
        inputs = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt"
        ).to(self.device)
        
        # Inference
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probs = torch.nn.functional.softmax(logits, dim=-1)
            predictions = torch.argmax(probs, dim=-1)
            confidences = torch.max(probs, dim=-1).values
        
        # Process results
        processing_time = time.time() - start_time
        
        for i, req in enumerate(batch):
            sentiment = self.id2label[predictions[i].item()]
            confidence = confidences[i].item()
            
            result = InferenceResult(
                request_id=req.id,
                text=req.text,
                sentiment=sentiment,
                confidence=confidence,
                processing_time=processing_time / len(batch),
                timestamp=time.time()
            )
            
            # Call callback if provided
            if req.callback:
                req.callback(result)
        
        # Update metrics
        self.total_requests += len(batch)
        self.total_processing_time += processing_time
        self.batch_count += 1
        
        # Log performance
        avg_time = processing_time / len(batch) * 1000  # ms per request
        logger.debug(
            f"Batch processed: {len(batch)} requests, "
            f"{avg_time:.2f}ms per request"
        )
    
    async def predict_async(
        self,
        text: str,
        request_id: Optional[str] = None
    ) -> InferenceResult:
        """
        Async prediction with automatic batching
        
        Args:
            text: Input text
            request_id: Optional request ID
        
        Returns:
            InferenceResult
        """
        if not self.running:
            raise RuntimeError("Engine not started. Call start() first.")
        
        # Generate request ID
        if request_id is None:
            request_id = f"req_{int(time.time() * 1000000)}"
        
        # Create result holder
        result_future = asyncio.Future()
        
        def callback(result: InferenceResult):
            result_future.set_result(result)
        
        # Create request
        request = InferenceRequest(
            id=request_id,
            text=text,
            timestamp=time.time(),
            callback=callback
        )
        
        # Add to queue
        self.queue.put(request)
        
        # Wait for result
        result = await result_future
        return result
    
    def predict_sync(self, text: str) -> InferenceResult:
        """
        Synchronous prediction (blocks until complete)
        
        Args:
            text: Input text
        
        Returns:
            InferenceResult
        """
        # Direct inference without queue
        start_time = time.time()
        
        # Tokenize
        inputs = self.tokenizer(
            text,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt"
        ).to(self.device)
        
        # Inference
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probs = torch.nn.functional.softmax(logits, dim=-1)
            prediction = torch.argmax(probs, dim=-1)
            confidence = torch.max(probs, dim=-1).values
        
        sentiment = self.id2label[prediction.item()]
        processing_time = time.time() - start_time
        
        return InferenceResult(
            request_id=f"sync_{int(time.time() * 1000000)}",
            text=text,
            sentiment=sentiment,
            confidence=confidence.item(),
            processing_time=processing_time,
            timestamp=time.time()
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        avg_time = (
            self.total_processing_time / self.total_requests * 1000
            if self.total_requests > 0 else 0
        )
        
        throughput = (
            self.total_requests / self.total_processing_time
            if self.total_processing_time > 0 else 0
        )
        
        return {
            'total_requests': self.total_requests,
            'total_batches': self.batch_count,
            'avg_batch_size': self.total_requests / self.batch_count if self.batch_count > 0 else 0,
            'avg_processing_time_ms': avg_time,
            'throughput_per_sec': throughput,
            'queue_size': self.queue.size(),
            'device': self.device
        }
    
    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()


# Example usage and testing
async def test_realtime_inference():
    """Test the realtime inference engine"""
    
    # Initialize engine
    engine = RealtimeInferenceEngine(
        model_name="CAMeL-Lab/bert-base-arabic-camelbert-da-sentiment",
        device="cpu",
        batch_size=8,
        max_wait_time=0.05
    )
    
    # Start engine
    engine.start()
    
    try:
        # Test async predictions
        test_texts = [
            "الخدمة ممتازة جداً",
            "المنتج سيء للغاية",
            "لا بأس به",
            "تجربة رائعة",
            "غير راضٍ تماماً"
        ]
        
        print("🔄 Running async predictions...")
        
        # Send all requests
        tasks = [
            engine.predict_async(text, f"req_{i}")
            for i, text in enumerate(test_texts)
        ]
        
        # Wait for all results
        results = await asyncio.gather(*tasks)
        
        # Display results
        print("\n📊 Results:")
        for result in results:
            print(f"  {result.request_id}: {result.sentiment} "
                  f"(confidence: {result.confidence:.3f}, "
                  f"time: {result.processing_time*1000:.2f}ms)")
        
        # Display stats
        print("\n📈 Performance Stats:")
        stats = engine.get_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    finally:
        # Stop engine
        engine.stop()


if __name__ == "__main__":
    # Test the engine
    print("🚀 Testing Realtime Inference Engine\n")
    asyncio.run(test_realtime_inference())
    print("\n✅ Test completed!")