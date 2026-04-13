"""
Genetic Algorithm Optimizer
Optimize solar system size and battery capacity using GA.
"""

import random
import copy
import math
from typing import List, Dict, Tuple, Optional
from .design_space import CandidateSolution, DesignSpace
from .objective_functions import ObjectiveFunction


class GeneticAlgorithmOptimizer:
    """Genetic Algorithm for system optimization."""

    def __init__(
        self,
        design_space: DesignSpace,
        objective_function: ObjectiveFunction,
        budget: float,
        population_size: int = 30,
        generations: int = 50,
        mutation_rate: float = 0.1,
        crossover_rate: float = 0.8,
        elite_percentage: float = 0.1,
        random_seed: Optional[int] = None
    ):
        """
        Initialize GA optimizer.
        
        Args:
            design_space: DesignSpace instance
            objective_function: ObjectiveFunction instance
            budget: Budget constraint in ₹
            population_size: Number of individuals per generation (20-50)
            generations: Number of generations to evolve (30-100)
            mutation_rate: Probability of mutation (0-1)
            crossover_rate: Probability of crossover (0-1)
            elite_percentage: Percentage of best individuals to preserve
            random_seed: For reproducibility
        """
        self.design_space = design_space
        self.objective_function = objective_function
        self.budget = budget
        self.population_size = max(4, population_size)
        self.generations = max(1, generations)
        self.mutation_rate = max(0.01, min(mutation_rate, 0.5))
        self.crossover_rate = max(0.5, min(crossover_rate, 0.99))
        self.elite_size = max(1, int(self.population_size * elite_percentage))
        
        if random_seed is not None:
            random.seed(random_seed)
        
        # Initialize tracking
        self.population = []
        self.fitness_values = []
        self.best_individual = None
        self.best_fitness = -float('inf')
        self.fitness_history = []
        self.generation_count = 0

    def initialize_population(self) -> List[CandidateSolution]:
        """
        Initialize population with random valid solutions.
        
        Returns:
            Initial population
        """
        population = []
        
        print(f"Initializing population of size {self.population_size}...")
        
        for i in range(self.population_size):
            candidate = self.design_space.generate_random_solution()
            
            # Ensure within budget
            if candidate.total_cost <= self.budget:
                population.append(candidate)
            else:
                # Try to find a solution within budget
                attempts = 0
                while attempts < 10 and candidate.total_cost > self.budget:
                    candidate = self.design_space.generate_random_solution()
                    attempts += 1
                
                if candidate.total_cost <= self.budget:
                    population.append(candidate)
        
        # If not enough solutions, fill with smaller configurations
        while len(population) < self.population_size:
            # Create smaller solution
            solar_kw = random.uniform(1, 5)
            battery_kwh = random.uniform(0, 5)
            
            candidate = CandidateSolution(
                solar_kw=round(solar_kw, 1),
                battery_kwh=round(battery_kwh, 1),
                solar_panels_count=max(1, math.ceil(solar_kw * 1000 / 400)),
                battery_units=max(0, math.ceil(battery_kwh / 2.0)),
                total_cost=solar_kw * 1000 * 50 + battery_kwh * 60000,  # Rough estimate
                solar_panel_id='SP_IND_001',
                battery_id='BAT_IND_001'
            )
            
            if candidate.total_cost <= self.budget:
                population.append(candidate)
        
        self.population = population[:self.population_size]
        print(f"Population initialized with {len(self.population)} individuals.\n")
        
        return self.population

    def evaluate_population(self) -> List[Tuple[CandidateSolution, float]]:
        """
        Evaluate all individuals in population.
        
        Returns:
            List of (candidate, fitness) tuples
        """
        evaluated = []
        
        for individual in self.population:
            fitness, metrics = self.objective_function.evaluate(individual)
            evaluated.append((individual, fitness, metrics))
            
            # Track best individual
            if fitness > self.best_fitness:
                self.best_fitness = fitness
                self.best_individual = copy.deepcopy(individual)
        
        self.fitness_values = [f for _, f, _ in evaluated]
        self.fitness_history.append(self.best_fitness)
        
        return [(ind, fit) for ind, fit, _ in evaluated]

    def selection(self, evaluated_pop: List[Tuple[CandidateSolution, float]]) -> List[CandidateSolution]:
        """
        Select individuals using tournament selection.
        
        Args:
            evaluated_pop: List of (candidate, fitness) tuples
            
        Returns:
            Selected population
        """
        selected = []
        tournament_size = 3
        
        while len(selected) < self.population_size:
            # Tournament selection
            tournament = random.sample(evaluated_pop, min(tournament_size, len(evaluated_pop)))
            winner = max(tournament, key=lambda x: x[1])
            selected.append(copy.deepcopy(winner[0]))
        
        return selected

    def crossover(self, parent1: CandidateSolution, parent2: CandidateSolution) -> Tuple[CandidateSolution, CandidateSolution]:
        """
        Perform crossover between two parents.
        
        Args:
            parent1: First parent
            parent2: Second parent
            
        Returns:
            Two offspring
        """
        if random.random() > self.crossover_rate:
            return copy.deepcopy(parent1), copy.deepcopy(parent2)
        
        # Blend solar and battery sizes
        alpha = random.random()
        
        child1_solar = parent1.solar_kw * alpha + parent2.solar_kw * (1 - alpha)
        child1_battery = parent1.battery_kwh * alpha + parent2.battery_kwh * (1 - alpha)
        
        child2_solar = parent2.solar_kw * alpha + parent1.solar_kw * (1 - alpha)
        child2_battery = parent2.battery_kwh * alpha + parent1.battery_kwh * (1 - alpha)
        
        # Clamp to valid ranges
        child1_solar = max(1.0, min(15.0, round(child1_solar, 1)))
        child1_battery = max(0.0, min(20.0, round(child1_battery, 1)))
        child2_solar = max(1.0, min(15.0, round(child2_solar, 1)))
        child2_battery = max(0.0, min(20.0, round(child2_battery, 1)))
        
        # Recalculate component counts and costs
        child1 = self._create_candidate(child1_solar, child1_battery)
        child2 = self._create_candidate(child2_solar, child2_battery)
        
        return child1, child2

    def mutate(self, individual: CandidateSolution) -> CandidateSolution:
        """
        Perform mutation on an individual.
        
        Args:
            individual: Individual to mutate
            
        Returns:
            Mutated individual
        """
        if random.random() > self.mutation_rate:
            return copy.deepcopy(individual)
        
        mutant = copy.deepcopy(individual)
        
        # Random mutation of solar or battery (or both)
        if random.random() < 0.5:
            # Mutate solar size
            delta_solar = random.uniform(-2, 2)
            new_solar = max(1.0, min(15.0, mutant.solar_kw + delta_solar))
            mutant.solar_kw = round(new_solar, 1)
        
        if random.random() < 0.5:
            # Mutate battery size
            delta_battery = random.uniform(-2, 2)
            new_battery = max(0.0, min(20.0, mutant.battery_kwh + delta_battery))
            mutant.battery_kwh = round(new_battery, 1)
        
        # Recalculate
        mutant = self._create_candidate(mutant.solar_kw, mutant.battery_kwh)
        
        return mutant

    def evolve(self) -> Dict:
        """
        Run the genetic algorithm evolution.
        
        Returns:
            Results dictionary with best solution and evolution stats
        """
        print("\n" + "="*70)
        print("GENETIC ALGORITHM OPTIMIZATION")
        print("="*70)
        print(f"Population Size: {self.population_size}")
        print(f"Generations: {self.generations}")
        print(f"Mutation Rate: {self.mutation_rate:.1%}")
        print(f"Budget Constraint: ₹{self.budget:,.0f}")
        print("="*70 + "\n")
        
        # Initialize population
        self.initialize_population()
        
        # Evolve for specified generations
        for generation in range(self.generations):
            # Evaluate
            evaluated_pop = self.evaluate_population()
            
            # Select
            selected_pop = self.selection(evaluated_pop)
            
            # Create new population through crossover and mutation
            new_population = []
            
            # Elitism - preserve best individuals
            elite_individuals = sorted(evaluated_pop, key=lambda x: x[1], reverse=True)[:self.elite_size]
            new_population.extend([ind for ind, _ in elite_individuals])
            
            # Generate offspring
            while len(new_population) < self.population_size:
                parent1, parent2 = random.sample(selected_pop, 2)
                
                # Crossover
                child1, child2 = self.crossover(parent1, parent2)
                
                # Mutation
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                
                if len(new_population) < self.population_size:
                    new_population.append(child1)
                if len(new_population) < self.population_size:
                    new_population.append(child2)
            
            self.population = new_population[:self.population_size]
            self.generation_count = generation + 1
            
            # Print progress
            avg_fitness = sum(self.fitness_values) / len(self.fitness_values) if self.fitness_values else 0
            print(f"Gen {generation + 1:3d}/{self.generations} | "
                  f"Best: {self.best_fitness:6.2f} | "
                  f"Avg: {avg_fitness:6.2f} | "
                  f"Cost: ₹{self.best_individual.total_cost:9,.0f}")
        
        return self._compile_results()

    def _compile_results(self) -> Dict:
        """Compile final results."""
        if self.best_individual is None:
            raise ValueError("No valid solution found")
        
        _, metrics = self.objective_function.evaluate(self.best_individual)
        
        return {
            'best_solution': self.best_individual,
            'best_fitness': self.best_fitness,
            'generations': self.generation_count,
            'population_size': self.population_size,
            'metrics': metrics,
            'fitness_history': self.fitness_history
        }

    def _create_candidate(self, solar_kw: float, battery_kwh: float) -> CandidateSolution:
        """Helper to create candidate from solar/battery sizes."""
        solar_results = self.design_space.calculate_solar_panels_needed(solar_kw)
        battery_results = self.design_space.calculate_battery_units_needed(battery_kwh)
        
        best_solar = min(solar_results.items(), key=lambda x: x[1]['total_cost'])
        best_battery = min(battery_results.items(), key=lambda x: x[1]['total_cost'])
        
        return CandidateSolution(
            solar_kw=solar_kw,
            battery_kwh=battery_kwh,
            solar_panels_count=best_solar[1]['panels_count'],
            battery_units=best_battery[1]['units'],
            total_cost=best_solar[1]['total_cost'] + best_battery[1]['total_cost'],
            solar_panel_id=best_solar[0],
            battery_id=best_battery[0]
        )

    def print_results(self, results: Dict):
        """Print optimization results in formatted manner."""
        print("\n" + "="*70)
        print("OPTIMIZATION RESULTS")
        print("="*70)
        
        solution = results['best_solution']
        metrics = results['metrics']
        
        print(f"\n🎯 OPTIMAL SYSTEM CONFIGURATION")
        print("-"*70)
        print(f"  Solar Capacity: {solution.solar_kw:.1f} kW ({solution.solar_panels_count} panels)")
        print(f"  Battery Capacity: {solution.battery_kwh:.1f} kWh ({solution.battery_units} units)")
        print(f"  Total System Cost: ₹{solution.total_cost:>12,.0f}")
        print(f"  Budget Available: ₹{self.budget:>12,.0f}")
        print(f"  Budget Utilization: {(solution.total_cost/self.budget)*100:>11.1f}%")
        
        print(f"\n📊 PERFORMANCE METRICS")
        print("-"*70)
        print(f"  Grid Dependency: {metrics['grid_dependency']:>33.1f}%")
        print(f"  Solar Utilization: {metrics['solar_utilization']:>31.1f}%")
        print(f"  Avg. Battery SoC: {metrics['avg_soc']:>32.1f}%")
        print(f"  Estimated Savings: ₹{metrics['estimated_savings']:>30,.0f}")
        
        print(f"\n🏆 FITNESS SCORE: {results['best_fitness']:.2f}/100")
        print("-"*70)
        
        print(f"\n📈 OPTIMIZATION STATISTICS")
        print("-"*70)
        print(f"  Generations: {results['generations']}")
        print(f"  Population Size: {results['population_size']}")
        print(f"  Final Fitness: {results['fitness_history'][-1]:.2f}")
        print(f"  Initial Fitness: {results['fitness_history'][0]:.2f}")
        print(f"  Improvement: +{results['fitness_history'][-1] - results['fitness_history'][0]:.2f}")
        
        print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    opt = OptimizationManager(
        load_file="outputs/cleaned_hourly.csv",
        tariff_per_kwh=8.0
    )
    best_design, df = opt.run_optimization(hours=24)
