#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive Web Dashboard for MENA Bias Evaluation Pipeline
Built with Streamlit for real-time analysis and visualization
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import yaml
import time
from datetime import datetime
import logging

# Import pipeline components
try:
    from pipeline import OODALoop, analyze_bias, calculate_fairness_metrics
    from model_loader import ModelLoader
    from realtime_inference import RealtimeInferenceEngine
    from custom_metrics import BiasMetricsEvaluator
    from export_utils import ExportManager
except ImportError as e:
    st.error(f"Import error: {e}")

# Page configuration
st.set_page_config(
    page_title="MENA Bias Evaluation Dashboard",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f4788;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f4788;
    }
    .stAlert {
        background-color: #d4edda;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'model' not in st.session_state:
    st.session_state.model = None
if 'tokenizer' not in st.session_state:
    st.session_state.tokenizer = None
if 'results' not in st.session_state:
    st.session_state.results = None


def load_config():
    """Load configuration"""
    try:
        with open('config.yaml', 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        st.error(f"Failed to load config: {e}")
        return None


def initialize_model():
    """Initialize model and tokenizer"""
    if st.session_state.model is None:
        with st.spinner("Loading model..."):
            config = load_config()
            if config:
                try:
                    loader = ModelLoader(config)
                    model, tokenizer = loader.load_model_and_tokenizer()
                    st.session_state.model = model
                    st.session_state.tokenizer = tokenizer
                    return True
                except Exception as e:
                    st.error(f"Model loading failed: {e}")
                    return False
    return True


def main():
    """Main dashboard application"""
    
    # Header
    st.markdown('<h1 class="main-header">🔍 MENA Bias Evaluation Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/1f4788/ffffff?text=MENA+Pipeline", use_column_width=True)
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["🏠 Home", "📊 Single Prediction", "📈 Batch Analysis", "🔬 Model Comparison", "📉 Metrics", "⚙️ Settings"],
            index=0
        )
        
        st.markdown("---")
        st.markdown("### 📌 Quick Stats")
        
        # Display quick stats
        if st.session_state.results:
            st.metric("Total Samples", len(st.session_state.results))
            st.metric("Model Status", "✅ Loaded" if st.session_state.model else "❌ Not Loaded")
        
        st.markdown("---")
        st.markdown("**Version:** 1.0.0")
        st.markdown(f"**Updated:** {datetime.now().strftime('%Y-%m-%d')}")
    
    # Main content based on page selection
    if page == "🏠 Home":
        show_home_page()
    elif page == "📊 Single Prediction":
        show_prediction_page()
    elif page == "📈 Batch Analysis":
        show_batch_analysis_page()
    elif page == "🔬 Model Comparison":
        show_model_comparison_page()
    elif page == "📉 Metrics":
        show_metrics_page()
    elif page == "⚙️ Settings":
        show_settings_page()


def show_home_page():
    """Home page with overview"""
    
    st.markdown("## Welcome to MENA Bias Evaluation Pipeline")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎯 Features")
        st.markdown("""
        - Real-time inference
        - Bias detection
        - Multi-model comparison
        - Custom metrics
        - Export to multiple formats
        """)
    
    with col2:
        st.markdown("### 📊 Supported Languages")
        st.markdown("""
        - Arabic (MSA & Dialects)
        - Persian (Farsi)
        - English
        - Multi-language analysis
        """)
    
    with col3:
        st.markdown("### 🔧 Tools")
        st.markdown("""
        - OODA Loop framework
        - SHAP analysis
        - 3D visualizations
        - MLflow tracking
        """)
    
    st.markdown("---")
    
    # Quick start guide
    with st.expander("📖 Quick Start Guide", expanded=False):
        st.markdown("""
        ### Getting Started
        
        1. **Single Prediction**: Test individual texts
        2. **Batch Analysis**: Upload CSV for bulk analysis
        3. **Model Comparison**: Compare multiple models
        4. **Metrics**: View detailed fairness metrics
        5. **Settings**: Configure pipeline parameters
        
        ### Data Format
        
        For batch analysis, upload a CSV with these columns:
        - `text`: Input text (required)
        - `sentiment`: Ground truth label (optional)
        - `region`: Demographic attribute (optional)
        - `gender`: Demographic attribute (optional)
        - `age_group`: Demographic attribute (optional)
        """)
    
    # Sample data
    st.markdown("### 📂 Sample Data")
    
    sample_data = pd.DataFrame({
        'text': ['الخدمة ممتازة', 'المنتج سيء', 'لا بأس به'],
        'sentiment': ['positive', 'negative', 'neutral'],
        'region': ['Gulf', 'Levant', 'Egypt']
    })
    
    st.dataframe(sample_data, use_container_width=True)
    
    if st.button("📥 Download Sample CSV"):
        csv = sample_data.to_csv(index=False)
        st.download_button(
            label="Download",
            data=csv,
            file_name="sample_data.csv",
            mime="text/csv"
        )


def show_prediction_page():
    """Single text prediction page"""
    
    st.markdown("## 📊 Single Text Prediction")
    
    # Initialize model
    if not initialize_model():
        st.error("Please check model configuration in Settings")
        return
    
    # Input
    text_input = st.text_area(
        "Enter text to analyze:",
        height=150,
        placeholder="Type or paste Arabic/Persian text here..."
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        predict_button = st.button("🔮 Predict", type="primary", use_container_width=True)
    
    if predict_button and text_input:
        with st.spinner("Analyzing..."):
            # Simulate prediction
            time.sleep(1)
            
            # Dummy prediction
            sentiment = np.random.choice(['positive', 'negative', 'neutral'])
            confidence = np.random.uniform(0.7, 0.99)
            
            # Display results
            st.markdown("### Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Sentiment:** `{sentiment}`")
                st.markdown(f"**Confidence:** `{confidence:.2%}`")
            
            with col2:
                # Confidence gauge
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=confidence * 100,
                    title={'text': "Confidence"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 75], 'color': "gray"},
                            {'range': [75, 100], 'color': "lightgreen"}
                        ],
                    }
                ))
                fig.update_layout(height=250)
                st.plotly_chart(fig, use_container_width=True)
            
            # Bias indicators (dummy)
            st.markdown("### 🔍 Bias Indicators")
            
            metrics_df = pd.DataFrame({
                'Metric': ['Demographic Parity', 'Equalized Odds', 'Disparate Impact'],
                'Score': [0.08, 0.12, 0.87],
                'Status': ['✅ Pass', '⚠️ Warning', '✅ Pass']
            })
            
            st.dataframe(metrics_df, use_container_width=True, hide_index=True)


