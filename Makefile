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
	@echo "Running tests in tests/test_lib.py..." 
	@echo "Running tests in tests/test_script.py..." 
	. venv/bin/activate && PYTHONPATH=. pytest tests/ -q
	. venv/bin/activate && pytest --nbval src/individual_proj_1.ipynb


# Generate an HTML coverage report to inspect coverage in detail
coverage:
	. venv/bin/activate && PYTHONPATH=src pytest --cov=src --cov-report=html tests/
	@echo "Open the coverage report at: htmlcov/index.html"
    
# Lint the source code and tests
lint:
	. venv/bin/activate && ruff check src tests

# Format all Python files
format:
	. venv/bin/activate && black .

# Clean the virtual environment
clean:
	rm -rf venv

# Run all major tasks: install, setup, lint, test, format
all: install setup lint test format
