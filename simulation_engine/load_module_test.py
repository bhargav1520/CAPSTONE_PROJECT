"""Lightweight harness to exercise LoadModel directly.

Run from project root:
    python -m simulation_engine.load_module_test

Or directly from the simulation_engine folder:
    python load_module_test.py
"""

import os
import sys

try:  # Module mode: python -m simulation_engine.load_module_test
    from .load_model import LoadModel
except ImportError:  # Script mode: python load_module_test.py from simulation_engine/
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from load_model import LoadModel

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_path = os.path.join(PROJECT_ROOT, "outputs", "monthly_synthetic_500kWh_30days.csv")

load_model = LoadModel(
    load_source="synthetic",
    file_path=load_path
)
min_load = min(load_model.get_load(h) for h in range(load_model.get_profile_length()))
hourly = [load_model.get_load(i) for i in range(load_model.get_profile_length())]
print("Total Energy:", sum(hourly))
print("Peak Load:", max(hourly))
print("minimum load:",min_load)
print("Hour 10 Load:", load_model.get_load(10))

# python -m simulation_engine.load_module_test