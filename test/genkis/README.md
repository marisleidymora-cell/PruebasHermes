# Genkis tests for PruebasHermes

This directory contains test case definitions and a minimal pytest loader adapted to the "Genkis" structure agreed for this project.

Structure
- test/genkis/cases/  -> JSON files, one per test case definition
- test/genkis/test_genkis_loader.py -> pytest-compatible loader that validates case schema and marks automatable tests as pending implementation

How to run

1. Install test dependencies (pytest):

   pip install -U pytest

2. Run the Genkis test loader (validates case schema):

   pytest test/genkis/test_genkis_loader.py

Notes
- The current loader validates the presence of required fields in each JSON case file. For automatable cases, the actual automation implementation is pending; the tests are marked as skipped so CI can still validate structure.
- Next steps: implement adapters to call the real application endpoints (HTTP requests or UI automation) for automatable cases and update the loader to execute assertions against responses.
