#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit Tests for MENA Bias Evaluation Pipeline
Comprehensive test coverage with pytest
"""

import pytest
import pandas as pd
import numpy as np
import os
import sys
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pipeline import (
    OODALoop,
    generate_sample_data,
    predict_sentiment,
    analyze_bias,
    calculate_fairness_metrics
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing"""
    data = {
        'text': ['test sentence 1', 'test sentence 2', 'test sentence 3'],
        'sentiment': ['positive', 'negative', 'neutral'],
        'region': ['Gulf', 'Levant', 'Egypt'],
        'gender': ['male', 'female', 'male'],
        'age_group': ['18-25', '26-35', '36-45']
    }
    return pd.DataFrame(data)


@pytest.fixture
def ooda_loop():
    """Create an OODA Loop instance"""
    return OODALoop()


@pytest.fixture
def mock_model():
    """Create a mock model for testing"""
    model = MagicMock()
    return model


@pytest.fixture
def mock_tokenizer():
    """Create a mock tokenizer for testing"""
    tokenizer = MagicMock()
    return tokenizer


# ============================================================================
# Test OODALoop Class
# ============================================================================

class TestOODALoop:
    """Test suite for OODA Loop implementation"""
    
    def test_initialization(self, ooda_loop):
        """Test OODA Loop initializes correctly"""
        assert ooda_loop.observations == []
        assert ooda_loop.orientations == []
        assert ooda_loop.decisions == []
        assert ooda_loop.actions == []
    
    def test_observe(self, ooda_loop, sample_dataframe):
        """Test observe phase captures data correctly"""
        observation = ooda_loop.observe(sample_dataframe)
        
        assert 'timestamp' in observation
        assert 'data_shape' in observation
        assert observation['data_shape'] == sample_dataframe.shape
        assert 'columns' in observation
        assert len(observation['columns']) == len(sample_dataframe.columns)
        assert len(ooda_loop.observations) == 1
    
    def test_orient(self, ooda_loop):
        """Test orient phase analyzes patterns correctly"""
        predictions = np.array(['positive', 'negative', 'neutral'])
        ground_truth = np.array(['positive', 'negative', 'positive'])
        
        orientation = ooda_loop.orient(predictions, ground_truth)
        
        assert 'accuracy' in orientation
        assert 'bias_indicators' in orientation
        assert 'confidence_distribution' in orientation
        assert 0 <= orientation['accuracy'] <= 1
        assert len(ooda_loop.orientations) == 1
    
    def test_decide(self, ooda_loop):
        """Test decide phase generates decisions correctly"""
        orientation = {'accuracy': 0.65}
        decision = ooda_loop.decide(orientation)
        
        assert 'severity' in decision
        assert 'recommended_actions' in decision
        assert 'priority' in decision
        assert decision['severity'] == 'high'
        assert len(ooda_loop.decisions) == 1
    
    def test_decide_medium_severity(self, ooda_loop):
        """Test decision with medium accuracy"""
        orientation = {'accuracy': 0.75}
        decision = ooda_loop.decide(orientation)
        
        assert decision['severity'] == 'medium'
        assert decision['priority'] == 2
    
    def test_decide_low_severity(self, ooda_loop):
        """Test decision with high accuracy"""
        orientation = {'accuracy': 0.90}
        decision = ooda_loop.decide(orientation)
        
        assert decision['severity'] == 'low'
        assert decision['priority'] == 3
    
    def test_act(self, ooda_loop):
        """Test act phase executes actions correctly"""
        decision = {
            'severity': 'high',
            'recommended_actions': ['action1', 'action2'],
            'priority': 1
        }
        action = ooda_loop.act(decision)
        
        assert 'executed' in action
        assert 'actions_taken' in action
        assert 'timestamp' in action
        assert action['executed'] is True
        assert len(ooda_loop.actions) == 1


# ============================================================================
# Test Data Generation
# ============================================================================

