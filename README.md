
# IEMS: Integrated Energy Management System

This project provides a modular simulation framework for energy management, including synthetic load generation, simulation engine, and data processing tools. It is designed for research, prototyping, and educational use in distributed energy systems, microgrids, and smart grid analytics.

---

## 📁 Folder Structure

```
IEMS/
├── .gitignore                # Git ignore rules (excludes Datasets/ and other files)
├── requirements.txt          # Python dependencies for the project
├── Datasets/                 # Raw smart meter data (not tracked in git)
│   └── Smart_meter/          # Smart meter CSV files (raw input)
├── outputs/                  # Processed data and intermediate outputs
│   ├── cleaned_hourly.csv    # Cleaned hourly load data
│   └── daily_profiles.npy    # Numpy array of daily load profiles
├── results/                  # Final simulation results
│   └── simulation_outputs.csv# Output from simulation runs
├── simulation_engine/        # Core simulation modules and tests
│   ├── battery_model.py      # Battery storage model
│   ├── economics.py          # Economic calculations (cost, tariff)
│   ├── energy_flow.py        # Energy flow logic (solar, battery, grid)
│   ├── load_model.py         # Load profile model
│   ├── simulator.py          # Main simulation runner
│   ├── solar_model.py        # Solar PV generation model
│   └── ...                   # Additional test scripts and cache
├── synthetic_load/           # Synthetic load generation and validation
│   ├── data_preprocessing.py # Preprocess raw data for modeling
│   ├── markov_model.py       # Markov model for synthetic load
│   ├── train_kmeans.py       # KMeans clustering for load profiles
│   ├── validate_model.py     # Model validation scripts
│   ├── markov_transition.npy # Markov model transition matrix
│   ├── metadata.json         # Metadata for synthetic load
│   ├── synthetic_load_test.ipynb # Jupyter notebook for testing
│   └── README.md             # Details for synthetic load module
└── ...
```

---

## 🧩 Module Descriptions

- **synthetic_load/**: Scripts and data for generating, validating, and analyzing synthetic load profiles using Markov models and clustering.
└── ...
---

## ⚡ Quick Start

1. **Install dependencies**
	- (Populate requirements.txt with needed packages, e.g., numpy, pandas, scikit-learn, matplotlib, joblib)
	- `pip install -r requirements.txt`

2. **Prepare Data**
	- Place raw smart meter CSVs in `Datasets/Smart_meter/`.
	- Run `synthetic_load/data_preprocessing.py` to generate cleaned hourly data and daily profiles.

3. **Generate Synthetic Load**
	- Run `synthetic_load/train_kmeans.py` to cluster daily profiles and save the KMeans model.
	- Run `synthetic_load/markov_model.py` to build the Markov transition matrix and generate synthetic load.

4. **Validate Synthetic Load**
	- Run `synthetic_load/validate_model.py` to compare synthetic and real load profiles, and compute error metrics.

5. **Run Simulation**
	- Use the simulation engine (`simulation_engine/`) to simulate energy flows, battery operation, and solar generation using either real or synthetic load profiles.

---

## 🔄 Example Scenario & Workflow

Suppose you want to simulate a microgrid with a solar-battery system for a residential community, but only have a few months of smart meter data. You want to:

1. **Expand your dataset** by generating realistic synthetic load profiles for a full year.
2. **Test different system sizes** (solar, battery) and tariff structures.
3. **Analyze performance** (cost savings, grid import, battery cycling).

**Workflow:**

1. Place your smart meter CSVs in `Datasets/Smart_meter/`.
2. Run the scripts in `synthetic_load/` to preprocess, cluster, and generate synthetic load.
3. Validate the synthetic load using the provided notebook or scripts.
4. Use the simulation engine to run scenarios with different system parameters.
5. Review results in `results/` and visualize with the provided notebooks.

---

## 🛠️ Extending the Project

- Add new clustering or Markov model variants in `synthetic_load/`.
- Integrate new DER (Distributed Energy Resource) models in `simulation_engine/`.
- Add economic or policy modules for tariff and incentive analysis.

---

## 📄 License & Contact

This project is open for academic and research use. For questions or contributions, contact the project maintainer.
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
