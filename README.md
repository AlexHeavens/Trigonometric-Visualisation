# Trigonometric Visualisation

A small interactive demo of sine, cosine and tangent, built with Bokeh. A slider sets an angle; the
unit-circle triangle and the three function plots follow it. It is a demo to run locally, not a
library and not a hosted service.

## Contents

- `src/trig_visualisation/viz.py`: the Bokeh app.
- `tests/`: tests that serve the app and open a session.
- `requirements.txt`, `requirements-dev.txt`: pinned dependencies for the app, and for tests and linters.
- `scripts/install-gitleaks.sh`, `pins/gitleaks/`: the pinned secrets scanner.
- `.githooks/pre-commit`: blocks a commit whose staged changes hold a secret.
- `.github/`: CI (lint, tests, full-history secret scan) and Dependabot.

## Setup

Prerequisites: Python 3.14 (the version CI uses), `curl` and `tar`.

```
python3 -m venv .venv
source .venv/bin/activate
pip install --requirement requirements-dev.txt   # use requirements.txt to run the app only
scripts/install-gitleaks.sh                      # the pre-commit hook needs gitleaks
git config core.hooksPath .githooks
bokeh serve src/trig_visualisation/viz.py
```

Then open `http://localhost:5006/viz` in a web browser.

## Tests

```
python -m pytest
actionlint
shellcheck .githooks/pre-commit scripts/*.sh
black --check .
flake8 .
```

The tests start `bokeh serve` on a free port and open a session, as a browser does. CI runs the same commands.
No tests are opt-in.
