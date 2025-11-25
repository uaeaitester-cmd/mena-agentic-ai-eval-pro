#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Performance Optimization Module for MENA Bias Evaluation Pipeline
Includes caching, batching, and profiling utilities
"""

import time
import functools
import pickle
from pathlib import Path
from typing import Any, Callable, Optional
import hashlib
import logging

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Monitor and log performance metrics"""
    
    def __init__(self):
        self.metrics = {}
    
    def time_function(self, func: Callable) -> Callable:
        """Decorator to time function execution"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start
            
            func_name = func.__name__
            if func_name not in self.metrics:
                self.metrics[func_name] = []
            
            self.metrics[func_name].append(duration)
            logger.info(f"⏱️  {func_name} completed in {duration:.2f}s")
            
            return result
        return wrapper
    
    def get_stats(self):
        """Get performance statistics"""
        stats = {}
        for func_name, times in self.metrics.items():
            stats[func_name] = {
                'count': len(times),
                'total': sum(times),
                'avg': sum(times) / len(times),
                'min': min(times),
                'max': max(times)
            }
        return stats


class ResultCache:
    """Cache expensive computation results"""
    
    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def _get_cache_key(self, func_name: str, args, kwargs) -> str:
        """Generate unique cache key"""
        key_data = f"{func_name}:{str(args)}:{str(kwargs)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def cache_result(self, func: Callable) -> Callable:
        """Decorator to cache function results"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = self._get_cache_key(func.__name__, args, kwargs)
            cache_file = self.cache_dir / f"{cache_key}.pkl"
            
            # Try to load from cache
            if cache_file.exists():
                try:
                    with open(cache_file, 'rb') as f:
                        result = pickle.load(f)
                    logger.info(f"✅ Loaded {func.__name__} from cache")
                    return result
                except Exception as e:
                    logger.warning(f"Cache load failed: {e}")
            
            # Compute result
            result = func(*args, **kwargs)
            
            # Save to cache
            try:
                with open(cache_file, 'wb') as f:
                    pickle.dump(result, f)
                logger.info(f"💾 Cached {func.__name__} result")
            except Exception as e:
                logger.warning(f"Cache save failed: {e}")
            
            return result
        return wrapper
    
    def clear_cache(self):
        """Clear all cached results"""
        for cache_file in self.cache_dir.glob("*.pkl"):
            cache_file.unlink()
        logger.info("🗑️  Cache cleared")


class BatchProcessor:
    """Process data in optimized batches"""
    
    def __init__(self, batch_size: int = 32):
        self.batch_size = batch_size
    
    def process_in_batches(
        self,
        data: list,
        process_fn: Callable,
        show_progress: bool = True
    ) -> list:
        """Process data in batches"""
        results = []
        total_batches = (len(data) + self.batch_size - 1) // self.batch_size
        
        for i in range(0, len(data), self.batch_size):
            batch = data[i:i + self.batch_size]
            
            if show_progress:
                batch_num = i // self.batch_size + 1
                logger.info(f"Processing batch {batch_num}/{total_batches}")
            
            batch_results = process_fn(batch)
            results.extend(batch_results)
        
        return results


# Global instances
performance_monitor = PerformanceMonitor()
result_cache = ResultCache()
batch_processor = BatchProcessor()


# Convenience decorators
def timeit(func: Callable) -> Callable:
    """Decorator to time function execution"""
    return performance_monitor.time_function(func)


def cached(func: Callable) -> Callable:
    """Decorator to cache function results"""
    return result_cache.cache_result(func)


if __name__ == "__main__":
    # Test performance utilities
    
    @timeit
    @cached
    def slow_function(n):
        """Simulate slow computation"""
        time.sleep(1)
        return n * 2
    
    print("First call (should be slow):")
    result1 = slow_function(5)
    
    print("\nSecond call (should be fast - cached):")
    result2 = slow_function(5)
    
    print("\nPerformance stats:")
    print(performance_monitor.get_stats())
    
    print("\n✅ Performance module test completed!")