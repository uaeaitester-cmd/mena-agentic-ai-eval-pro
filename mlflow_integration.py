#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MLflow Integration for MENA Bias Evaluation Pipeline
Track experiments, models, and metrics with MLflow
"""

import mlflow
import mlflow.pytorch
from mlflow.tracking import MlflowClient
from typing import Dict, Any, Optional, List
import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class MLflowExperimentTracker:
    """
    MLflow integration for experiment tracking
    
    Features:
    - Automatic experiment logging
    - Model versioning
    - Metric tracking
    - Artifact management
    - Comparison across runs
    """
    
    def __init__(
        self,
        experiment_name: str = "MENA_Bias_Evaluation",
        tracking_uri: Optional[str] = None,
        artifact_location: Optional[str] = None
    ):
        """
        Initialize MLflow tracker
        
        Args:
            experiment_name: Name of the experiment
            tracking_uri: MLflow tracking server URI (None for local)
            artifact_location: Location to store artifacts
        """
        
        # Set tracking URI
        if tracking_uri:
            mlflow.set_tracking_uri(tracking_uri)
        
        # Set or create experiment
        try:
            experiment = mlflow.get_experiment_by_name(experiment_name)
            if experiment is None:
                experiment_id = mlflow.create_experiment(
                    experiment_name,
                    artifact_location=artifact_location
                )
                logger.info(f"Created new experiment: {experiment_name}")
            else:
                experiment_id = experiment.experiment_id
                logger.info(f"Using existing experiment: {experiment_name}")
        except Exception as e:
            logger.error(f"Error setting up experiment: {e}")
            experiment_id = mlflow.create_experiment(experiment_name)
        
        self.experiment_name = experiment_name
        self.experiment_id = experiment_id
        self.client = MlflowClient()
        
        logger.info("✅ MLflow Experiment Tracker initialized")
    
    def start_run(
        self,
        run_name: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None
    ) -> mlflow.ActiveRun:
        """
        Start a new MLflow run
        
        Args:
            run_name: Name for the run
            tags: Dictionary of tags
        
        Returns:
            Active run context
        """
        
        if run_name is None:
            run_name = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Default tags
        default_tags = {
            'pipeline_version': '1.0.0',
            'framework': 'MENA_Bias_Evaluation'
        }
        
        if tags:
            default_tags.update(tags)
        
        run = mlflow.start_run(
            experiment_id=self.experiment_id,
            run_name=run_name,
            tags=default_tags
        )
        
        logger.info(f"Started run: {run_name} (ID: {run.info.run_id})")
        
        return run
    
    def log_parameters(self, params: Dict[str, Any]):
        """Log parameters to current run"""
        for key, value in params.items():
            mlflow.log_param(key, value)
        
        logger.debug(f"Logged {len(params)} parameters")
    
    def log_metrics(
        self,
        metrics: Dict[str, float],
        step: Optional[int] = None
    ):
        """
        Log metrics to current run
        
        Args:
            metrics: Dictionary of metric_name -> value
            step: Optional step number for time-series metrics
        """
        for key, value in metrics.items():
            mlflow.log_metric(key, value, step=step)
        
        logger.debug(f"Logged {len(metrics)} metrics")
    
    def log_model(
        self,
        model: Any,
        artifact_path: str = "model",
        registered_model_name: Optional[str] = None
    ):
        """
        Log PyTorch model
        
        Args:
            model: PyTorch model to log
            artifact_path: Path within the run's artifact directory
            registered_model_name: Name for model registry
        """
        try:
            mlflow.pytorch.log_model(
                model,
                artifact_path=artifact_path,
                registered_model_name=registered_model_name
            )
            logger.info(f"Model logged to: {artifact_path}")
        except Exception as e:
            logger.error(f"Failed to log model: {e}")
    
    def log_artifact(self, local_path: str, artifact_path: Optional[str] = None):
        """
        Log a file or directory as an artifact
        
        Args:
            local_path: Path to local file or directory
            artifact_path: Path within the run's artifact directory
        """
        try:
            mlflow.log_artifact(local_path, artifact_path)
            logger.debug(f"Artifact logged: {local_path}")
        except Exception as e:
            logger.error(f"Failed to log artifact: {e}")
    
    def log_dataframe(
        self,
        df: pd.DataFrame,
        filename: str = "data.csv",
        artifact_path: Optional[str] = None
    ):
        """
        Log a DataFrame as an artifact
        
        Args:
            df: DataFrame to log
            filename: Name for the saved file
            artifact_path: Path within the run's artifact directory
        """
        try:
            temp_path = Path(f"/tmp/{filename}")
            df.to_csv(temp_path, index=False)
            mlflow.log_artifact(str(temp_path), artifact_path)
            temp_path.unlink()  # Clean up
            logger.debug(f"DataFrame logged: {filename}")
        except Exception as e:
            logger.error(f"Failed to log DataFrame: {e}")
    
    def log_figure(
        self,
        figure,
        filename: str = "plot.png",
        artifact_path: Optional[str] = None
    ):
        """
        Log a matplotlib figure
        
        Args:
            figure: Matplotlib figure object
            filename: Name for the saved file
            artifact_path: Path within the run's artifact directory
        """
        try:
            temp_path = Path(f"/tmp/{filename}")
            figure.savefig(temp_path, dpi=300, bbox_inches='tight')
            mlflow.log_artifact(str(temp_path), artifact_path)
            temp_path.unlink()
            logger.debug(f"Figure logged: {filename}")
        except Exception as e:
            logger.error(f"Failed to log figure: {e}")
    
    def log_bias_results(self, bias_results: Dict[str, Any]):
        """
        Log bias analysis results
        
        Args:
            bias_results: Dictionary containing bias analysis results
        """
        # Log fairness metrics
        if 'fairness' in bias_results:
            fairness_metrics = bias_results['fairness']
            for metric_name, value in fairness_metrics.items():
                mlflow.log_metric(f"fairness_{metric_name}", value)
        
        # Log as JSON artifact
        try:
            temp_path = Path("/tmp/bias_results.json")
            with open(temp_path, 'w') as f:
                json.dump(bias_results, f, indent=2)
            mlflow.log_artifact(str(temp_path), "bias_analysis")
            temp_path.unlink()
        except Exception as e:
            logger.error(f"Failed to log bias results: {e}")
    
    def end_run(self, status: str = "FINISHED"):
        """
        End the current run
        
        Args:
            status: Run status (FINISHED, FAILED, KILLED)
        """
        mlflow.end_run(status=status)
        logger.info(f"Run ended with status: {status}")
    
    def compare_runs(
        self,
        run_ids: List[str],
        metrics: List[str]
    ) -> pd.DataFrame:
        """
        Compare multiple runs
        
        Args:
            run_ids: List of run IDs to compare
            metrics: List of metric names to compare
        
        Returns:
            DataFrame with comparison results
        """
        comparison_data = []
        
        for run_id in run_ids:
            run = self.client.get_run(run_id)
            
            row = {
                'run_id': run_id,
                'run_name': run.data.tags.get('mlflow.runName', 'N/A'),
                'start_time': datetime.fromtimestamp(run.info.start_time / 1000)
            }
            
            # Add requested metrics
            for metric in metrics:
                value = run.data.metrics.get(metric)
                row[metric] = value
            
            comparison_data.append(row)
        
        df = pd.DataFrame(comparison_data)
        logger.info(f"Compared {len(run_ids)} runs")
        
        return df
    
    def get_best_run(
        self,
        metric: str,
        ascending: bool = False
    ) -> Optional[str]:
        """
        Get the best run based on a metric
        
        Args:
            metric: Metric name to optimize
            ascending: True for minimization, False for maximization
        
        Returns:
            Run ID of the best run
        """
        runs = self.client.search_runs(
            experiment_ids=[self.experiment_id],
            order_by=[f"metrics.{metric} {'ASC' if ascending else 'DESC'}"],
            max_results=1
        )
        
        if runs:
            best_run = runs[0]
            logger.info(
                f"Best run: {best_run.info.run_id} "
                f"({metric}={best_run.data.metrics.get(metric)})"
            )
            return best_run.info.run_id
        
        return None
    
    def register_model(
        self,
        run_id: str,
        model_name: str,
        artifact_path: str = "model"
    ) -> str:
        """
        Register a model in MLflow Model Registry
        
        Args:
            run_id: Run ID containing the model
            model_name: Name for the registered model
            artifact_path: Path to model artifacts within the run
        
        Returns:
            Model version
        """
        try:
            model_uri = f"runs:/{run_id}/{artifact_path}"
            result = mlflow.register_model(model_uri, model_name)
            
            logger.info(
                f"Model registered: {model_name} "
                f"(version {result.version})"
            )
            
            return result.version
        except Exception as e:
            logger.error(f"Failed to register model: {e}")
            return None


# Context manager for convenient usage
class MLflowRun:
    """Context manager for MLflow runs"""
    
    def __init__(
        self,
        tracker: MLflowExperimentTracker,
        run_name: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None
    ):
        self.tracker = tracker
        self.run_name = run_name
        self.tags = tags
        self.run = None
    
    def __enter__(self):
        self.run = self.tracker.start_run(self.run_name, self.tags)
        return self.tracker
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.tracker.end_run(status="FAILED")
            logger.error(f"Run failed: {exc_val}")
        else:
            self.tracker.end_run(status="FINISHED")
        return False


# Example usage
if __name__ == "__main__":
    print("🔬 Testing MLflow Integration\n")
    
    # Initialize tracker
    tracker = MLflowExperimentTracker(
        experiment_name="Test_Experiment"
    )
    
    # Use context manager
    with MLflowRun(tracker, run_name="test_run_1", tags={'test': 'true'}):
        # Log parameters
        tracker.log_parameters({
            'model': 'CAMeLBERT',
            'batch_size': 32,
            'learning_rate': 0.001
        })
        
        # Log metrics
        tracker.log_metrics({
            'accuracy': 0.85,
            'f1_score': 0.83,
            'bias_score': 0.12
        })
        
        # Log bias results
        bias_results = {
            'fairness': {
                'demographic_parity': 0.08,
                'equalized_odds': 0.12
            }
        }
        tracker.log_bias_results(bias_results)
        
        print("✅ Logged parameters, metrics, and artifacts")
    
    print("\n✅ Test completed!")
    print(f"View results: mlflow ui --backend-store-uri ./mlruns")