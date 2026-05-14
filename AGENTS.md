# Repository Guidelines

## Project Structure & Module Organization

This is a Python 3.12 project managed with `uv`. Source code lives under `src/`.
Core framework code is in `src/core/`, including the base `Agent`, `Config`,
`HelloAgentsLLM`, messages, and exceptions. Agent implementations live in
`src/agent/`; the current concrete implementation is under
`src/agent/simple_agent/`. Tool scaffolding lives in `src/tools/` and
`src/tools/builtin/`. The root `main.py` is a minimal entry point. There is no
dedicated `tests/` directory yet; add one when introducing automated tests.

## Build, Test, and Development Commands

Use `uv sync` to install dependencies from `pyproject.toml` and `uv.lock`.
Run the default entry point with:

```powershell
uv run python main.py
```

Run syntax checks for changed Python files with:

```powershell
uv run python -m py_compile src\core\agent.py src\agent\simple_agent\simple_agent.py
```

For ad hoc import checks, use short `uv run python -c "..."` commands from the
repository root.

## Coding Style & Naming Conventions

Use 4-space indentation and standard Python naming: `snake_case` for modules,
functions, variables, and file names; `PascalCase` for classes. Keep agent files
grouped by agent type, for example `src/agent/simple_agent/simple_agent.py`.
Prefer explicit type hints on public methods, especially agent lifecycle methods
such as `run()` and `stream_run()`. Keep comments brief and focused on non-obvious
logic.

## Testing Guidelines

No test framework is currently configured. When adding tests, prefer `pytest` and
place tests under `tests/` with names like `test_simple_agent.py`. Mock LLM calls
instead of hitting real providers. At minimum, cover message construction,
history persistence, streaming behavior, and provider configuration resolution.
Run tests with `uv run pytest` once `pytest` is added to the project.

## Commit & Pull Request Guidelines

Existing commits use concise Conventional Commits style, such as `feat: init` and
`feat: finish agent and message model`. Continue using messages like
`feat: add extensible agent`, `fix: correct import path`, or `docs: update readme`.

Pull requests should include a short summary, changed modules, verification
commands run, and any configuration implications. Link related issues when
available. Do not commit `.env`, `.venv/`, `__pycache__/`, API keys, or generated
local cache files.

## Security & Configuration Tips

Keep credentials in `.env` and document new variables in `.env.example`.
`HelloAgentsLLM` supports OpenAI-compatible providers through environment
variables such as `LLM_API_KEY`, `LLM_BASE_URL`, and `LLM_MODEL_ID`. Avoid real API
calls in tests unless explicitly marked as integration tests.
