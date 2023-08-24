# autoQA

This repository contains the automated testing suite for Webcursos. This QA environment was developed against Moodle 4.1 and RemUI

## How to use:

1. Copy the `env.py-dist` file to `env.py` and populate the fields
2. Setup a python environment (`python3 -m venv venv`)
3. Load the environment (`source venv/bin/activate`)
4. Install requirements (`pip install -r requirements`)
5. Run (`python autoQA.py`)