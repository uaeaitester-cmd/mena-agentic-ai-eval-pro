#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced 3D Visualization Suite for MENA Bias Evaluation Pipeline
Interactive and publication-quality visualizations
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class AdvancedVisualizer:
    """
    Advanced visualization suite
    
    Features:
    - 3D scatter plots with clusters
    - Interactive surfaces
    - Animated transitions
    - Network graphs
    - Sankey diagrams
    """
    
    def __init__(self, output_dir: str = "visualizations"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
        # Color schemes
        self.color_schemes = {
            'bias': ['#2ecc71', '#f39c12', '#e74c3c'],  # Green, Orange, Red
            'sentiment': ['#3498db', '#95a5a6', '#e67e22'],  # Blue, Gray, Orange
            'regions': ['#9b59b6', '#1abc9c', '#34495e', '#e74c3c']  # Purple, Teal, Dark, Red
        }
        
        logger.info(f"✅ Advanced Visualizer initialized: {self.output_dir}")
    
    def create_3d_bias_scatter(
        self,
        df: pd.DataFrame,
        x_col: str = 'accuracy',
        y_col: str = 'bias_score',
        z_col: str = 'fairness_score',
        color_col: str = 'region',
        title: str = '3D Bias Analysis'
    ) -> go.Figure:
        """
        Create interactive 3D scatter plot
        
        Args:
            df: DataFrame with data
            x_col, y_col, z_col: Column names for axes
            color_col: Column for color coding
            title: Plot title
        
        Returns:
            Plotly Figure object
        """
        fig = go.Figure(data=[go.Scatter3d(
            x=df[x_col],
            y=df[y_col],
            z=df[z_col],
            mode='markers',
            marker=dict(
                size=8,
                color=df[color_col].astype('category').cat.codes,
                colorscale='Viridis',
                showscale=True,
                line=dict(width=0.5, color='white')
            ),
            text=df[color_col],
            hovertemplate=
                f'<b>{color_col}</b>: %{{text}}<br>' +
                f'{x_col}: %{{x:.3f}}<br>' +
                f'{y_col}: %{{y:.3f}}<br>' +
                f'{z_col}: %{{z:.3f}}<br>' +
                '<extra></extra>'
        )])
        
        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title=x_col.replace('_', ' ').title(),
                yaxis_title=y_col.replace('_', ' ').title(),
                zaxis_title=z_col.replace('_', ' ').title(),
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            width=1000,
            height=800
        )
        
        output_path = self.output_dir / f"{title.replace(' ', '_')}.html"
        fig.write_html(output_path)
        
        logger.info(f"📊 3D scatter created: {output_path}")
        return fig
    
    def create_bias_surface(
        self,
        data: np.ndarray,
        x_labels: List[str],
        y_labels: List[str],
        title: str = 'Bias Surface'
    ) -> go.Figure:
        """
        Create 3D surface plot for bias across dimensions
        
        Args:
            data: 2D numpy array
            x_labels: Labels for x-axis
            y_labels: Labels for y-axis
            title: Plot title
        
        Returns:
            Plotly Figure object
        """
        fig = go.Figure(data=[go.Surface(
            z=data,
            x=x_labels,
            y=y_labels,
            colorscale='RdYlGn_r',
            reversescale=False
        )])
        
        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title='Demographic Groups',
                yaxis_title='Sentiment Categories',
                zaxis_title='Bias Score',
                camera=dict(
                    eye=dict(x=1.7, y=1.7, z=1.3)
                )
            ),
            width=1000,
            height=800
        )
        
        output_path = self.output_dir / f"{title.replace(' ', '_')}.html"
        fig.write_html(output_path)
        
        logger.info(f"🌊 Surface plot created: {output_path}")
        return fig
    
    def create_animated_bias_evolution(
        self,
        time_series_data: Dict[str, pd.DataFrame],
        title: str = 'Bias Evolution Over Time'
    ) -> go.Figure:
        """
        Create animated visualization of bias changes over time
        
        Args:
            time_series_data: Dict of timestamp -> DataFrame
            title: Plot title
        
        Returns:
            Plotly Figure object
        """
        # Prepare frames
        frames = []
        
        for timestamp, df in time_series_data.items():
            frame = go.Frame(
                data=[go.Scatter3d(
                    x=df['x'],
                    y=df['y'],
                    z=df['z'],
                    mode='markers',
                    marker=dict(
                        size=8,
                        color=df['bias'],
                        colorscale='RdYlGn_r',
                        showscale=True
                    )
                )],
                name=str(timestamp)
            )
            frames.append(frame)
        
        # Initial frame
        first_df = list(time_series_data.values())[0]
        
        fig = go.Figure(
            data=[go.Scatter3d(
                x=first_df['x'],
                y=first_df['y'],
                z=first_df['z'],
                mode='markers',
                marker=dict(
                    size=8,
                    color=first_df['bias'],
                    colorscale='RdYlGn_r',
                    showscale=True
                )
            )],
            frames=frames
        )
        
        # Add play/pause buttons
        fig.update_layout(
            title=title,
            updatemenus=[{
                'type': 'buttons',
                'showactive': False,
                'buttons': [
                    {
                        'label': '▶ Play',
                        'method': 'animate',
                        'args': [None, {
                            'frame': {'duration': 500, 'redraw': True},
                            'fromcurrent': True
                        }]
                    },
                    {
                        'label': '⏸ Pause',
                        'method': 'animate',
                        'args': [[None], {
                            'frame': {'duration': 0, 'redraw': False},
                            'mode': 'immediate'
                        }]
                    }
                ]
            }],
            width=1000,
            height=800
        )
        
        output_path = self.output_dir / f"{title.replace(' ', '_')}.html"
        fig.write_html(output_path)
        
        logger.info(f"🎬 Animated plot created: {output_path}")
        return fig
    
    def create_bias_sankey(
        self,
        df: pd.DataFrame,
        source_col: str = 'region',
        target_col: str = 'sentiment',
        value_col: str = 'count',
        title: str = 'Bias Flow Diagram'
    ) -> go.Figure:
        """
        Create Sankey diagram showing bias flow
        
        Args:
            df: DataFrame with flow data
            source_col: Source column
            target_col: Target column
            value_col: Value column
            title: Plot title
        
        Returns:
            Plotly Figure object
        """
        # Create node labels
        sources = df[source_col].unique().tolist()
        targets = df[target_col].unique().tolist()
        all_nodes = sources + targets
        
        # Map to indices
        source_indices = [all_nodes.index(s) for s in df[source_col]]
        target_indices = [all_nodes.index(t) for t in df[target_col]]
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color='black', width=0.5),
                label=all_nodes,
                color=['lightblue'] * len(sources) + ['lightcoral'] * len(targets)
            ),
            link=dict(
                source=source_indices,
                target=target_indices,
                value=df[value_col].tolist()
            )
        )])
        
        fig.update_layout(
            title=title,
            font_size=12,
            width=1200,
            height=700
        )
        
        output_path = self.output_dir / f"{title.replace(' ', '_')}.html"
        fig.write_html(output_path)
        
        logger.info(f"🌊 Sankey diagram created: {output_path}")
        return fig
    
    def create_fairness_radar(
        self,
        metrics: Dict[str, float],
        title: str = 'Fairness Metrics Radar'
    ) -> go.Figure:
        """
        Create radar chart for fairness metrics
        
        Args:
            metrics: Dictionary of metric_name -> value
            title: Plot title
        
        Returns:
            Plotly Figure object
        """
        categories = list(metrics.keys())
        values = list(metrics.values())
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Fairness Score',
            line=dict(color='rgb(46, 204, 113)', width=2)
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            showlegend=True,
            title=title,
            width=700,
            height=700
        )
        
        output_path = self.output_dir / f"{title.replace(' ', '_')}.html"
        fig.write_html(output_path)
        
        logger.info(f"📡 Radar chart created: {output_path}")
        return fig
    
    def create_correlation_heatmap_3d(
        self,
        corr_matrix: pd.DataFrame,
        title: str = '3D Correlation Heatmap'
    ) -> go.Figure:
        """
        Create 3D heatmap for correlation matrix
        
        Args:
            corr_matrix: Correlation matrix DataFrame
            title: Plot title
        
        Returns:
            Plotly Figure object
        """
        fig = go.Figure(data=[go.Surface(
            z=corr_matrix.values,
            x=corr_matrix.columns.tolist(),
            y=corr_matrix.index.tolist(),
            colorscale='RdBu',
            zmid=0,
            colorbar=dict(title='Correlation')
        )])
        
        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title='Features',
                yaxis_title='Features',
                zaxis_title='Correlation',
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
            ),
            width=1000,
            height=800
        )
        
        output_path = self.output_dir / f"{title.replace(' ', '_')}.html"
        fig.write_html(output_path)
        
        logger.info(f"🔥 3D heatmap created: {output_path}")
        return fig
    
    def create_dashboard_layout(
        self,
        figures: Dict[str, go.Figure],
        title: str = 'Bias Analysis Dashboard'
    ) -> go.Figure:
        """
        Create multi-panel dashboard
        
        Args:
            figures: Dictionary of subplot_name -> figure
            title: Dashboard title
        
        Returns:
            Combined Plotly Figure
        """
        n_plots = len(figures)
        rows = (n_plots + 1) // 2
        cols = 2
        
        fig = make_subplots(
            rows=rows,
            cols=cols,
            subplot_titles=list(figures.keys()),
            specs=[[{'type': 'scene'} for _ in range(cols)] for _ in range(rows)]
        )
        
        for idx, (name, sub_fig) in enumerate(figures.items()):
            row = idx // cols + 1
            col = idx % cols + 1
            
            for trace in sub_fig.data:
                fig.add_trace(trace, row=row, col=col)
        
        fig.update_layout(
            title_text=title,
            showlegend=False,
            width=1600,
            height=1200
        )
        
        output_path = self.output_dir / f"{title.replace(' ', '_')}.html"
        fig.write_html(output_path)
        
        logger.info(f"📊 Dashboard created: {output_path}")
        return fig


