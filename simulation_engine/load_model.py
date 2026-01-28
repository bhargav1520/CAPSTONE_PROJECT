import numpy as np
import pandas as pd
import os

class LoadModel:
    """
    Load Model
    ----------
    Provides hourly electrical load (kWh)
    """

    def __init__(self, load_source="synthetic", file_path=None):
        """
        Parameters
        ----------
        load_source : str
            'synthetic' or 'real'
        file_path : str
            Path to CSV file containing hourly load
        """
        self.load_source = load_source
        self.file_path = file_path
        self.hourly_load = None

        self._load_data()

    # --------------------------------------------------
    def _load_data(self):
        """
        Load hourly load data from CSV
        """
        if self.file_path is None:
            raise ValueError("file_path must be provided")

        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Load file not found: {self.file_path}")

        df = pd.read_csv(self.file_path)

        # Expect column: t_kWh or load_kWh
        if "t_kWh" in df.columns:
            self.hourly_load = df["t_kWh"].values
        elif "load_kWh" in df.columns:
            self.hourly_load = df["load_kWh"].values
        else:
            raise ValueError("CSV must contain 't_kWh' or 'load_kWh' column")

    # --------------------------------------------------
    def get_load(self, hour):
        """
        Returns load at a given hour

        Parameters
        ----------
        hour : int
            Hour index (0, 1, 2, ...)

        Returns
        -------
        float
            Load in kWh
        """
        return self.hourly_load[hour]

    # --------------------------------------------------
    def get_total_energy(self):
        """
        Returns total energy consumption (kWh)
        """
        return np.sum(self.hourly_load)

    # --------------------------------------------------
    def get_peak_load(self):
        """
        Returns peak load (kW equivalent for 1 hour)
        """
        return np.max(self.hourly_load)

    # --------------------------------------------------
    def get_profile_length(self):
        """
        Returns number of hours in load profile
        """
        return len(self.hourly_load)
