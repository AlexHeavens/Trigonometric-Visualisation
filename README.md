# Trigonomentric Visualisation Demo
A simple interactive demo of trigonometric functions.

# Installation
## Pre-requisites
* Python 3.7

## Installation Process
```
pip3.7 install --user requirements.txt
```

# Running the Visualisation
```
bokeh serve src/trig_visualisation/viz.py
```
Then open `http://localhost:5006/viz` in a web browser.

# Setting up for development
The `virtualenv` module is a pre-requisite for development:
```
pip3.7 install --user virtualenv
```

Then:
```
python3.7 -m virtualenv --python=python3.7 .venv3.7 || true
source .venv3.7/bin/activate
pip install --requirement requirements-dev.txt
pre-commit install
```