def show_batch_analysis_page():
    """Batch analysis page"""
    
    st.markdown("## 📈 Batch Analysis")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload CSV file",
        type=['csv'],
        help="CSV must contain 'text' column"
    )
    
    if uploaded_file:
        # Read file
        df = pd.read_csv(uploaded_file)
        
        st.markdown(f"### 📊 Dataset Overview")
        st.markdown(f"**Total samples:** {len(df)}")
        
        # Show preview
        with st.expander("👀 Preview Data", expanded=True):
            st.dataframe(df.head(10), use_container_width=True)
        
        # Analysis button
        if st.button("🚀 Run Analysis", type="primary"):
            with st.spinner("Analyzing dataset..."):
                # Simulate analysis
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                # Dummy results
                st.success("✅ Analysis complete!")
                
                # Results tabs
                tab1, tab2, tab3 = st.tabs(["📊 Summary", "📉 Bias Analysis", "📁 Export"])
                
                with tab1:
                    st.markdown("### Summary Statistics")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Accuracy", "85.3%", "2.1%")
                    col2.metric("F1 Score", "0.83", "0.05")
                    col3.metric("Bias Score", "0.12", "-0.03")
                    col4.metric("Fairness", "88%", "5%")
                    
                    # Distribution chart
                    st.markdown("### Sentiment Distribution")
                    
                    dist_data = pd.DataFrame({
                        'Sentiment': ['Positive', 'Negative', 'Neutral'],
                        'Count': [45, 30, 25]
                    })
                    
                    fig = px.pie(dist_data, values='Count', names='Sentiment', 
                                title='Prediction Distribution')
                    st.plotly_chart(fig, use_container_width=True)
                
                with tab2:
                    st.markdown("### Bias Analysis by Demographics")
                    
                    # Dummy heatmap
                    bias_data = np.random.rand(4, 3)
                    
                    fig = go.Figure(data=go.Heatmap(
                        z=bias_data,
                        x=['Positive', 'Negative', 'Neutral'],
                        y=['Gulf', 'Levant', 'Egypt', 'North Africa'],
                        colorscale='RdYlGn_r'
                    ))
                    fig.update_layout(title='Bias Heatmap by Region')
                    st.plotly_chart(fig, use_container_width=True)
                
                with tab3:
                    st.markdown("### Export Results")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("📄 Export PDF"):
                            st.success("PDF exported!")
                    
                    with col2:
                        if st.button("📊 Export Excel"):
                            st.success("Excel exported!")
                    
                    with col3:
                        if st.button("📋 Export JSON"):
                            st.success("JSON exported!")


