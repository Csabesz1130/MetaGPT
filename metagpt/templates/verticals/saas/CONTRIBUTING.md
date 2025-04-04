# Contributing to SaaS Template

Thank you for your interest in contributing to the SaaS Template! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project.

## How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/saas-template.git
cd saas-template
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

## Code Style

We use the following tools to maintain code quality:

- Black for code formatting
- isort for import sorting
- mypy for type checking
- flake8 for linting

Run the following commands before committing:

```bash
black .
isort .
mypy .
flake8
```

## Testing

1. Run tests:
```bash
pytest
```

2. Generate coverage report:
```bash
pytest --cov=src tests/
```

## Documentation

1. Update docstrings following Google style
2. Update README.md if necessary
3. Add new features to the documentation

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the documentation if needed
3. The PR must pass all tests
4. The PR must follow the code style guidelines
5. The PR must be reviewed by at least one maintainer

## Questions?

Feel free to open an issue if you have any questions or need clarification. 