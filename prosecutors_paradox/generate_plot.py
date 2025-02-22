import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

from simulation import Simulation
from visualization import Visualizer

def generate_multiple_simulation_plot():
    # Initialize simulation with default parameters
    simulation = Simulation()
    visualizer = Visualizer()
    
    # Use the same default parameters as in the GUI
    white_rate = 0.01  # 1%
    black_rate = 0.07  # 7%
    sentence_lengths = (0, 0.5, 3)  # 1st, 2nd, 3rd+ offense sentences
    
    # Run simulations
    white_stats, black_stats = simulation.run_multiple_simulations(
        white_rate, black_rate, sentence_lengths
    )
    
    # Create and save visualization
    fig = visualizer.plot_multiple_simulations(white_stats, black_stats)
    fig.savefig('multiple_simulation_results.png', bbox_inches='tight', dpi=300)
    print("Plot saved as multiple_simulation_results.png")

if __name__ == "__main__":
    generate_multiple_simulation_plot()