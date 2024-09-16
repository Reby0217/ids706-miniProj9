# Ensure pip is upgraded and install all required packages
install:
	pip install --upgrade pip && pip install -r requirements.txt

# Setup the virtual environment
setup:
	python3 -m venv venv
	@echo "Virtual environment created. Activate with: 'source venv/bin/activate'"
	. venv/bin/activate && pip install --upgrade pip

# Run tests within the virtual environment
test:
	. venv/bin/activate && PYTHONPATH=. pytest


# Lint the source code and tests
lint:
	. venv/bin/activate && flake8 src tests

# Format all Python files
format:
	. venv/bin/activate && black .

# Lint using pylint, disable specific checks for speed, and use ruff if desired
pylint:
	. venv/bin/activate && pylint --disable=R,C --disable=unnecessary-pass --ignore-patterns=test_.*?py *.py

# Lint using ruff, which is faster than pylint (uncomment if using ruff)
ruff:
	. venv/bin/activate && ruff check .

# Run container linting on Dockerfile
container-lint:
	docker run --rm -i hadolint/hadolint < Dockerfile

# Clean the virtual environment
clean:
	rm -rf venv

# Format and lint code
refactor: format lint

# Deploy the application (replace with actual deploy commands)
deploy:
	@echo "Deploy the app"

# Run all major tasks: install, lint, test, format, and deploy
all: install setup lint test format deploy
