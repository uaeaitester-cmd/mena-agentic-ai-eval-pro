#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Model Comparison Framework for MENA Bias Evaluation Pipeline
Compare multiple models across various metrics
"""

import time
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging

from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
    classification_report
)

logger = logging.getLogger(__name__)


@dataclass
class ModelMetrics:
    """Metrics for a single model"""
    model_name: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    inference_time: float  # seconds per sample
    memory_usage: float  # MB
    bias_score: float  # 0-1, lower is better
    fairness_score: float  # 0-1, higher is better
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


class ModelComparator:
    """
    Framework for comparing multiple models
    
    Features:
    - Performance metrics comparison
    - Bias analysis comparison
    - Inference speed benchmarking
    - Memory usage profiling
    - Visual comparison reports
    """
    
    def __init__(self, output_dir: str = "comparison_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.models = {}  # model_name -> (model, tokenizer)
        self.results = {}  # model_name -> ModelMetrics
        
        logger.info("✅ Model Comparator initialized")
    
    def add_model(
        self,
        name: str,
        model: Any,
        tokenizer: Any,
        description: str = ""
    ):
        """
        Add a model to comparison
        
        Args:
            name: Model identifier
            model: Trained model
            tokenizer: Tokenizer
            description: Optional description
        """
        self.models[name] = {
            'model': model,
            'tokenizer': tokenizer,
            'description': description
        }
        logger.info(f"Added model: {name}")
    
    def predict_batch(
        self,
        model_name: str,
        texts: List[str]
    ) -> List[str]:
        """Make predictions for a batch of texts"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")
        
        model_info = self.models[model_name]
        model = model_info['model']
        tokenizer = model_info['tokenizer']
        
        # Simple prediction logic (customize based on your models)
        predictions = []
        
        for text in texts:
            # This is a placeholder - replace with actual inference
            pred = np.random.choice(['positive', 'negative', 'neutral'])
            predictions.append(pred)
        
        return predictions
    
    def evaluate_model(
        self,
        model_name: str,
        test_data: pd.DataFrame,
        text_column: str = 'text',
        label_column: str = 'sentiment'
    ) -> ModelMetrics:
        """
        Evaluate a single model
        
        Args:
            model_name: Name of model to evaluate
            test_data: Test DataFrame
            text_column: Column name for text
            label_column: Column name for labels
        
        Returns:
            ModelMetrics object
        """
        logger.info(f"Evaluating model: {model_name}")
        
        # Extract data
        texts = test_data[text_column].tolist()
        true_labels = test_data[label_column].tolist()
        
        # Measure inference time
        start_time = time.time()
        predictions = self.predict_batch(model_name, texts)
        inference_time = (time.time() - start_time) / len(texts)
        
        # Calculate metrics
        accuracy = accuracy_score(true_labels, predictions)
        precision, recall, f1, _ = precision_recall_fscore_support(
            true_labels,
            predictions,
            average='weighted',
            zero_division=0
        )
        
        # Calculate bias score (simplified)
        bias_score = self._calculate_bias_score(test_data, predictions)
        
        # Calculate fairness score
        fairness_score = 1.0 - bias_score
        
        # Memory usage (placeholder)
        memory_usage = 0.0  # Would need actual memory profiling
        
        metrics = ModelMetrics(
            model_name=model_name,
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1,
            inference_time=inference_time,
            memory_usage=memory_usage,
            bias_score=bias_score,
            fairness_score=fairness_score
        )
        
        self.results[model_name] = metrics
        logger.info(f"✅ {model_name} - Accuracy: {accuracy:.3f}, F1: {f1:.3f}")
        
        return metrics
    
    def _calculate_bias_score(
        self,
        data: pd.DataFrame,
        predictions: List[str]
    ) -> float:
        """Calculate bias score across demographics"""
        data = data.copy()
        data['prediction'] = predictions
        
        bias_scores = []
        
        # Check bias across demographics
        for demo_col in ['region', 'gender', 'age_group']:
            if demo_col not in data.columns:
                continue
            
            # Calculate demographic parity
            positive_rates = data.groupby(demo_col)['prediction'].apply(
                lambda x: (x == 'positive').mean()
            )
            
            if len(positive_rates) > 1:
                dpd = positive_rates.max() - positive_rates.min()
                bias_scores.append(dpd)
        
        return np.mean(bias_scores) if bias_scores else 0.0
    
    def compare_all(
        self,
        test_data: pd.DataFrame,
        text_column: str = 'text',
        label_column: str = 'sentiment'
    ) -> pd.DataFrame:
        """
        Compare all added models
        
        Args:
            test_data: Test DataFrame
            text_column: Column name for text
            label_column: Column name for labels
        
        Returns:
            Comparison DataFrame
        """
        logger.info(f"Comparing {len(self.models)} models...")
        
        # Evaluate all models
        for model_name in self.models.keys():
            self.evaluate_model(model_name, test_data, text_column, label_column)
        
        # Create comparison DataFrame
        comparison_df = pd.DataFrame([
            metrics.to_dict() for metrics in self.results.values()
        ])
        
        # Save to CSV
        output_path = self.output_dir / "comparison_results.csv"
        comparison_df.to_csv(output_path, index=False)
        logger.info(f"💾 Results saved to {output_path}")
        
        return comparison_df
    
    def generate_comparison_report(self) -> str:
        """Generate comprehensive comparison report"""
        if not self.results:
            raise ValueError("No results available. Run compare_all() first.")
        
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("MODEL COMPARISON REPORT")
        report_lines.append("=" * 80)
        report_lines.append("")
        
        # Summary table
        df = pd.DataFrame([m.to_dict() for m in self.results.values()])
        report_lines.append("PERFORMANCE METRICS:")
        report_lines.append("")
        report_lines.append(df.to_string(index=False))
        report_lines.append("")
        
        # Best models
        report_lines.append("BEST MODELS:")
        report_lines.append(f"  Highest Accuracy: {df.loc[df['accuracy'].idxmax(), 'model_name']}")
        report_lines.append(f"  Highest F1 Score: {df.loc[df['f1_score'].idxmax(), 'model_name']}")
        report_lines.append(f"  Lowest Bias: {df.loc[df['bias_score'].idxmin(), 'model_name']}")
        report_lines.append(f"  Fastest Inference: {df.loc[df['inference_time'].idxmin(), 'model_name']}")
        report_lines.append("")
        
        # Rankings
        report_lines.append("OVERALL RANKINGS:")
        df['overall_score'] = (
            df['accuracy'] * 0.3 +
            df['f1_score'] * 0.3 +
            df['fairness_score'] * 0.2 +
            (1 - df['inference_time'] / df['inference_time'].max()) * 0.2
        )
        df_ranked = df.sort_values('overall_score', ascending=False)
        
        for i, row in df_ranked.iterrows():
            rank = df_ranked.index.get_loc(i) + 1
            report_lines.append(
                f"  {rank}. {row['model_name']} (Score: {row['overall_score']:.3f})"
            )
        
        report_lines.append("")
        report_lines.append("=" * 80)
        
        report = "\n".join(report_lines)
        
        # Save report
        report_path = self.output_dir / "comparison_report.txt"
        with open(report_path, 'w') as f:
            f.write(report)
        
        logger.info(f"📄 Report saved to {report_path}")
        
        return report
    
    def visualize_comparison(self):
        """Create visual comparison charts"""
        if not self.results:
            raise ValueError("No results available. Run compare_all() first.")
        
        df = pd.DataFrame([m.to_dict() for m in self.results.values()])
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Model Comparison Analysis', fontsize=16, fontweight='bold')
        
        # 1. Performance metrics
        ax1 = axes[0, 0]
        metrics_to_plot = ['accuracy', 'precision', 'recall', 'f1_score']
        df[['model_name'] + metrics_to_plot].set_index('model_name').plot(
            kind='bar',
            ax=ax1
        )
        ax1.set_title('Performance Metrics')
        ax1.set_ylabel('Score')
        ax1.set_ylim(0, 1)
        ax1.legend(loc='lower right')
        ax1.grid(axis='y', alpha=0.3)
        
        # 2. Bias vs Fairness
        ax2 = axes[0, 1]
        ax2.scatter(df['bias_score'], df['fairness_score'], s=100, alpha=0.6)
        for i, row in df.iterrows():
            ax2.annotate(
                row['model_name'],
                (row['bias_score'], row['fairness_score']),
                fontsize=8
            )
        ax2.set_xlabel('Bias Score (lower is better)')
        ax2.set_ylabel('Fairness Score (higher is better)')
        ax2.set_title('Bias vs Fairness')
        ax2.grid(alpha=0.3)
        
        # 3. Inference time
        ax3 = axes[1, 0]
        df[['model_name', 'inference_time']].set_index('model_name').plot(
            kind='barh',
            ax=ax3,
            legend=False
        )
        ax3.set_title('Inference Time (seconds per sample)')
        ax3.set_xlabel('Time (s)')
        ax3.grid(axis='x', alpha=0.3)
        
        # 4. Overall score radar
        ax4 = axes[1, 1]
        
        # Normalize metrics for radar chart
        metrics_normalized = df.copy()
        for col in ['accuracy', 'f1_score', 'fairness_score']:
            metrics_normalized[col] = df[col]
        
        # Create radar chart (simplified as bar)
        top_3 = df.nlargest(3, 'f1_score')
        top_3[['model_name', 'accuracy', 'f1_score', 'fairness_score']].set_index('model_name').plot(
            kind='bar',
            ax=ax4
        )
        ax4.set_title('Top 3 Models - Key Metrics')
        ax4.set_ylabel('Score')
        ax4.set_ylim(0, 1)
        ax4.legend(loc='lower right')
        ax4.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        # Save figure
        output_path = self.output_dir / "comparison_visualization.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"📊 Visualization saved to {output_path}")
    
    def export_results(self, format: str = 'json'):
        """
        Export results to various formats
        
        Args:
            format: 'json', 'csv', or 'excel'
        """
        if not self.results:
            raise ValueError("No results available")
        
        data = [m.to_dict() for m in self.results.values()]
        
        if format == 'json':
            output_path = self.output_dir / "comparison_results.json"
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)
        
        elif format == 'csv':
            output_path = self.output_dir / "comparison_results.csv"
            pd.DataFrame(data).to_csv(output_path, index=False)
        
        elif format == 'excel':
            output_path = self.output_dir / "comparison_results.xlsx"
            pd.DataFrame(data).to_excel(output_path, index=False)
        
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        logger.info(f"💾 Results exported to {output_path}")


# Example usage
if __name__ == "__main__":
    print("🔬 Testing Model Comparison Framework\n")
    
    # Create dummy test data
    test_data = pd.DataFrame({
        'text': ['test1', 'test2', 'test3'] * 100,
        'sentiment': ['positive', 'negative', 'neutral'] * 100,
        'region': ['Gulf', 'Levant', 'Egypt'] * 100,
        'gender': ['male', 'female', 'male'] * 100,
        'age_group': ['18-25', '26-35', '36-45'] * 100
    })
    
    # Initialize comparator
    comparator = ModelComparator()
    
    # Add dummy models
    comparator.add_model("Model_A", None, None, "Baseline model")
    comparator.add_model("Model_B", None, None, "Optimized model")
    comparator.add_model("Model_C", None, None, "Experimental model")
    
    # Compare
    results_df = comparator.compare_all(test_data)
    print("\n📊 Comparison Results:")
    print(results_df)
    
    # Generate report
    report = comparator.generate_comparison_report()
    print("\n" + report)
    
    # Visualize
    comparator.visualize_comparison()
    
    # Export
    comparator.export_results('json')
    comparator.export_results('excel')
    
    print("\n✅ Test completed!")