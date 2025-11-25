#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A/B Testing Framework for MENA Bias Evaluation Pipeline
Statistical comparison of models and bias mitigation strategies
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from scipy import stats
from scipy.stats import ttest_ind, chi2_contingency, mannwhitneyu
import logging

logger = logging.getLogger(__name__)


@dataclass
class ABTestResult:
    """Result of an A/B test"""
    test_name: str
    variant_a_mean: float
    variant_b_mean: float
    difference: float
    percent_change: float
    p_value: float
    is_significant: bool
    confidence_level: float
    recommendation: str
    effect_size: float


class ABTester:
    """
    A/B Testing framework for model comparison
    
    Features:
    - Statistical significance testing
    - Multiple comparison correction
    - Effect size calculation
    - Power analysis
    - Bayesian A/B testing
    """
    
    def __init__(self, alpha: float = 0.05, power: float = 0.8):
        """
        Initialize A/B tester
        
        Args:
            alpha: Significance level (default 0.05 for 95% confidence)
            power: Statistical power (default 0.8)
        """
        self.alpha = alpha
        self.power = power
        self.confidence_level = 1 - alpha
        
        logger.info(f"✅ A/B Tester initialized (α={alpha}, power={power})")
    
    def t_test(
        self,
        variant_a: np.ndarray,
        variant_b: np.ndarray,
        test_name: str = "T-Test"
    ) -> ABTestResult:
        """
        Perform independent t-test
        
        Args:
            variant_a: Metrics for variant A
            variant_b: Metrics for variant B
            test_name: Name of the test
        
        Returns:
            ABTestResult object
        """
        # Calculate statistics
        mean_a = np.mean(variant_a)
        mean_b = np.mean(variant_b)
        difference = mean_b - mean_a
        percent_change = (difference / mean_a * 100) if mean_a != 0 else 0
        
        # Perform t-test
        t_stat, p_value = ttest_ind(variant_a, variant_b)
        is_significant = p_value < self.alpha
        
        # Calculate effect size (Cohen's d)
        pooled_std = np.sqrt((np.var(variant_a) + np.var(variant_b)) / 2)
        effect_size = difference / pooled_std if pooled_std != 0 else 0
        
        # Recommendation
        if is_significant:
            if difference > 0:
                recommendation = f"✅ Variant B is significantly better ({percent_change:+.2f}%)"
            else:
                recommendation = f"⚠️ Variant A is significantly better ({percent_change:+.2f}%)"
        else:
            recommendation = "⚪ No significant difference detected"
        
        return ABTestResult(
            test_name=test_name,
            variant_a_mean=mean_a,
            variant_b_mean=mean_b,
            difference=difference,
            percent_change=percent_change,
            p_value=p_value,
            is_significant=is_significant,
            confidence_level=self.confidence_level,
            recommendation=recommendation,
            effect_size=effect_size
        )
    
    def mann_whitney_test(
        self,
        variant_a: np.ndarray,
        variant_b: np.ndarray,
        test_name: str = "Mann-Whitney U Test"
    ) -> ABTestResult:
        """
        Perform Mann-Whitney U test (non-parametric)
        
        Args:
            variant_a: Metrics for variant A
            variant_b: Metrics for variant B
            test_name: Name of the test
        
        Returns:
            ABTestResult object
        """
        mean_a = np.mean(variant_a)
        mean_b = np.mean(variant_b)
        difference = mean_b - mean_a
        percent_change = (difference / mean_a * 100) if mean_a != 0 else 0
        
        # Perform Mann-Whitney U test
        u_stat, p_value = mannwhitneyu(variant_a, variant_b, alternative='two-sided')
        is_significant = p_value < self.alpha
        
        # Effect size (rank-biserial correlation)
        n_a, n_b = len(variant_a), len(variant_b)
        effect_size = 1 - (2 * u_stat) / (n_a * n_b)
        
        # Recommendation
        if is_significant:
            if difference > 0:
                recommendation = f"✅ Variant B is significantly better ({percent_change:+.2f}%)"
            else:
                recommendation = f"⚠️ Variant A is significantly better ({percent_change:+.2f}%)"
        else:
            recommendation = "⚪ No significant difference detected"
        
        return ABTestResult(
            test_name=test_name,
            variant_a_mean=mean_a,
            variant_b_mean=mean_b,
            difference=difference,
            percent_change=percent_change,
            p_value=p_value,
            is_significant=is_significant,
            confidence_level=self.confidence_level,
            recommendation=recommendation,
            effect_size=effect_size
        )
    
    def chi_square_test(
        self,
        variant_a_counts: np.ndarray,
        variant_b_counts: np.ndarray,
        test_name: str = "Chi-Square Test"
    ) -> ABTestResult:
        """
        Perform chi-square test for categorical data
        
        Args:
            variant_a_counts: Category counts for variant A
            variant_b_counts: Category counts for variant B
            test_name: Name of the test
        
        Returns:
            ABTestResult object
        """
        # Create contingency table
        contingency_table = np.array([variant_a_counts, variant_b_counts])
        
        # Perform chi-square test
        chi2, p_value, dof, expected = chi2_contingency(contingency_table)
        is_significant = p_value < self.alpha
        
        # Calculate proportions
        total_a = variant_a_counts.sum()
        total_b = variant_b_counts.sum()
        prop_a = variant_a_counts / total_a if total_a > 0 else variant_a_counts
        prop_b = variant_b_counts / total_b if total_b > 0 else variant_b_counts
        
        mean_a = np.mean(prop_a)
        mean_b = np.mean(prop_b)
        difference = mean_b - mean_a
        percent_change = (difference / mean_a * 100) if mean_a != 0 else 0
        
        # Effect size (Cramér's V)
        n = contingency_table.sum()
        effect_size = np.sqrt(chi2 / (n * (min(contingency_table.shape) - 1)))
        
        # Recommendation
        if is_significant:
            recommendation = f"✅ Distributions are significantly different (χ²={chi2:.2f})"
        else:
            recommendation = "⚪ No significant difference in distributions"
        
        return ABTestResult(
            test_name=test_name,
            variant_a_mean=mean_a,
            variant_b_mean=mean_b,
            difference=difference,
            percent_change=percent_change,
            p_value=p_value,
            is_significant=is_significant,
            confidence_level=self.confidence_level,
            recommendation=recommendation,
            effect_size=effect_size
        )
    
    def calculate_sample_size(
        self,
        baseline_rate: float,
        minimum_detectable_effect: float,
        alpha: Optional[float] = None,
        power: Optional[float] = None
    ) -> int:
        """
        Calculate required sample size for A/B test
        
        Args:
            baseline_rate: Current conversion/success rate
            minimum_detectable_effect: Minimum effect to detect (e.g., 0.05 for 5%)
            alpha: Significance level (uses instance default if None)
            power: Statistical power (uses instance default if None)
        
        Returns:
            Required sample size per variant
        """
        alpha = alpha or self.alpha
        power = power or self.power
        
        # Z-scores
        z_alpha = stats.norm.ppf(1 - alpha / 2)
        z_beta = stats.norm.ppf(power)
        
        # Effect size
        p1 = baseline_rate
        p2 = baseline_rate * (1 + minimum_detectable_effect)
        
        # Sample size calculation
        pooled_p = (p1 + p2) / 2
        numerator = (z_alpha * np.sqrt(2 * pooled_p * (1 - pooled_p)) + 
                    z_beta * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
        denominator = (p2 - p1) ** 2
        
        sample_size = int(np.ceil(numerator / denominator))
        
        logger.info(f"Required sample size: {sample_size} per variant")
        
        return sample_size
    
    def bayesian_ab_test(
        self,
        variant_a_successes: int,
        variant_a_trials: int,
        variant_b_successes: int,
        variant_b_trials: int,
        prior_alpha: float = 1,
        prior_beta: float = 1
    ) -> Dict[str, float]:
        """
        Perform Bayesian A/B test
        
        Args:
            variant_a_successes: Number of successes in A
            variant_a_trials: Number of trials in A
            variant_b_successes: Number of successes in B
            variant_b_trials: Number of trials in B
            prior_alpha: Prior alpha for Beta distribution
            prior_beta: Prior beta for Beta distribution
        
        Returns:
            Dictionary with Bayesian results
        """
        # Posterior distributions
        posterior_a_alpha = prior_alpha + variant_a_successes
        posterior_a_beta = prior_beta + variant_a_trials - variant_a_successes
        
        posterior_b_alpha = prior_alpha + variant_b_successes
        posterior_b_beta = prior_beta + variant_b_trials - variant_b_successes
        
        # Sample from posteriors
        n_samples = 100000
        samples_a = np.random.beta(posterior_a_alpha, posterior_a_beta, n_samples)
        samples_b = np.random.beta(posterior_b_alpha, posterior_b_beta, n_samples)
        
        # Probability that B > A
        prob_b_better = np.mean(samples_b > samples_a)
        
        # Expected loss
        expected_loss_a = np.mean(np.maximum(samples_b - samples_a, 0))
        expected_loss_b = np.mean(np.maximum(samples_a - samples_b, 0))
        
        # Credible intervals
        credible_interval_a = np.percentile(samples_a, [2.5, 97.5])
        credible_interval_b = np.percentile(samples_b, [2.5, 97.5])
        
        return {
            'prob_b_better_than_a': prob_b_better,
            'prob_a_better_than_b': 1 - prob_b_better,
            'expected_loss_choosing_a': expected_loss_a,
            'expected_loss_choosing_b': expected_loss_b,
            'credible_interval_a': credible_interval_a.tolist(),
            'credible_interval_b': credible_interval_b.tolist(),
            'recommendation': (
                f"Choose B (prob={prob_b_better:.2%})" if prob_b_better > 0.95
                else f"Choose A (prob={1-prob_b_better:.2%})" if prob_b_better < 0.05
                else "Inconclusive - continue testing"
            )
        }
    
    def compare_multiple_variants(
        self,
        variants: Dict[str, np.ndarray],
        test_name: str = "ANOVA"
    ) -> Dict[str, any]:
        """
        Compare multiple variants using ANOVA
        
        Args:
            variants: Dictionary of variant_name -> metrics
            test_name: Name of the test
        
        Returns:
            Dictionary with ANOVA results
        """
        # Perform one-way ANOVA
        f_stat, p_value = stats.f_oneway(*variants.values())
        is_significant = p_value < self.alpha
        
        # Calculate means
        means = {name: np.mean(data) for name, data in variants.items()}
        
        # Find best variant
        best_variant = max(means, key=means.get)
        
        result = {
            'test_name': test_name,
            'f_statistic': f_stat,
            'p_value': p_value,
            'is_significant': is_significant,
            'means': means,
            'best_variant': best_variant,
            'recommendation': (
                f"✅ Significant difference found. Best: {best_variant}"
                if is_significant else
                "⚪ No significant difference between variants"
            )
        }
        
        return result


# Example usage
if __name__ == "__main__":
    print("🧪 Testing A/B Testing Framework\n")
    
    # Generate sample data
    np.random.seed(42)
    
    variant_a = np.random.normal(0.80, 0.05, 1000)  # Baseline: 80% accuracy
    variant_b = np.random.normal(0.85, 0.05, 1000)  # Treatment: 85% accuracy
    
    # Initialize tester
    tester = ABTester(alpha=0.05)
    
    # Perform t-test
    print("=" * 60)
    print("T-TEST RESULTS")
    print("=" * 60)
    result = tester.t_test(variant_a, variant_b, "Accuracy Comparison")
    print(f"Variant A Mean: {result.variant_a_mean:.4f}")
    print(f"Variant B Mean: {result.variant_b_mean:.4f}")
    print(f"Difference: {result.difference:+.4f} ({result.percent_change:+.2f}%)")
    print(f"P-value: {result.p_value:.6f}")
    print(f"Effect Size (Cohen's d): {result.effect_size:.3f}")
    print(f"Significant: {result.is_significant}")
    print(f"\n{result.recommendation}")
    
    print("\n" + "=" * 60)
    print("SAMPLE SIZE CALCULATION")
    print("=" * 60)
    sample_size = tester.calculate_sample_size(
        baseline_rate=0.80,
        minimum_detectable_effect=0.05
    )
    print(f"Required sample size per variant: {sample_size}")
    
    print("\n" + "=" * 60)
    print("BAYESIAN A/B TEST")
    print("=" * 60)
    bayesian_result = tester.bayesian_ab_test(
        variant_a_successes=800,
        variant_a_trials=1000,
        variant_b_successes=850,
        variant_b_trials=1000
    )
    print(f"P(B > A): {bayesian_result['prob_b_better_than_a']:.2%}")
    print(f"Expected Loss (A): {bayesian_result['expected_loss_choosing_a']:.4f}")
    print(f"Expected Loss (B): {bayesian_result['expected_loss_choosing_b']:.4f}")
    print(f"\n{bayesian_result['recommendation']}")
    
    print("\n✅ Test completed!")