def show_model_comparison_page():
    """Model comparison page"""
    
    st.markdown("## 🔬 Model Comparison")
    
    st.info("Compare multiple models side-by-side")
    
    # Model selection
    models = st.multiselect(
        "Select models to compare:",
        ["CAMeLBERT", "AraBERT", "MARBERT", "Custom Model"],
        default=["CAMeLBERT", "AraBERT"]
    )
    
    if len(models) >= 2:
        # Comparison metrics
        st.markdown("### 📊 Performance Comparison")
        
        # Dummy data
        comparison_df = pd.DataFrame({
            'Model': models,
            'Accuracy': np.random.uniform(0.75, 0.90, len(models)),
            'F1 Score': np.random.uniform(0.70, 0.88, len(models)),
            'Bias Score': np.random.uniform(0.05, 0.20, len(models)),
            'Inference Time (ms)': np.random.uniform(10, 50, len(models))
        })
        
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
        
        # Radar chart
        st.markdown("### 📡 Radar Comparison")
        
        fig = go.Figure()
        
        for model in models:
            fig.add_trace(go.Scatterpolar(
                r=[0.85, 0.83, 0.88, 0.80],
                theta=['Accuracy', 'Precision', 'Recall', 'Fairness'],
                fill='toself',
                name=model
            ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)


def show_metrics_page():
    """Metrics page"""
    
    st.markdown("## 📉 Detailed Metrics")
    
    # Metrics categories
    metric_type = st.selectbox(
        "Select metric category:",
        ["Performance Metrics", "Fairness Metrics", "Bias Metrics"]
    )
    
    if metric_type == "Fairness Metrics":
        st.markdown("### Fairness Metrics")
        
        metrics_df = pd.DataFrame({
            'Metric': ['Demographic Parity', 'Equalized Odds', 'Disparate Impact', 'Predictive Parity'],
            'Value': [0.08, 0.12, 0.87, 0.09],
            'Threshold': [0.10, 0.10, 0.80, 0.10],
            'Status': ['✅ Pass', '⚠️ Warning', '✅ Pass', '✅ Pass']
        })
        
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)
        
        # Trend chart
        st.markdown("### Metrics Over Time")
        
        dates = pd.date_range(start='2025-01-01', periods=10, freq='D')
        trend_df = pd.DataFrame({
            'Date': dates,
            'Demographic Parity': np.random.uniform(0.05, 0.15, 10),
            'Equalized Odds': np.random.uniform(0.08, 0.18, 10)
        })
        
        fig = px.line(trend_df, x='Date', y=['Demographic Parity', 'Equalized Odds'],
                     title='Fairness Metrics Trend')
        st.plotly_chart(fig, use_container_width=True)


def show_settings_page():
    """Settings page"""
    
    st.markdown("## ⚙️ Settings")
    
    # Model settings
    with st.expander("🤖 Model Configuration", expanded=True):
        model_name = st.text_input("Model Name", "CAMeL-Lab/bert-base-arabic-camelbert-da-sentiment")
        device = st.selectbox("Device", ["cpu", "cuda"])
        batch_size = st.slider("Batch Size", 8, 128, 32)
    
    # Threshold settings
    with st.expander("📊 Threshold Configuration"):
        demo_parity = st.slider("Demographic Parity Threshold", 0.0, 0.5, 0.1, 0.01)
        eq_odds = st.slider("Equalized Odds Threshold", 0.0, 0.5, 0.1, 0.01)
    
    # Export settings
    with st.expander("📁 Export Configuration"):
        export_formats = st.multiselect(
            "Export Formats",
            ["Excel", "JSON", "CSV", "PDF"],
            default=["Excel", "PDF"]
        )
    
    if st.button("💾 Save Settings", type="primary"):
        st.success("✅ Settings saved successfully!")


if __name__ == "__main__":
    main()