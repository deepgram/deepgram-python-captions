# Contributing Guidelines

Thank you for your interest in contributing to `deepgram-captions`! We welcome
contributions of all kinds — bug fixes, new converter support, documentation
improvements, and test coverage increases.

Please take a moment to review this document before submitting a pull request.

## Code of Conduct

By participating in this project you agree to abide by our
[Code of Conduct](.github/CODE_OF_CONDUCT.md). Please read it before
contributing.

## Types of Contributions

### Bug Fixes

- If you find a bug, please first report it using
  [GitHub Issues](https://github.com/deepgram/deepgram-python-captions/issues/new).
- Issues confirmed as bugs are labelled `bug`.
- If you'd like to fix a bug yourself, send a Pull Request from your fork and
  reference the Issue number.
- Include a test that isolates the bug and verifies the fix.

### New Features / Converters

- If you'd like to add support for a new speech-to-text provider, or add a
  new feature, describe the problem or use case in a
  [GitHub Issue](https://github.com/deepgram/deepgram-python-captions/issues/new).
- Issues identified as feature requests are labelled `enhancement`.
- Wait for feedback from the project maintainers before spending significant
  time writing code — some ideas may not align with the project's current
  direction.

### Tests, Documentation, Refactoring

- If you think test coverage could be improved, the documentation could be
  clearer, or you have an alternative implementation that has advantages,
  we are happy to hear it.
- For trivial changes, go ahead and open a Pull Request directly.
- For larger changes, open a GitHub Issue to discuss first.

We also welcome contributions to any existing issues labelled
`good first issue`.

---

## Setting Up Your Development Environment

### Prerequisites

- Python 3.10 or higher
- `pip` (or `pipx` for isolated tool installs)
- `git`

### Steps

1. **Fork** the repository on GitHub.

2. **Clone** your fork locally:

   ```bash
   git clone https://github.com/YOUR_USERNAME/deepgram-python-captions.git
   cd deepgram-python-captions
   ```

3. **Install** the package in editable mode with dev dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

   This installs `pytest`, `ruff`, and `mypy` alongside the package itself.

4. **Verify** your setup by running the tests:

   ```bash
   make test
   ```

---

## Running Tests

Tests live in the `test/` directory and use [pytest](https://pytest.org).

```bash
# Run all tests
make test

# Or directly
pytest test/ -v

# Run a single test file
pytest test/test_deepgram.py -v
```

All tests must pass before a pull request will be merged.

---

## Code Style

This project uses [ruff](https://docs.astral.sh/ruff/) for linting and
formatting, and [mypy](https://mypy.readthedocs.io/) for static type checking.

### Formatting

```bash
# Format all source files
make format

# Check formatting without making changes
make format-check
```

Line length is set to **120 characters**.

### Linting

```bash
# Run linter
make lint

# Auto-fix lint issues
make lint-fix
```

### Type Checking

All public functions and methods should include type annotations. We use
`from __future__ import annotations` in all source files for forward reference
support.

```bash
# Run mypy
make typecheck
```

### Run All Checks

```bash
# format-check + lint + typecheck (no tests)
make check

# Full development cycle: lint-fix + format + test
make dev
```

---

## Adding a New Converter

A converter is any object that implements the following duck-typing interface:

### Required

```python
def get_lines(self, line_length: int) -> list[list[dict]]:
    ...
```

Return a list of caption cue groups. Each group is a list of word dicts
containing at minimum:

| Key               | Type    | Description                                         |
| ----------------- | ------- | --------------------------------------------------- |
| `word`            | `str`   | Word text (used as fallback display text)           |
| `punctuated_word` | `str`   | Punctuated form of the word (preferred for display) |
| `start`           | `float` | Start time in seconds                               |
| `end`             | `float` | End time in seconds                                 |
| `speaker`         | `int`   | (Optional) Speaker index for diarisation            |

If `punctuated_word` is absent, `word` is used instead. If `speaker` is
present on any word in the first cue group, speaker labels are automatically
emitted by the formatters.

### Optional

```python
def get_headers(self) -> list[str]:
    ...
```

Return a list of strings to be joined as a `NOTE` block in WebVTT output
(placed after the `WEBVTT` header line). If this method is absent, no `NOTE`
block is generated.

### Placement

Add new converters to `deepgram_captions/converters.py` and export them from
`deepgram_captions/__init__.py`. Add tests in `test/` using a representative
fixture JSON response from the provider.

### Example Skeleton

```python
from __future__ import annotations

from typing import Any

from .helpers import chunk_array


class MyProviderConverter:
    """Convert a MyProvider speech-to-text response into caption lines.

    Args:
        response: The full MyProvider API response dict.
    """

    def __init__(self, response: dict[str, Any]) -> None:
        self.response = response

    def get_lines(self, line_length: int = 8) -> list[list[dict[str, Any]]]:
        """Return caption lines as groups of normalised word dicts."""
        words = [
            {
                "word": w["token"],
                "punctuated_word": w.get("display", w["token"]),
                "start": w["start_time"],
                "end": w["end_time"],
            }
            for w in self.response.get("words", [])
        ]
        return chunk_array(words, line_length)
```

---

## Commit Message Convention

We follow the [Conventional Commits](https://www.conventionalcommits.org/)
specification. All commit messages must use one of the following types:

| Type       | When to use                                                        |
| ---------- | ------------------------------------------------------------------ |
| `feat`     | A new feature or converter                                         |
| `fix`      | A bug fix                                                          |
| `docs`     | Documentation changes only                                         |
| `style`    | Code style / formatting changes (no logic change)                  |
| `refactor` | Code restructuring without feature changes or bug fixes            |
| `perf`     | Performance improvements                                           |
| `test`     | Adding or improving tests                                          |
| `chore`    | Maintenance tasks, dependency updates, tooling changes             |
| `ci`       | CI/CD configuration changes                                        |

**Format:**

```
<type>(<optional scope>): <short summary>

<optional body>

<optional footer>
```

**Examples:**

```
feat(converters): add RevAI converter
fix(srt): correct millisecond precision for timestamps > 1 hour
docs(readme): add streaming transcription example
test(assemblyai): add fixture for utterances response
chore(deps): upgrade ruff to 0.11
```

---

## Pull Request Process

1. **Fork** the repository and create a new branch from `main`.

   ```bash
   git checkout -b feat/my-new-converter
   ```

2. **Make your changes** following the code style and commit conventions above.

3. **Run the full check suite** before opening a PR:

   ```bash
   make dev     # lint-fix + format + test
   make check   # format-check + lint + typecheck
   ```

4. **Push** your branch to your fork:

   ```bash
   git push origin feat/my-new-converter
   ```

5. **Open a Pull Request** from your branch to `main` in the upstream
   repository. Include:
   - A clear description of what the PR does and why.
   - A reference to the related Issue (if applicable): `Closes #123`.
   - Any notes on testing approach or edge cases.

6. A maintainer will review your PR. You may be asked to make changes before
   it is merged.

---

## Acceptance Criteria

For a contribution to be accepted:

- The test suite must pass: `make test`.
- Code must pass all quality checks: `make check`.
- Commit messages must follow the Conventional Commits format.
- New public APIs must include type annotations and docstrings.
- Related Issues should be mentioned in the PR description.

---

## Getting Help

If you have questions about contributing, feel free to:

- [Open a GitHub Issue](https://github.com/deepgram/deepgram-python-captions/issues/new)
- [Join the Deepgram Discord Community](https://discord.gg/xWRaCDBtW4)
- [Join GitHub Discussions](https://github.com/orgs/deepgram/discussions)
