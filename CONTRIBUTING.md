# Contributing

Thanks for your interest!

## Dev setup

```bash
git clone https://github.com/sandeepmothukuri/promptshield
cd promptshield
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
pytest
```

## Adding a detector

1. Create a new file in `promptshield/detectors/` or add to an existing one.
2. Subclass `Detector` (or use `RegexDetector` for simple cases).
3. Add it to the appropriate `*_DETECTORS` list.
4. Add tests in `tests/`.

## Pull requests

- Keep changes focused.
- Add tests.
- Run `pytest` before pushing.
