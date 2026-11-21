# Trigonometric Visualisation

- Run: `bokeh serve src/trig_visualisation/viz.py`, then open `http://localhost:5006/viz`.
- Test: `python -m pytest`. It starts the app on a free port and opens a session; no tests are opt-in.
- Lint (as CI does): `actionlint`, `shellcheck .githooks/pre-commit scripts/*.sh`, `black --check .`, `flake8 .`.
- Docs: `README.md` for setup.
- Before each commit, check the staged diff for secrets. The pre-commit hook needs `git config core.hooksPath .githooks`.
