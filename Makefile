.PHONY: install lint format typecheck test coverage serve benchmark screenshots clean help

help:
	@echo "Available targets:"
	@echo "  install      Install in editable mode with dev deps"
	@echo "  lint         Run ruff linter"
	@echo "  format       Auto-format with ruff"
	@echo "  typecheck    Run mypy"
	@echo "  test         Run pytest"
	@echo "  coverage     Run tests with coverage report"
	@echo "  serve        Start the REST API server (requires [api] extras)"
	@echo "  benchmark    Run attack simulation benchmarks"
	@echo "  screenshots  Regenerate all demo screenshots"
	@echo "  clean        Remove build/cache artifacts"

install:
	pip install -e ".[dev]"
	pre-commit install

lint:
	ruff check .

format:
	ruff format .
	ruff check --fix .

typecheck:
	mypy promptsentinel/

test:
	pytest -v

coverage:
	pytest --cov=promptsentinel --cov-report=term-missing --cov-report=html
	@echo "HTML report: htmlcov/index.html"

serve:
	uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

benchmark:
	python benchmarks/run_benchmarks.py

screenshots:
	python scripts/make_screenshot.py
	python scripts/make_screenshots.py

clean:
	rm -rf build/ dist/ *.egg-info/ .coverage htmlcov/ coverage.xml .mypy_cache/ .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
