
# Simulation Engine

This folder contains the core simulation modules for the project, including:
- Battery model
- Energy flow logic
- Load and solar models
- Simulation runner and tests

## File Overview & Main Functions

### battery_model.py
**BatteryModel**
- `__init__`: Initialize battery parameters (capacity, charge/discharge limits, efficiencies, initial SoC)
- `charge(energy_kwh)`: Charge the battery, returns energy stored
- `discharge(energy_kwh)`: Discharge the battery, returns energy supplied
- `get_soc()`: Get current state of charge (kWh)
- `get_soc_percent()`: Get state of charge as a percentage

### energy_flow.py
**EnergyFlow**
- `__init__`: Set up with load, solar, and battery models
- `simulate(hours)`: Simulate hour-by-hour energy flow (solar, battery, grid)
- `get_results()`: Retrieve simulation results as a dictionary

### load_model.py
**LoadModel**
- `__init__`: Load hourly load data from CSV (synthetic or real)
- `get_load(hour)`: Get load for a specific hour
- `get_total_energy()`: Total energy consumption
- `get_peak_load()`: Peak hourly load
- `get_profile_length()`: Number of hours in profile

### solar_model.py
**SolarModel**
- `__init__`: Initialize solar PV parameters and irradiance profile
- `get_generation(hour)`: Get solar generation for a given hour
- `get_daily_energy()`: Total daily solar energy

### simulator.py
**HybridSystemSimulator**
- `__init__`: Set up all models and energy flow
- `run(hours)`: Run the full simulation
- `export_results(output_csv)`: Export results to CSV
- `summary()`: Return key system metrics (load, grid, solar, SoC)

### economics.py
- `calculate_cost(grid_energy_kwh, tariff_per_kwh)`: Calculate cost of grid energy


## Typical Order of Running Files
1. Prepare your input data (e.g., outputs/cleaned_hourly.csv).
2. Run test scripts to validate modules (optional):
	- `python -m simulation_engine.energy_flow_test`
	- `python -m simulation_engine.battery_model_test`
	- `python -m simulation_engine.solar_model_test`
	- `python -m simulation_engine.load_module_test`
3. Run the main simulation:
	- Use `HybridSystemSimulator` in `simulator.py` (see example usage in that file)
	- Or create your own script using the models and `EnergyFlow`
4. Export and analyze results as needed.

See the main project README for usage instructions and module integration.
