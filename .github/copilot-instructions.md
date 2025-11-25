# Repo-specific guidance for AI assistants

## Big picture
- This project uses `uv` as its package manager; dependencies are in `pyproject.toml`.
- Source code lives under `src/<package_name>/`; tests under `tests/`.
- Notebooks for exploration/documentation are in `notebooks/`.

## Environment & workflows
- **Setup:** `uv sync` installs dependencies into `.venv/`
- **Run Python:** `uv run python <script.py>` or activate `.venv/bin/activate`
- **Run tests:** `uv run pytest`
- **Lint:** `uv run ruff check src/`
- **Format:** `uv run black src/ tests/`

## Coding patterns & conventions
- Python formatting uses `black` (line length 88) and `ruff` for linting.
- Match existing style: type hints, dataclasses, clear docstrings.
- Keep reusable logic in library modules under `src/`; notebooks import from there.
- Prefer extending existing helpers over duplicating logic.

## External dependencies & data handling
- Large data files should NOT be committed; use `.gitignore` patterns.
- Configure data paths via environment variables or config files.
- Document data sources and download procedures in README.

## Productivity tips
- There is no dedicated test suite initially; add tests as features develop.
- Use the devcontainer for consistent environment across machines.
- Keep notebooks clean: restart kernel and run all before committing.
