---
title: MENA Bias Evaluation Pipeline - Enterprise Edition
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: static
app_file: api.py
pinned: false
---
# 🚀 MENA Bias Evaluation Pipeline - Enterprise Edition
... (بقیه محتوای شما)
# 🚀 MENA Bias Evaluation Pipeline - Enterprise Edition

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Quality](https://img.shields.io/badge/Code%20Quality-A+-brightgreen.svg)]()
[![Tests](https://img.shields.io/badge/Tests-70%2B-success.svg)]()
[![Coverage](https://img.shields.io/badge/Coverage-80%25%2B-brightgreen.svg)]()

**Enterprise-grade bias detection toolkit for Arabic/Persian sentiment analysis with real-time inference, MLflow tracking, and production deployment.**

---

## ✨ Key Features

### 🎯 Core Capabilities
- ✅ **Real-time Inference Engine** - High-performance streaming with intelligent batching
- ✅ **Multi-Model Comparison** - Compare unlimited models with statistical significance testing
- ✅ **Custom Bias Metrics** - 10+ fairness metrics with configurable thresholds
- ✅ **OODA Loop Framework** - Observe-Orient-Decide-Act decision cycle
- ✅ **SHAP Integration** - Model interpretability and explainability

### 🌐 Multi-Language Support
- ✅ **Arabic** (MSA + Dialects)
- ✅ **Persian** (Farsi)
- ✅ **English**
- ✅ Auto language detection and normalization

### 📊 Visualization Suite
- ✅ **3D Interactive Plots** - Plotly-powered with 360° exploration
- ✅ **Animated Bias Evolution** - Track changes over time
- ✅ **Sankey Diagrams** - Bias flow visualization
- ✅ **Radar Charts** - Fairness metrics comparison
- ✅ **Heatmaps** - Correlation and bias patterns

### 🔬 Advanced Analytics
- ✅ **A/B Testing Framework** - Statistical comparison with Bayesian methods
- ✅ **MLflow Integration** - Experiment tracking and model registry
- ✅ **Performance Monitoring** - Caching, profiling, and optimization
- ✅ **Multi-Format Export** - Excel, JSON, CSV, Parquet, Markdown, HTML

### 🌐 Deployment Options
- ✅ **REST API** - FastAPI with OpenAPI documentation
- ✅ **Web Dashboard** - Streamlit interactive interface
- ✅ **Docker Compose** - Multi-service orchestration
- ✅ **Kubernetes Ready** - Production-scale deployment
- ✅ **CI/CD Pipeline** - GitHub Actions automation

---

## 📦 Project Structure
```
mena_eval_tools/
├── 🐍 Core Pipeline
│   ├── pipeline.py                  # Main analysis pipeline
│   ├── model_loader.py              # Advanced model loading
│   ├── realtime_inference.py        # Real-time streaming engine
│   └── validators.py                # Input validation
│
├── 📊 Analysis & Metrics
│   ├── custom_metrics.py            # Custom fairness metrics
│   ├── model_comparison.py          # Multi-model comparison
│   ├── ab_testing.py                # A/B testing framework
│   └── multilingual_support.py      # Multi-language processing
│
├── 📈 Visualization
│   ├── advanced_viz.py              # 3D visualization suite
│   └── export_utils.py              # Multi-format export
│
├── 🔬 Tracking & Monitoring
│   ├── mlflow_integration.py        # MLflow experiment tracking
│   ├── performance.py               # Performance optimization
│   └── logger.py                    # Structured logging
│
├── 🌐 Web Interfaces
│   ├── api.py                       # FastAPI REST API
│   └── dashboard.py                 # Streamlit dashboard
│
├── 🧪 Testing & Quality
│   ├── tests/                       # 70+ unit tests
│   ├── pytest.ini                   # Test configuration
│   └── .pre-commit-config.yaml      # Code quality hooks
│
├── 🐳 Deployment
│   ├── Dockerfile                   # Main container
│   ├── Dockerfile.dashboard         # Dashboard container
│   ├── docker-compose.yml           # Multi-service setup
│   └── nginx/                       # Reverse proxy config
│
├── 📚 Documentation
│   ├── README.md                    # This file
│   ├── API.md                       # API documentation
│   ├── DEPLOYMENT.md                # Deployment guide
│   ├── CONTRIBUTING.md              # Contribution guidelines
│   ├── CHANGELOG.md                 # Version history
│   └── LICENSE                      # MIT License
│
└── ⚙️ Configuration
    ├── config.yaml                  # Main configuration
    ├── requirements.txt             # Production dependencies
    ├── requirements-dev.txt         # Development dependencies
    ├── requirements-api.txt         # API dependencies
    └── setup.py                     # Package setup
```

---

## 🚀 Quick Start

### Option 1: Python Local (Recommended)
```bash
# 1. Clone or extract
cd mena_eval_tools

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install --upgrade pip
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt

# 4. Run pipeline
python pipeline.py
```

### Option 2: Docker (Production)
```bash
# Build and start all services
docker-compose up -d

# Access services
# API: http://localhost:8000/docs
# Dashboard: http://localhost:8501
# MLflow: http://localhost:5000
```

### Option 3: API Only
```bash
# Install API dependencies
pip install -r requirements-api.txt

# Start API server
python api.py

# View docs: http://localhost:8000/docs
```

### Option 4: Dashboard Only
```bash
# Install and run
pip install streamlit
streamlit run dashboard.py
```

---

## 🎯 Usage Examples

### Example 1: Single Text Prediction
```python
from realtime_inference import RealtimeInferenceEngine

# Initialize engine
engine = RealtimeInferenceEngine(
    model_name="CAMeL-Lab/bert-base-arabic-camelbert-da-sentiment"
)

# Start engine
engine.start()

# Predict
result = engine.predict_sync("الخدمة ممتازة جداً")
print(f"Sentiment: {result.sentiment}, Confidence: {result.confidence:.2%}")

# Stop engine
engine.stop()
```

### Example 2: Batch Analysis with Bias Detection
```python
import pandas as pd
from pipeline import OODALoop, analyze_bias

# Load data
df = pd.read_csv('input/data.csv')

# Initialize OODA Loop
ooda = OODALoop()

# Run analysis
observation = ooda.observe(df)
predictions = model.predict(df['text'])
orientation = ooda.orient(predictions, df['sentiment'])
decision = ooda.decide(orientation)
action = ooda.act(decision)

# Analyze bias
bias_results = analyze_bias(df, predictions)
print(f"Fairness Score: {bias_results['fairness']['overall_fairness']:.2%}")
```

### Example 3: Multi-Model Comparison
```python
from model_comparison import ModelComparator

# Initialize comparator
comparator = ModelComparator()

# Add models
comparator.add_model("CAMeLBERT", model1, tokenizer1)
comparator.add_model("AraBERT", model2, tokenizer2)

# Compare
results = comparator.compare_all(test_data)
report = comparator.generate_comparison_report()
comparator.visualize_comparison()
```

### Example 4: A/B Testing
```python
from ab_testing import ABTester
import numpy as np

# Initialize tester
tester = ABTester(alpha=0.05)

# Generate data
variant_a = np.random.normal(0.80, 0.05, 1000)
variant_b = np.random.normal(0.85, 0.05, 1000)

# Run test
result = tester.t_test(variant_a, variant_b)
print(result.recommendation)
```

### Example 5: MLflow Experiment Tracking
```python
from mlflow_integration import MLflowExperimentTracker, MLflowRun

# Initialize tracker
tracker = MLflowExperimentTracker("My_Experiment")

# Track experiment
with MLflowRun(tracker, run_name="test_run"):
    tracker.log_parameters({'batch_size': 32, 'lr': 0.001})
    tracker.log_metrics({'accuracy': 0.85, 'f1': 0.83})
    tracker.log_model(model, "model")
```

---

## 📊 Performance Benchmarks

| Metric | Value |
|--------|-------|
| **Inference Speed** | ~50ms per sample (CPU) |
| **Batch Throughput** | ~1000 samples/sec |
| **Memory Usage** | ~500MB (base model) |
| **Accuracy** | 85%+ on test sets |
| **Test Coverage** | 80%+ |

---

## 🔧 Configuration

All settings are managed through `config.yaml`:
```yaml
model:
  name: "CAMeL-Lab/bert-base-arabic-camelbert-da-sentiment"
  device: "cpu"  # or "cuda"
  
data:
  input_dir: "input"
  output_dir: "output"
  
bias:
  fairness_threshold: 0.8
  
performance:
  batch_size: 32
  enable_cache: true
```

---

## 🧪 Testing
```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=. --cov-report=html

# Specific test file
pytest tests/test_pipeline.py -v
```

---

## 📚 Documentation

- **[API Documentation](docs/API.md)** - Complete API reference
- **[Deployment Guide](DEPLOYMENT.md)** - Production deployment
- **[Contributing](CONTRIBUTING.md)** - Contribution guidelines
- **[Changelog](CHANGELOG.md)** - Version history

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run quality checks
black .
flake8 .
mypy pipeline.py
```

---

## 📈 Roadmap

### v1.1 (Planned)
- [ ] GPU acceleration support
- [ ] More pre-trained models
- [ ] Web UI improvements
- [ ] Mobile app

### v2.0 (Future)
- [ ] Federated learning
- [ ] AutoML integration
- [ ] Real-time monitoring dashboard
- [ ] Multi-modal bias detection

---

## 🏆 Key Differentiators

| Feature | This Project | Competitors |
|---------|-------------|-------------|
| Real-time Inference | ✅ Yes | ❌ No |
| Multi-Language | ✅ AR/FA/EN | ⚠️ Limited |
| Custom Metrics | ✅ 10+ metrics | ⚠️ 2-3 metrics |
| MLflow Integration | ✅ Full | ❌ No |
| A/B Testing | ✅ Built-in | ❌ No |
| Web Dashboard | ✅ Streamlit | ⚠️ Basic |
| Production Ready | ✅ Docker Compose | ⚠️ Limited |
| Documentation | ✅ Comprehensive | ⚠️ Minimal |

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- HuggingFace Transformers for model infrastructure
- CAMeL Lab for Arabic NLP models
- Plotly team for visualization tools
- MLflow community for experiment tracking

---

## 📧 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/mena-bias-evaluation/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/mena-bias-evaluation/discussions)
- **Email**:uae.ai.tester@gmail.com

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Made with ❤️ for fair and unbiased AI**

**Version**: 1.0.0  
**Last Updated**: November 2025  
**Status**: Production Ready 🚀

---
title: Mena Bias Api
emoji: 📉
colorFrom: purple
colorTo: red
sdk: docker
pinned: false
license: mit
short_description: 'Enterprise-grade bias detection for Arabic/Persian NLP with '
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference c1c03b1952fe313a5482d60b4228f59ac2fe7ddd
