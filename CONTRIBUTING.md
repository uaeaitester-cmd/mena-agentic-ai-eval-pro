\# Contributing to MENA Bias Evaluation Pipeline



Thank you for your interest in contributing! 🎉



\## How to Contribute



\### 1. Fork and Clone

```bash

git clone https://github.com/yourusername/mena-bias-evaluation.git

cd mena-bias-evaluation

```



\### 2. Create Virtual Environment

```bash

python -m venv venv

venv\\Scripts\\activate  # Windows

pip install -r requirements-dev.txt

```



\### 3. Create a Branch

```bash

git checkout -b feature/your-feature-name

```



\### 4. Make Changes



\- Write clean, documented code

\- Follow PEP 8 style guide

\- Add tests for new features

\- Update documentation



\### 5. Run Tests

```bash

pytest tests/ -v

black .

flake8 .

```



\### 6. Commit Changes

```bash

git add .

git commit -m "Add: your feature description"

```



\### 7. Push and Create PR

```bash

git push origin feature/your-feature-name

```



Then create a Pull Request on GitHub.



\## Code Standards



\- \*\*Style\*\*: Black formatter, 100 character line length

\- \*\*Linting\*\*: Flake8 compliant

\- \*\*Type hints\*\*: Use type annotations

\- \*\*Docstrings\*\*: Google style

\- \*\*Tests\*\*: Minimum 80% coverage



\## Commit Message Format

```

<type>: <description>



\[optional body]

```



Types: Add, Fix, Update, Refactor, Docs, Test



\## Questions?



Open an issue or contact maintainers.

