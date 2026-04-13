"""
Component Loader Module
Load and manage solar panels and batteries from CSV datasets.
"""

import pandas as pd
import os
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SolarPanel:
    """Represents a solar panel with its specifications."""
    panel_id: str
    rated_power_w: int
    efficiency: float
    area_m2: float
    cost_per_panel: float
    lifetime_years: int
    degradation_rate: float

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'panel_id': self.panel_id,
            'rated_power_w': self.rated_power_w,
            'efficiency': self.efficiency,
            'area_m2': self.area_m2,
            'cost_per_panel': self.cost_per_panel,
            'lifetime_years': self.lifetime_years,
            'degradation_rate': self.degradation_rate
        }


@dataclass
class Battery:
    """Represents a battery with its specifications."""
    battery_id: str
    capacity_kwh: float
    max_charge_kw: float
    max_discharge_kw: float
    efficiency: float
    cost: float
    cycle_life: int
    depth_of_discharge: float

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'battery_id': self.battery_id,
            'capacity_kwh': self.capacity_kwh,
            'max_charge_kw': self.max_charge_kw,
            'max_discharge_kw': self.max_discharge_kw,
            'efficiency': self.efficiency,
            'cost': self.cost,
            'cycle_life': self.cycle_life,
            'depth_of_discharge': self.depth_of_discharge
        }


class ComponentLoader:
    """Loads and manages component datasets."""

    def __init__(self, dataset_dir: str):
        """
        Initialize the component loader.
        
        Args:
            dataset_dir: Path to the Datasets folder
        """
        self.dataset_dir = dataset_dir
        self.solar_panels: List[SolarPanel] = []
        self.batteries: List[Battery] = []

    def load_solar_panels(self) -> List[SolarPanel]:
        """
        Load solar panel dataset from CSV.
        
        Returns:
            List of SolarPanel objects
            
        Raises:
            FileNotFoundError: If solar panel CSV not found
        """
        csv_path = os.path.join(self.dataset_dir, 'solar_panel_dataset.csv')
        
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Solar panel dataset not found at {csv_path}")
        
        df = pd.read_csv(csv_path)
        self.solar_panels = []
        
        for idx, row in df.iterrows():
            panel = SolarPanel(
                panel_id=str(row['panel_id']),
                rated_power_w=int(row['rated_power_w']),
                efficiency=float(row['efficiency']),
                area_m2=float(row['area_m2']),
                cost_per_panel=float(row['cost_per_panel']),
                lifetime_years=int(row['lifetime_years']),
                degradation_rate=float(row['degradation_rate'])
            )
            self.solar_panels.append(panel)
        
        return self.solar_panels

    def load_batteries(self) -> List[Battery]:
        """
        Load battery dataset from CSV.
        
        Returns:
            List of Battery objects
            
        Raises:
            FileNotFoundError: If battery CSV not found
        """
        csv_path = os.path.join(self.dataset_dir, 'battery_dataset.csv')
        
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Battery dataset not found at {csv_path}")
        
        df = pd.read_csv(csv_path)
        self.batteries = []
        
        for idx, row in df.iterrows():
            battery = Battery(
                battery_id=str(row['battery_id']),
                capacity_kwh=float(row['capacity_kwh']),
                max_charge_kw=float(row['max_charge_kw']),
                max_discharge_kw=float(row['max_discharge_kw']),
                efficiency=float(row['efficiency']),
                cost=float(row['cost']),
                cycle_life=int(row['cycle_life']),
                depth_of_discharge=float(row['depth_of_discharge'])
            )
            self.batteries.append(battery)
        
        return self.batteries

    def get_solar_panels(self) -> List[SolarPanel]:
        """Get loaded solar panels."""
        if not self.solar_panels:
            self.load_solar_panels()
        return self.solar_panels

    def get_batteries(self) -> List[Battery]:
        """Get loaded batteries."""
        if not self.batteries:
            self.load_batteries()
        return self.batteries

    def get_panel_by_id(self, panel_id: str) -> Optional[SolarPanel]:
        """Get a specific solar panel by ID."""
        if not self.solar_panels:
            self.load_solar_panels()
        return next((p for p in self.solar_panels if p.panel_id == panel_id), None)

    def get_battery_by_id(self, battery_id: str) -> Optional[Battery]:
        """Get a specific battery by ID."""
        if not self.batteries:
            self.load_batteries()
        return next((b for b in self.batteries if b.battery_id == battery_id), None)

    def print_summary(self):
        """Print a summary of loaded components."""
        if not self.solar_panels:
            self.load_solar_panels()
        if not self.batteries:
            self.load_batteries()

        print("\n" + "="*60)
        print("COMPONENT DATASET SUMMARY")
        print("="*60)
        
        print(f"\n📊 SOLAR PANELS: {len(self.solar_panels)} models")
        print(f"   Power Range: {min(p.rated_power_w for p in self.solar_panels)}W - {max(p.rated_power_w for p in self.solar_panels)}W")
        print(f"   Cost Range: ₹{min(p.cost_per_panel for p in self.solar_panels):,.0f} - ₹{max(p.cost_per_panel for p in self.solar_panels):,.0f}")
        
        print(f"\n🔋 BATTERIES: {len(self.batteries)} models")
        print(f"   Capacity Range: {min(b.capacity_kwh for b in self.batteries)}kWh - {max(b.capacity_kwh for b in self.batteries)}kWh")
        print(f"   Cost Range: ₹{min(b.cost for b in self.batteries):,.0f} - ₹{max(b.cost for b in self.batteries):,.0f}")
        print("\n" + "="*60 + "\n")
