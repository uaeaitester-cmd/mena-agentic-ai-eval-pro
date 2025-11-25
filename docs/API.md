\# API Documentation



\## MENA Bias Evaluation Pipeline API Reference



\### Core Classes



\#### `OODALoop`



OODA (Observe-Orient-Decide-Act) decision framework for bias detection.



\*\*Methods:\*\*



\- `observe(data: pd.DataFrame) -> dict`

&nbsp; - Collects data and initial metrics

&nbsp; - Returns: Observation dictionary with timestamp, shape, columns



\- `orient(predictions: np.array, ground\_truth: np.array) -> dict`

&nbsp; - Analyzes patterns and biases

&nbsp; - Returns: Orientation with accuracy and bias indicators



\- `decide(orientation: dict) -> dict`

&nbsp; - Determines mitigation strategies

&nbsp; - Returns: Decision with severity and recommended actions



\- `act(decision: dict) -> dict`

&nbsp; - Executes mitigation strategies

&nbsp; - Returns: Action record with timestamp



\*\*Example:\*\*

```python

from pipeline import OODALoop

import pandas as pd



ooda = OODALoop()

df = pd.read\_csv('data.csv')



\# Observe

obs = ooda.observe(df)



\# Orient

predictions = model.predict(df\['text'])

orientation = ooda.orient(predictions, df\['sentiment'])



\# Decide

decision = ooda.decide(orientation)



\# Act

action = ooda.act(decision)

```



---



\#### `ModelLoader`



Advanced model loading with multiple fallback strategies.



\*\*Parameters:\*\*



\- `config: Dict\[str, Any]` - Configuration dictionary



\*\*Methods:\*\*



\- `load\_model\_and\_tokenizer() -> Tuple\[Optional\[Model], Optional\[Tokenizer]]`

&nbsp; - Loads model with fallback strategies

&nbsp; - Returns: (model, tokenizer) or (None, None)



\*\*Example:\*\*

```python

from model\_loader import ModelLoader

import yaml



with open('config.yaml') as f:

&nbsp;   config = yaml.safe\_load(f)



loader = ModelLoader(config)

model, tokenizer = loader.load\_model\_and\_tokenizer()

```



---



\#### `PerformanceMonitor`



Monitor and log performance metrics.



\*\*Methods:\*\*



\- `time\_function(func: Callable) -> Callable`

&nbsp; - Decorator to time function execution



\- `get\_stats() -> dict`

&nbsp; - Returns performance statistics



\*\*Example:\*\*

```python

from performance import PerformanceMonitor



monitor = PerformanceMonitor()



@monitor.time\_function

def my\_function():

&nbsp;   # Your code here

&nbsp;   pass



my\_function()

stats = monitor.get\_stats()

```



---



\#### `ResultCache`



Cache expensive computation results.



\*\*Parameters:\*\*



\- `cache\_dir: str` - Directory for cache files (default: ".cache")



\*\*Methods:\*\*



\- `cache\_result(func: Callable) -> Callable`

&nbsp; - Decorator to cache function results



\- `clear\_cache() -> None`

&nbsp; - Clear all cached results



\*\*Example:\*\*

```python

from performance import ResultCache



cache = ResultCache()



@cache.cache\_result

def expensive\_function(x):

&nbsp;   # Expensive computation

&nbsp;   return x \* 2



result = expensive\_function(5)  # Computes

result = expensive\_function(5)  # Loads from cache

```



---



\### Utility Functions



\#### `generate\_sample\_data() -> pd.DataFrame`



Generate sample Arabic/Persian sentiment data for testing.



\*\*Returns:\*\* DataFrame with columns: text, sentiment, region, gender, age\_group



---



\#### `predict\_sentiment(texts: List\[str], model, tokenizer) -> List\[str]`



Predict sentiment for given texts.



\*\*Parameters:\*\*

\- `texts: List\[str]` - List of text strings

\- `model` - Trained model (or None for dummy)

\- `tokenizer` - Tokenizer (or None for dummy)



\*\*Returns:\*\* List of sentiment labels



---



\#### `analyze\_bias(df: pd.DataFrame, predictions: List\[str]) -> dict`



Analyze bias across demographic groups.



\*\*Parameters:\*\*

\- `df: pd.DataFrame` - DataFrame with demographic columns

\- `predictions: List\[str]` - Model predictions



\*\*Returns:\*\* Bias analysis results dictionary



---



\#### `calculate\_fairness\_metrics(df: pd.DataFrame) -> dict`



Calculate fairness metrics across groups.



\*\*Parameters:\*\*

\- `df: pd.DataFrame` - DataFrame with 'prediction' column



\*\*Returns:\*\* Dictionary of fairness metrics



---



\### Configuration



Configuration is managed through `config.yaml`. See example:

```yaml

model:

&nbsp; name: "CAMeL-Lab/bert-base-arabic-camelbert-da-sentiment"

&nbsp; local\_path: "input/pytorch\_model.bin"

&nbsp; device: "cpu"



data:

&nbsp; input\_dir: "input"

&nbsp; output\_dir: "output"



bias:

&nbsp; demographics:

&nbsp;   - region

&nbsp;   - gender

&nbsp;   - age\_group

```



---



\### Command Line Usage



Run the complete pipeline:

```bash

python pipeline.py

```



Run with custom config:

```bash

python pipeline.py --config custom\_config.yaml

```



---



\### Error Handling



All functions include proper error handling. Example:

```python

try:

&nbsp;   model, tokenizer = load\_model\_and\_tokenizer()

except Exception as e:

&nbsp;   logger.error(f"Model loading failed: {e}")

```



---



\### Performance Tips



1\. \*\*Use caching\*\* for expensive operations

2\. \*\*Batch processing\*\* for large datasets

3\. \*\*Enable GPU\*\* if available (set device: "cuda" in config)

4\. \*\*Monitor performance\*\* with PerformanceMonitor



---



\### Testing



Run tests:

```bash

pytest tests/ -v

```



With coverage:

```bash

pytest tests/ --cov=. --cov-report=html

```



---



\### Contributing



See CONTRIBUTING.md for guidelines.

