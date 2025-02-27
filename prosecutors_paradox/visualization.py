import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Tuple
from simulation import Person

class Visualizer:
    """Handles visualization of simulation results."""
    
    def __init__(self):
        plt.style.use('seaborn')
        # Match web version colors
        self.white_color = '#1976D2'  # Blue
        self.black_color = '#D32F2F'  # Red
        self.background_color = '#ffffff'
        self.grid_color = (0, 0, 0, 0.05)  # RGBA tuple for matplotlib
        # Use a generic sans-serif font that's available on most systems
        self.font_family = 'sans-serif'

    def setup_population_plot(self, ax, title: str, is_white: bool):
        """Set up a subplot for population visualization."""
        ax.set_title(title, fontsize=12, pad=10)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_facecolor(self.background_color)
        
        # Add grid pattern similar to web version
        ax.grid(True, color=self.grid_color, linestyle='-', linewidth=0.5)
        ax.set_axisbelow(True)
        
        # Add border and box styling
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color('#e0e0e0')
            spine.set_linewidth(1)
        
        color = self.white_color if is_white else self.black_color
        return color

    def draw_population(self, population: List[Person], ax, color: str):
        """Draw population as dots with size based on arrest count."""
        ax.clear()
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_facecolor(self.background_color)
        
        # Re-add grid and border styling after clear
        ax.grid(True, color=self.grid_color, linestyle='-', linewidth=0.5)
        ax.set_axisbelow(True)
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color('#e0e0e0')
            spine.set_linewidth(1)

        for person in population:
            if person.arrests > 0:
                # Match web version dot sizes with improved visibility
                base_size = 50  # Base marker size
                size = base_size + (person.arrests - 1) * 25
                # Add slight shadow effect to dots
                ax.scatter(person.x, person.y, s=size + 5, c='gray', alpha=0.1)
                ax.scatter(person.x, person.y, s=size, c=color, alpha=0.7,
                         edgecolor='white', linewidth=1.5)

    def plot_single_simulation(self, white_data: List[float], black_data: List[float],
                              white_pop: List[Person], black_pop: List[Person]) -> Tuple[plt.Figure, List[plt.Axes]]:
        """Create plots for single simulation results."""
        # Create figure with better proportions and spacing
        fig = plt.figure(figsize=(16, 10))
        fig.patch.set_facecolor(self.background_color)
        
        # Create two separate GridSpecs for better layout control
        gs_top = fig.add_gridspec(2, 2, height_ratios=[1, 1], hspace=0.3, wspace=0.3,
                                top=0.95, bottom=0.45)  # Top section for populations and legends
        
        # Population grids (2x2 grid on top)
        ax_white_pop = fig.add_subplot(gs_top[0, 0])
        ax_black_pop = fig.add_subplot(gs_top[1, 0])
        white_color = self.setup_population_plot(ax_white_pop, 'Comparison Population', True)
        black_color = self.setup_population_plot(ax_black_pop, 'Targetted Population', False)
        
        # Draw populations
        self.draw_population(white_pop, ax_white_pop, white_color)
        self.draw_population(black_pop, ax_black_pop, black_color)
        
        # Legend for arrest counts with better positioning
        ax_white_legend = fig.add_subplot(gs_top[0, 1])
        ax_black_legend = fig.add_subplot(gs_top[1, 1])
        self._add_legend(ax_white_legend, 'Comparison Population Legend', True)
        self._add_legend(ax_black_legend, 'Targetted Population Legend', False)

        # Time series plot below with proper spacing
        gs_bottom = fig.add_gridspec(1, 1, top=0.35, bottom=0.1,
                                   left=0.1, right=0.9)  # Bottom section for time series
        ax_time = fig.add_subplot(gs_bottom[0])
        self._plot_time_series(ax_time, white_data, black_data, 'Single Simulation Results')
        return fig, [ax_white_pop, ax_black_pop, ax_time]

    def plot_multiple_simulations(self, white_stats: Dict, black_stats: Dict) -> plt.Figure:
        """Create plot for multiple simulations with error bands."""
        fig, ax = plt.subplots(figsize=(12, 6))
        fig.patch.set_facecolor(self.background_color)
        
        x = np.arange(1, len(white_stats['means']) + 1)
        
        # Plot with error bands
        ax.plot(x, white_stats['means'], color=self.white_color,
                label='Comparison Population', linewidth=2)
        ax.fill_between(x,
                       np.array(white_stats['means']) - np.array(white_stats['std_devs']),
                       np.array(white_stats['means']) + np.array(white_stats['std_devs']),
                       color=self.white_color, alpha=0.2)
        
        ax.plot(x, black_stats['means'], color=self.black_color,
                label='Targetted Population', linewidth=2)
        ax.fill_between(x,
                       np.array(black_stats['means']) - np.array(black_stats['std_devs']),
                       np.array(black_stats['means']) + np.array(black_stats['std_devs']),
                       color=self.black_color, alpha=0.2)
        
        self._style_axis(ax, 'Multiple Simulations Results\n(with Standard Deviation)')
        
        # Calculate black-to-white ratio at year 20
        black_to_white_ratio = black_stats['means'][-1] / white_stats['means'][-1]
        
        # Add descriptive text to upper left
        text = (f"For every year people in the White cohort spend incarcerated\n"
                f"for criminal conduct, poeple in the Black cohort engaging in\n"
                f"the same conduct spend {black_to_white_ratio:.1f} years incarcerated.")
        
        # Position text in upper left with some padding
        ax.text(0.02, 0.98, text,
                transform=ax.transAxes,
                verticalalignment='top',
                horizontalalignment='left',
                fontsize=10,
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=3))
        
        plt.tight_layout()
        return fig

    def _add_legend(self, ax, title: str, is_white: bool):
        """Add legend showing dot sizes for arrest counts."""
        ax.set_title(title, fontsize=12, pad=10)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_facecolor(self.background_color)
        
        # Add border and box styling
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color('#e0e0e0')
            spine.set_linewidth(1)
        
        color = self.white_color if is_white else self.black_color
        y_positions = [0.75, 0.5, 0.25]  # Better spacing
        sizes = [50, 75, 100]  # Match population dot sizes
        labels = ['1 Arrest', '2 Arrests', '3+ Arrests']
        
        # Add legend items with improved styling
        for y, size, label in zip(y_positions, sizes, labels):
            # Add dot with shadow effect
            ax.scatter(0.25, y, s=size, c=color, alpha=0.6,
                      edgecolor='white', linewidth=1)
            # Add label with improved positioning and styling
            ax.text(0.45, y, label, verticalalignment='center',
                   horizontalalignment='left', fontsize=10,
                   color='#34495e')  # Darker text color for better contrast

    def _plot_time_series(self, ax, white_data: List[float], black_data: List[float],
                         title: str):
        """Plot time series data for single simulation."""
        x = np.arange(1, len(white_data) + 1)
        
        ax.plot(x, white_data, color=self.white_color, label='Comparison Population',
                marker='o', markersize=4, linewidth=2)
        ax.plot(x, black_data, color=self.black_color, label='Targetted Population',
                marker='o', markersize=4, linewidth=2)
        
        self._style_axis(ax, title)

    def _style_axis(self, ax, title: str):
        """Apply consistent styling to an axis."""
        ax.set_xlabel('Simulation Year', fontsize=12)
        ax.set_ylabel('Cumulative Sentence Years', fontsize=12)
        ax.set_title(title, fontsize=14, pad=20)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)  # Use default grid color with alpha
        ax.set_facecolor(self.background_color)
        
        # Style ticks
        ax.tick_params(labelsize=10)