class TestDataGeneration:
    """Test suite for data generation functions"""
    
    def test_generate_sample_data_structure(self):
        """Test generated data has correct structure"""
        df = generate_sample_data()
        
        assert isinstance(df, pd.DataFrame)
        assert 'text' in df.columns
        assert 'sentiment' in df.columns
        assert 'region' in df.columns
        assert 'gender' in df.columns
        assert 'age_group' in df.columns
    
    def test_generate_sample_data_size(self):
        """Test generated data has correct size"""
        df = generate_sample_data()
        assert len(df) == 300  # 15 samples * 20 repetitions
    
    def test_generate_sample_data_sentiments(self):
        """Test generated data contains all sentiment categories"""
        df = generate_sample_data()
        sentiments = df['sentiment'].unique()
        
        assert 'positive' in sentiments
        assert 'negative' in sentiments
        assert 'neutral' in sentiments
    
    def test_generate_sample_data_no_nulls(self):
        """Test generated data has no missing values"""
        df = generate_sample_data()
        assert df.isnull().sum().sum() == 0


# ============================================================================
# Test Prediction Functions
# ============================================================================

class TestPrediction:
    """Test suite for sentiment prediction"""
    
    def test_predict_sentiment_with_none_model(self):
        """Test prediction works with no model (dummy mode)"""
        texts = ['test1', 'test2', 'test3']
        predictions = predict_sentiment(texts, None, None)
        
        assert len(predictions) == len(texts)
        assert all(p in ['positive', 'negative', 'neutral'] for p in predictions)
    
    @patch('pipeline.torch')
    def test_predict_sentiment_with_model(self, mock_torch, mock_model, mock_tokenizer):
        """Test prediction with actual model"""
        # Setup mocks
        mock_tokenizer.return_value = {'input_ids': Mock(), 'attention_mask': Mock()}
        mock_model.return_value.logits = Mock()
        mock_torch.nn.functional.softmax.return_value = Mock()
        mock_torch.argmax.return_value.item.return_value = 0
        
        texts = ['test sentence']
        predictions = predict_sentiment(texts, mock_model, mock_tokenizer)
        
        assert len(predictions) == len(texts)


# ============================================================================
# Test Bias Analysis
# ============================================================================

class TestBiasAnalysis:
    """Test suite for bias analysis functions"""
    
    def test_analyze_bias_structure(self, sample_dataframe):
        """Test bias analysis returns correct structure"""
        predictions = ['positive', 'negative', 'neutral']
        results = analyze_bias(sample_dataframe, predictions)
        
        assert 'region' in results
        assert 'gender' in results
        assert 'age_group' in results
        assert 'fairness' in results
    
    def test_calculate_fairness_metrics(self, sample_dataframe):
        """Test fairness metrics calculation"""
        sample_dataframe['prediction'] = ['positive', 'negative', 'neutral']
        metrics = calculate_fairness_metrics(sample_dataframe)
        
        assert 'region_demographic_parity' in metrics
        assert 'gender_demographic_parity' in metrics
        assert 'age_group_demographic_parity' in metrics
        assert 'overall_fairness' in metrics
        assert all(isinstance(v, (int, float)) for v in metrics.values())
    
    def test_fairness_metrics_range(self, sample_dataframe):
        """Test fairness metrics are within valid range"""
        sample_dataframe['prediction'] = ['positive'] * len(sample_dataframe)
        metrics = calculate_fairness_metrics(sample_dataframe)
        
        # Demographic parity should be 0 when all predictions are same
        assert metrics['region_demographic_parity'] == 0
        assert metrics['overall_fairness'] == 1.0


# ============================================================================
# Test Edge Cases
# ============================================================================

