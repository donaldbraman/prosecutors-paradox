import numpy as np
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Person:
    """Represents an individual in the simulation."""
    arrests: int = 0
    sentence_served: float = 0
    sentence_remaining: float = 0
    x: float = 0.0
    y: float = 0.0

class Simulation:
    """Handles the core simulation logic."""
    def __init__(self, grid_size: int = 10):
        self.grid_size = grid_size
        self.reset()

    def reset(self):
        """Reset the simulation with new random positions."""
        population_size = self.grid_size * self.grid_size
        self.white_population = [
            Person(x=np.random.random(), y=np.random.random())
            for _ in range(population_size)
        ]
        self.black_population = [
            Person(x=np.random.random(), y=np.random.random())
            for _ in range(population_size)
        ]

    def get_sentence(self, arrest_count: int, sentence_lengths: Tuple[float, float, float]) -> float:
        """Determine sentence length based on arrest count."""
        if arrest_count == 1:
            return sentence_lengths[0]
        elif arrest_count == 2:
            return sentence_lengths[1]
        return sentence_lengths[2]

    def simulate_arrests(self, population: List[Person], arrest_rate: float, sentence_lengths: Tuple[float, float, float]):
        """Simulate arrests for a given population."""
        eligible_people = [p for p in population if p.sentence_remaining <= 0]
        expected_arrests = round(len(eligible_people) * arrest_rate)

        # Randomly select people for arrest
        if eligible_people and expected_arrests > 0:
            arrested_indices = np.random.choice(
                len(eligible_people),
                size=min(expected_arrests, len(eligible_people)),
                replace=False
            )
            
            for idx in arrested_indices:
                person = eligible_people[idx]
                person.arrests += 1
                person.sentence_remaining = self.get_sentence(person.arrests, sentence_lengths)

    def update_sentences(self, population: List[Person]):
        """Update sentence progress for a population."""
        for person in population:
            if person.sentence_remaining > 0:
                person.sentence_served += 1
                person.sentence_remaining -= 1

    def run_single_simulation(self, 
                            white_rate: float,
                            black_rate: float,
                            sentence_lengths: Tuple[float, float, float],
                            years: int = 20) -> Tuple[List[float], List[float]]:
        """Run a single simulation and return cumulative sentences for both populations."""
        self.reset()
        white_sentences = []
        black_sentences = []

        for _ in range(years):
            self.simulate_arrests(self.white_population, white_rate, sentence_lengths)
            self.simulate_arrests(self.black_population, black_rate, sentence_lengths)
            
            self.update_sentences(self.white_population)
            self.update_sentences(self.black_population)

            white_total = sum(p.sentence_served for p in self.white_population)
            black_total = sum(p.sentence_served for p in self.black_population)
            
            white_sentences.append(white_total)
            black_sentences.append(black_total)

        return white_sentences, black_sentences

    def run_multiple_simulations(self,
                               white_rate: float,
                               black_rate: float,
                               sentence_lengths: Tuple[float, float, float],
                               num_simulations: int = 1000,
                               years: int = 20) -> Tuple[dict, dict]:
        """Run multiple simulations and return statistics."""
        white_simulations = []
        black_simulations = []

        for _ in range(num_simulations):
            white_data, black_data = self.run_single_simulation(
                white_rate, black_rate, sentence_lengths, years
            )
            white_simulations.append(white_data)
            black_simulations.append(black_data)

        # Calculate statistics
        white_stats = self._calculate_stats(white_simulations)
        black_stats = self._calculate_stats(black_simulations)

        return white_stats, black_stats

    def _calculate_stats(self, simulations: List[List[float]]) -> dict:
        """Calculate mean and standard deviation for multiple simulations."""
        simulations_array = np.array(simulations)
        means = np.mean(simulations_array, axis=0)
        std_devs = np.std(simulations_array, axis=0)
        
        return {
            'means': means.tolist(),
            'std_devs': std_devs.tolist()
        }