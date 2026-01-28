
# Synthetic Load

This folder contains scripts and data for generating and validating synthetic load profiles using Markov models and clustering.

## Folder Structure
```
synthetic_load/
├── data_preprocessing.py
├── markov_model.py
├── markov_transition.npy
├── metadata.json
├── README.md
├── synthetic_load_test.ipynb
├── train_kmeans.py
├── validate_model.py
├── kmeans_model.pkl
├── load_comparison.png
├── __pycache__/
└── .ipynb_checkpoints/
```

## Main Files
- `data_preprocessing.py`: Preprocesses raw data for modeling
- `markov_model.py`: Markov model for load synthesis
- `train_kmeans.py`: Clustering for load profiles
- `validate_model.py`: Model validation scripts
- `synthetic_load_test.ipynb`: Jupyter notebook for testing
- `markov_transition.npy`, `metadata.json`: Model data

## Data
- Place raw smart meter CSV files in `../Datasets/Smart_meter/`.
- Preprocessed outputs are saved in `../outputs/`.


## Order of Running Files
1. Run `data_preprocessing.py` to preprocess raw smart meter data and generate hourly profiles.
2. Train the Markov model and clusters:
	- `train_kmeans.py` (for clustering)
	- `markov_model.py` (for Markov model training and synthetic load generation)
3. Validate the synthetic load model:
	- `validate_model.py` (compare synthetic and real profiles, compute error metrics)
4. (Optional) Use `synthetic_load_test.ipynb` for interactive analysis and visualization.
5. Check `outputs/` for generated data and results.

## Notes
- Outliers (high energy usage) are retained for battery optimization steps.
- Missing values are handled via interpolation or robust methods.
- You can combine multiple CSVs for better model accuracy.

---
For questions or improvements, contact the project maintainer.
