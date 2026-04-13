"""
Optimization Engine for Intelligent Energy Management System (IEMS)

This module provides:
- Component data loading (solar panels, batteries)
- Design space generation (valid system configurations)
- Objective function evaluation (fitness scoring)
- Genetic Algorithm optimization (GA-based sizing)
- CLI interface for user interaction

Main entry point: main.py
"""

from .component_loader import ComponentLoader, SolarPanel, Battery
from .design_space import DesignSpace, CandidateSolution
from .objective_functions import ObjectiveFunction
from .optimizer import GeneticAlgorithmOptimizer

__all__ = [
    'ComponentLoader',
    'SolarPanel',
    'Battery',
    'DesignSpace',
    'CandidateSolution',
    'ObjectiveFunction',
    'GeneticAlgorithmOptimizer'
]

__version__ = '1.0.0'