class TestEdgeCases:
    """Test suite for edge cases and error handling"""
    
    def test_empty_dataframe(self):
        """Test handling of empty DataFrame"""
        df = pd.DataFrame()
        ooda = OODALoop()
        
        with pytest.raises((KeyError, AttributeError)):
            ooda.observe(df)
    
    def test_single_row_dataframe(self):
        """Test handling of single-row DataFrame"""
        df = pd.DataFrame({
            'text': ['test'],
            'sentiment': ['positive'],
            'region': ['Gulf'],
            'gender': ['male'],
            'age_group': ['18-25']
        })
        
        predictions = ['positive']
        results = analyze_bias(df, predictions)
        
        assert results is not None
        assert 'fairness' in results
    
    def test_mismatched_prediction_length(self, sample_dataframe):
        """Test error when predictions don't match data length"""
        predictions = ['positive', 'negative']  # Only 2, but df has 3
        
        # Should handle gracefully or raise appropriate error
        try:
            results = analyze_bias(sample_dataframe, predictions)
            # If it doesn't raise, ensure it handles it somehow
            assert results is not None
        except (ValueError, IndexError):
            # Expected behavior
            pass


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """Integration tests for full pipeline"""
    
    def test_full_ooda_cycle(self, sample_dataframe):
        """Test complete OODA cycle"""
        ooda = OODALoop()
        
        # Observe
        observation = ooda.observe(sample_dataframe)
        assert observation is not None
        
        # Orient
        predictions = np.array(['positive', 'negative', 'neutral'])
        ground_truth = np.array(['positive', 'negative', 'positive'])
        orientation = ooda.orient(predictions, ground_truth)
        assert orientation is not None
        
        # Decide
        decision = ooda.decide(orientation)
        assert decision is not None
        
        # Act
        action = ooda.act(decision)
        assert action is not None
        
        # Verify all phases recorded
        assert len(ooda.observations) == 1
        assert len(ooda.orientations) == 1
        assert len(ooda.decisions) == 1
        assert len(ooda.actions) == 1
    
    def test_data_generation_and_analysis(self):
        """Test data generation followed by bias analysis"""
        # Generate data
        df = generate_sample_data()
        assert df is not None
        
        # Predict
        predictions = predict_sentiment(df['text'].tolist(), None, None)
        assert len(predictions) == len(df)
        
        # Analyze bias
        results = analyze_bias(df, predictions)
        assert results is not None
        assert 'fairness' in results


# ============================================================================
# Performance Tests
# ============================================================================

class TestPerformance:
    """Test suite for performance requirements"""
    
    def test_prediction_speed(self):
        """Test prediction completes in reasonable time"""
        import time
        
        texts = ['test'] * 100
        start = time.time()
        predictions = predict_sentiment(texts, None, None)
        duration = time.time() - start
        
        assert duration < 1.0  # Should complete in under 1 second
        assert len(predictions) == 100
    
    def test_bias_analysis_speed(self):
        """Test bias analysis completes in reasonable time"""
        import time
        
        df = generate_sample_data()
        predictions = ['positive'] * len(df)
        
        start = time.time()
        results = analyze_bias(df, predictions)
        duration = time.time() - start
        
        assert duration < 2.0  # Should complete in under 2 seconds
        assert results is not None


# ============================================================================
# Parametrized Tests
# ============================================================================

@pytest.mark.parametrize("accuracy,expected_severity", [
    (0.5, 'high'),
    (0.65, 'high'),
    (0.75, 'medium'),
    (0.80, 'medium'),
    (0.90, 'low'),
    (0.95, 'low'),
])
def test_severity_levels(accuracy, expected_severity):
    """Test severity levels for different accuracy values"""
    ooda = OODALoop()
    orientation = {'accuracy': accuracy}
    decision = ooda.decide(orientation)
    
    assert decision['severity'] == expected_severity


@pytest.mark.parametrize("text_input", [
    "الخدمة ممتازة",  # Arabic
    "خدمات عالی",  # Persian
    "Great service",  # English
    "👍😊",  # Emoji
    "",  # Empty
])
def test_prediction_with_various_inputs(text_input):
    """Test prediction handles various text inputs"""
    predictions = predict_sentiment([text_input], None, None)
    assert len(predictions) == 1
    assert predictions[0] in ['positive', 'negative', 'neutral']


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--cov=pipeline', '--cov-report=html'])