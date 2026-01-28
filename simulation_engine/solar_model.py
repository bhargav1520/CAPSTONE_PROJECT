# solar_model.py
# This module handles the modeling of solar PV generation for the simulation engine.

import numpy as np

class SolarModel:
    """
    Solar PV Generation Model
    -------------------------
    Computes hourly solar energy generation (kWh)
    """

    def __init__(
        self,
        solar_capacity_kw,
        efficiency=0.18,
        irradiance_profile=None
    ):
        """
        Parameters
        ----------
        solar_capacity_kw : float
            Installed PV capacity in kW
        efficiency : float
            Overall system efficiency (default 18%)
        irradiance_profile : array-like (length 24)
            Normalized hourly irradiance profile (0–1)
        """
        self.solar_capacity_kw = solar_capacity_kw
        self.efficiency = efficiency

        # Default clear-sky irradiance profile
        if irradiance_profile is None:
            self.irradiance_profile = np.array([
                0.0, 0.0, 0.0, 0.0, 0.05, 0.15,
                0.35, 0.55, 0.75, 0.90, 1.00, 0.95,
                0.85, 0.70, 0.55, 0.35, 0.20, 0.10,
                0.05, 0.0, 0.0, 0.0, 0.0, 0.0
            ])
        else:
            self.irradiance_profile = np.array(irradiance_profile)

    # --------------------------------------------------
    def get_generation(self, hour):
        """
        Returns solar generation at a given hour

        Parameters
        ----------
        hour : int
            Hour index (0–23)

        Returns
        -------
        float
            Solar generation (kWh)
        """
        h = hour % 24
        generation = (
            self.solar_capacity_kw *
            self.irradiance_profile[h] *
            self.efficiency
        )
        return generation

    # --------------------------------------------------
    def get_daily_energy(self):
        """
        Returns total daily solar energy (kWh)
        """
        daily_energy = sum(
            self.get_generation(h) for h in range(24)
        )
        return daily_energy
