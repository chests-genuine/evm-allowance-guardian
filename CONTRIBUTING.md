# Contributing

Thanks for your interest!

## Workflow
1. Fork → feature branch → PR.
2. Keep PRs small and focused.
3. Add/adjust tests for behavior changes.

## Commit style (Conventional Commits)
- `feat:` new feature
- `fix:` bug fix
- `docs:` docs only
- `test:` tests only
- `chore:` tooling, CI, deps

Examples:
- `feat(cli): add --json output`
- `fix(allowances): handle missing decimals`
- `chore(ci): enable Python 3.13`

## Issues
- Use the template.
- Provide chain, token, spender, and exact command/output.

## Code Style
- Python ≥ 3.10
- Run `ruff` and `pytest` before committing.

```bash
pip install -e .[dev]
ruff check .
pytest -q
