#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom Bias Metrics Designer for MENA Bias Evaluation Pipeline
Define and compute custom fairness and bias metrics
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Any, Callable, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


@dataclass
class MetricResult:
    """Result of a metric computation"""
    metric_name: str
    value: float
    interpretation: str
    threshold: Optional[float] = None
    passed: Optional[bool] = None
    details: Optional[Dict[str, Any]] = None


class BiasMetric(ABC):
    """Abstract base class for bias metrics"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def compute(
        self,
        predictions: np.ndarray,
        ground_truth: np.ndarray,
        sensitive_attribute: np.ndarray
    ) -> MetricResult:
        """Compute the metric"""
        pass


class DemographicParity(BiasMetric):
    """
    Demographic Parity (Statistical Parity)
    Measures if positive predictions are equally distributed across groups
    """
    
    def __init__(self, threshold: float = 0.1):
        super().__init__(
            name="Demographic Parity",
            description="Difference in positive prediction rates between groups"
        )
        self.threshold = threshold
    
    def compute(
        self,
        predictions: np.ndarray,
        ground_truth: np.ndarray,
        sensitive_attribute: np.ndarray
    ) -> MetricResult:
        """Compute demographic parity difference"""
        
        unique_groups = np.unique(sensitive_attribute)
        positive_rates = []
        
        for group in unique_groups:
            mask = sensitive_attribute == group
            if mask.sum() > 0:
                pos_rate = (predictions[mask] == 'positive').mean()
                positive_rates.append(pos_rate)
        
        if len(positive_rates) < 2:
            return MetricResult(
                metric_name=self.name,
                value=0.0,
                interpretation="Not enough groups to compute",
                threshold=self.threshold,
                passed=True
            )
        
        dpd = max(positive_rates) - min(positive_rates)
        passed = dpd <= self.threshold
        
        interpretation = (
            f"{'✅ Fair' if passed else '⚠️ Biased'}: "
            f"Max difference of {dpd:.3f} between groups "
            f"({'within' if passed else 'exceeds'} threshold {self.threshold})"
        )
        
        return MetricResult(
            metric_name=self.name,
            value=dpd,
            interpretation=interpretation,
            threshold=self.threshold,
            passed=passed,
            details={
                'positive_rates': dict(zip(unique_groups, positive_rates))
            }
        )


class EqualizedOdds(BiasMetric):
    """
    Equalized Odds
    Measures if true positive and false positive rates are equal across groups
    """
    
    def __init__(self, threshold: float = 0.1):
        super().__init__(
            name="Equalized Odds",
            description="Difference in TPR and FPR between groups"
        )
        self.threshold = threshold
    
    def compute(
        self,
        predictions: np.ndarray,
        ground_truth: np.ndarray,
        sensitive_attribute: np.ndarray
    ) -> MetricResult:
        """Compute equalized odds difference"""
        
        unique_groups = np.unique(sensitive_attribute)
        tpr_list = []
        fpr_list = []
        
        for group in unique_groups:
            mask = sensitive_attribute == group
            
            # True Positive Rate
            true_positive = ((predictions[mask] == 'positive') & 
                           (ground_truth[mask] == 'positive')).sum()
            actual_positive = (ground_truth[mask] == 'positive').sum()
            tpr = true_positive / actual_positive if actual_positive > 0 else 0
            tpr_list.append(tpr)
            
            # False Positive Rate
            false_positive = ((predictions[mask] == 'positive') & 
                            (ground_truth[mask] != 'positive')).sum()
            actual_negative = (ground_truth[mask] != 'positive').sum()
            fpr = false_positive / actual_negative if actual_negative > 0 else 0
            fpr_list.append(fpr)
        
        if len(tpr_list) < 2:
            return MetricResult(
                metric_name=self.name,
                value=0.0,
                interpretation="Not enough groups to compute",
                threshold=self.threshold,
                passed=True
            )
        
        tpr_diff = max(tpr_list) - min(tpr_list)
        fpr_diff = max(fpr_list) - min(fpr_list)
        eod = max(tpr_diff, fpr_diff)
        
        passed = eod <= self.threshold
        
        interpretation = (
            f"{'✅ Fair' if passed else '⚠️ Biased'}: "
            f"Max difference of {eod:.3f} "
            f"({'within' if passed else 'exceeds'} threshold {self.threshold})"
        )
        
        return MetricResult(
            metric_name=self.name,
            value=eod,
            interpretation=interpretation,
            threshold=self.threshold,
            passed=passed,
            details={
                'tpr_diff': tpr_diff,
                'fpr_diff': fpr_diff,
                'tpr_by_group': dict(zip(unique_groups, tpr_list)),
                'fpr_by_group': dict(zip(unique_groups, fpr_list))
            }
        )


class DisparateImpact(BiasMetric):
    """
    Disparate Impact Ratio
    Ratio of positive rates between protected and unprotected groups
    """
    
    def __init__(self, threshold: float = 0.8):
        super().__init__(
            name="Disparate Impact",
            description="Ratio of positive rates (should be >= 0.8)"
        )
        self.threshold = threshold
    
    def compute(
        self,
        predictions: np.ndarray,
        ground_truth: np.ndarray,
        sensitive_attribute: np.ndarray
    ) -> MetricResult:
        """Compute disparate impact ratio"""
        
        unique_groups = np.unique(sensitive_attribute)
        positive_rates = []
        
        for group in unique_groups:
            mask = sensitive_attribute == group
            if mask.sum() > 0:
                pos_rate = (predictions[mask] == 'positive').mean()
                positive_rates.append(pos_rate)
        
        if len(positive_rates) < 2 or min(positive_rates) == 0:
            return MetricResult(
                metric_name=self.name,
                value=1.0,
                interpretation="Cannot compute (zero rates)",
                threshold=self.threshold,
                passed=True
            )
        
        di_ratio = min(positive_rates) / max(positive_rates)
        passed = di_ratio >= self.threshold
        
        interpretation = (
            f"{'✅ Fair' if passed else '⚠️ Biased'}: "
            f"Ratio of {di_ratio:.3f} "
            f"({'meets' if passed else 'below'} threshold {self.threshold})"
        )
        
        return MetricResult(
            metric_name=self.name,
            value=di_ratio,
            interpretation=interpretation,
            threshold=self.threshold,
            passed=passed,
            details={
                'positive_rates': dict(zip(unique_groups, positive_rates))
            }
        )


class PredictiveParityDifference(BiasMetric):
    """
    Predictive Parity Difference
    Difference in precision (PPV) between groups
    """
    
    def __init__(self, threshold: float = 0.1):
        super().__init__(
            name="Predictive Parity",
            description="Difference in precision between groups"
        )
        self.threshold = threshold
    
    def compute(
        self,
        predictions: np.ndarray,
        ground_truth: np.ndarray,
        sensitive_attribute: np.ndarray
    ) -> MetricResult:
        """Compute predictive parity difference"""
        
        unique_groups = np.unique(sensitive_attribute)
        precision_list = []
        
        for group in unique_groups:
            mask = sensitive_attribute == group
            
            # Precision (PPV)
            true_positive = ((predictions[mask] == 'positive') & 
                           (ground_truth[mask] == 'positive')).sum()
            predicted_positive = (predictions[mask] == 'positive').sum()
            precision = true_positive / predicted_positive if predicted_positive > 0 else 0
            precision_list.append(precision)
        
        if len(precision_list) < 2:
            return MetricResult(
                metric_name=self.name,
                value=0.0,
                interpretation="Not enough groups to compute",
                threshold=self.threshold,
                passed=True
            )
        
        ppd = max(precision_list) - min(precision_list)
        passed = ppd <= self.threshold
        
        interpretation = (
            f"{'✅ Fair' if passed else '⚠️ Biased'}: "
            f"Precision difference of {ppd:.3f} "
            f"({'within' if passed else 'exceeds'} threshold {self.threshold})"
        )
        
        return MetricResult(
            metric_name=self.name,
            value=ppd,
            interpretation=interpretation,
            threshold=self.threshold,
            passed=passed,
            details={
                'precision_by_group': dict(zip(unique_groups, precision_list))
            }
        )


class CustomMetricRegistry:
    """Registry for custom bias metrics"""
    
    def __init__(self):
        self.metrics: Dict[str, BiasMetric] = {}
        
        # Register default metrics
        self.register_default_metrics()
    
    def register_default_metrics(self):
        """Register standard fairness metrics"""
        self.register(DemographicParity())
        self.register(EqualizedOdds())
        self.register(DisparateImpact())
        self.register(PredictiveParityDifference())
        
        logger.info(f"✅ Registered {len(self.metrics)} default metrics")
    
    def register(self, metric: BiasMetric):
        """Register a new metric"""
        self.metrics[metric.name] = metric
        logger.info(f"Registered metric: {metric.name}")
    
    def compute_all(
        self,
        predictions: np.ndarray,
        ground_truth: np.ndarray,
        sensitive_attribute: np.ndarray
    ) -> List[MetricResult]:
        """Compute all registered metrics"""
        results = []
        
        for metric in self.metrics.values():
            try:
                result = metric.compute(predictions, ground_truth, sensitive_attribute)
                results.append(result)
            except Exception as e:
                logger.error(f"Error computing {metric.name}: {e}")
        
        return results
    
    def get_summary(self, results: List[MetricResult]) -> Dict[str, Any]:
        """Get summary of all metric results"""
        passed = sum(1 for r in results if r.passed)
        failed = sum(1 for r in results if r.passed is False)
        
        return {
            'total_metrics': len(results),
            'passed': passed,
            'failed': failed,
            'pass_rate': passed / len(results) if results else 0,
            'results': [
                {
                    'metric': r.metric_name,
                    'value': r.value,
                    'passed': r.passed,
                    'interpretation': r.interpretation
                }
                for r in results
            ]
        }


class BiasMetricsEvaluator:
    """High-level evaluator for bias metrics"""
    
    def __init__(self):
        self.registry = CustomMetricRegistry()
    
    def evaluate_dataframe(
        self,
        df: pd.DataFrame,
        prediction_col: str = 'prediction',
        ground_truth_col: str = 'sentiment',
        sensitive_cols: List[str] = ['region', 'gender', 'age_group']
    ) -> Dict[str, Any]:
        """
        Evaluate bias metrics on a DataFrame
        
        Args:
            df: DataFrame with predictions and ground truth
            prediction_col: Column name for predictions
            ground_truth_col: Column name for ground truth
            sensitive_cols: List of sensitive attribute columns
        
        Returns:
            Dictionary with results for each sensitive attribute
        """
        
        results_by_attribute = {}
        
        for sensitive_col in sensitive_cols:
            if sensitive_col not in df.columns:
                logger.warning(f"Column {sensitive_col} not found, skipping")
                continue
            
            logger.info(f"Evaluating bias for: {sensitive_col}")
            
            # Compute all metrics
            metric_results = self.registry.compute_all(
                predictions=df[prediction_col].values,
                ground_truth=df[ground_truth_col].values,
                sensitive_attribute=df[sensitive_col].values
            )
            
            # Get summary
            summary = self.registry.get_summary(metric_results)
            
            results_by_attribute[sensitive_col] = {
                'summary': summary,
                'details': metric_results
            }
        
        return results_by_attribute
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate text report from results"""
        lines = []
        lines.append("=" * 80)
        lines.append("CUSTOM BIAS METRICS EVALUATION REPORT")
        lines.append("=" * 80)
        lines.append("")
        
        for attr, attr_results in results.items():
            lines.append(f"SENSITIVE ATTRIBUTE: {attr.upper()}")
            lines.append("-" * 80)
            
            summary = attr_results['summary']
            lines.append(f"Total Metrics: {summary['total_metrics']}")
            lines.append(f"Passed: {summary['passed']} | Failed: {summary['failed']}")
            lines.append(f"Pass Rate: {summary['pass_rate']:.1%}")
            lines.append("")
            
            lines.append("Metric Results:")
            for result_dict in summary['results']:
                status = "✅" if result_dict['passed'] else "❌"
                lines.append(
                    f"  {status} {result_dict['metric']}: "
                    f"{result_dict['value']:.3f} - {result_dict['interpretation']}"
                )
            
            lines.append("")
        
        lines.append("=" * 80)
        
        return "\n".join(lines)


# Example usage
if __name__ == "__main__":
    print("📏 Testing Custom Bias Metrics\n")
    
    # Create sample data
    np.random.seed(42)
    n = 1000
    
    df = pd.DataFrame({
        'text': [f'text_{i}' for i in range(n)],
        'sentiment': np.random.choice(['positive', 'negative', 'neutral'], n),
        'prediction': np.random.choice(['positive', 'negative', 'neutral'], n),
        'region': np.random.choice(['Gulf', 'Levant', 'Egypt'], n),
        'gender': np.random.choice(['male', 'female'], n),
        'age_group': np.random.choice(['18-25', '26-35', '36-45'], n)
    })
    
    # Evaluate
    evaluator = BiasMetricsEvaluator()
    results = evaluator.evaluate_dataframe(df)
    
    # Generate report
    report = evaluator.generate_report(results)
    print(report)
    
    print("\n✅ Test completed!")