# Example usage
if __name__ == "__main__":
    print("🎨 Testing Advanced Visualization Suite\n")
    
    # Create sample data
    np.random.seed(42)
    
    df = pd.DataFrame({
        'accuracy': np.random.uniform(0.7, 0.95, 50),
        'bias_score': np.random.uniform(0.05, 0.25, 50),
        'fairness_score': np.random.uniform(0.75, 0.95, 50),
        'region': np.random.choice(['Gulf', 'Levant', 'Egypt', 'N.Africa'], 50)
    })
    
    # Initialize visualizer
    viz = AdvancedVisualizer()
    
    # Create 3D scatter
    print("Creating 3D scatter plot...")
    fig1 = viz.create_3d_bias_scatter(df)
    
    # Create surface
    print("Creating bias surface...")
    surface_data = np.random.rand(5, 4)
    fig2 = viz.create_bias_surface(
        surface_data,
        ['Group1', 'Group2', 'Group3', 'Group4'],
        ['Positive', 'Negative', 'Neutral', 'Mixed', 'Unknown']
    )
    
    # Create radar chart
    print("Creating fairness radar...")
    metrics = {
        'Demographic Parity': 0.85,
        'Equalized Odds': 0.78,
        'Disparate Impact': 0.92,
        'Predictive Parity': 0.88,
        'Calibration': 0.91
    }
    fig3 = viz.create_fairness_radar(metrics)
    
    print("\n✅ Visualizations created!")
    print(f"📁 Output directory: {viz.output_dir}")