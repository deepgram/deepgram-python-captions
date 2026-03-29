.PHONY: install test lint format typecheck check clean

install:
	pip install -e ".[dev]"

test:
	pytest test/ -v

lint:
	ruff check deepgram_captions/ test/

lint-fix:
	ruff check --fix deepgram_captions/ test/

format:
	ruff format deepgram_captions/ test/

format-check:
	ruff format --check deepgram_captions/ test/

typecheck:
	mypy deepgram_captions/

check: format-check lint typecheck

dev: lint-fix format test
