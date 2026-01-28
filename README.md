# IEMS Project

This project provides a simulation framework for energy management, including synthetic load generation, simulation engine, and data processing tools.


## Folder Structure

```
IEMS/
├── .gitignore               # Git ignore rules (excludes Datasets/ and other files)
├── requirements.txt          # Python dependencies for the project
├── Datasets/                 # Raw data (not tracked in git)
│   └── Smart_meter/          # Smart meter CSV files (raw input)
├── outputs/                  # Processed data and intermediate outputs
│   ├── cleaned_hourly.csv    # Cleaned hourly load data
│   └── daily_profiles.npy    # Numpy array of daily load profiles
├── results/                  # Final simulation results
│   └── simulation_outputs.csv# Output from simulation runs
├── simulation_engine/        # Core simulation modules and tests
│   ├── battery_model.py      # Battery storage model
│   ├── battery_model_test.py # Battery model test script
│   ├── economics.py          # Economic calculations (cost, tariff)
│   ├── energy_flow.py        # Energy flow logic (solar, battery, grid)
│   ├── energy_flow_test.py   # Energy flow test script
│   ├── load_model.py         # Load profile model
│   ├── load_module_test.py   # Load model test script
│   ├── simulator.py          # Main simulation runner
│   ├── simulator_test.py     # Simulator test script
│   ├── solar_model.py        # Solar PV generation model
│   ├── solar_model_test.py   # Solar model test script
│   ├── tempCodeRunnerFile.py # Temporary file (can be ignored)
│   └── __pycache__/          # Python cache files
├── synthetic_load/           # Synthetic load generation and validation
│   ├── data_preprocessing.py # Preprocess raw data for modeling
│   ├── markov_model.py       # Markov model for synthetic load
│   ├── markov_transition.npy # Markov model transition matrix
│   ├── metadata.json         # Metadata for synthetic load
│   ├── README.md             # Details for synthetic load module
│   ├── synthetic_load_test.ipynb # Jupyter notebook for testing
│   ├── train_kmeans.py       # KMeans clustering for load profiles
│   ├── validate_model.py     # Validation of synthetic load
│   ├── kmeans_model.pkl      # Saved KMeans model
│   ├── load_comparison.png   # Visualization of load comparison
│   ├── __pycache__/          # Python cache files
│   └── .ipynb_checkpoints/   # Jupyter notebook checkpoints
└── ...
```

## Folder Specifications
- **Datasets/**: Place all raw smart meter data here. This folder is excluded from git to save space.
- **outputs/**: Contains processed data, such as cleaned hourly load profiles and numpy arrays.
- **results/**: Stores final outputs from simulation runs for analysis and reporting.
- **simulation_engine/**: Main simulation code, including models for battery, solar, load, and the simulation runner. Also contains test scripts for each module.
- **synthetic_load/**: Scripts and data for generating synthetic load profiles using Markov models and clustering, as well as validation and analysis tools.


## Notes
- The `Datasets/` folder is excluded from version control due to large file sizes. Place your raw data here.
- See `simulation_engine/README.md` and `synthetic_load/README.md` for module-specific details.
- Install dependencies from `requirements.txt`.

## Getting Started
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Add your data to `Datasets/Smart_meter/`.
4. Run scripts in `synthetic_load/` and `simulation_engine/` as needed.

---
