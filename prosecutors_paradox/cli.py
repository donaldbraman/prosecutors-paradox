import sys
from simulation import Simulation
from visualization import Visualizer
import matplotlib.pyplot as plt

def print_usage():
    print("""
Criminal History Impact Simulation - CLI Version

Usage:
    python cli.py [single|multiple] white_rate black_rate first_sentence second_sentence third_sentence

Arguments:
    single|multiple    - Run mode ('single' for one simulation, 'multiple' for 1000 simulations)
    white_rate        - Arrest rate for white population (0-100)
    black_rate        - Arrest rate for black population (0-100)
    first_sentence    - Average sentence for first arrest (0-10)
    second_sentence   - Average sentence for second arrest (0-10)
    third_sentence    - Average sentence for third+ arrest (0-10)

Example:
    python cli.py single 1 7 0 0.5 3
    python cli.py multiple 1 7 0 0.5 3
    """)

def validate_inputs(args):
    try:
        mode = args[1]
        if mode not in ['single', 'multiple']:
            raise ValueError("Mode must be 'single' or 'multiple'")
        
        rates = [float(args[2]), float(args[3])]
        sentences = [float(args[4]), float(args[5]), float(args[6])]
        
        for rate in rates:
            if not 0 <= rate <= 100:
                raise ValueError("Arrest rates must be between 0 and 100%")
        
        for sentence in sentences:
            if not 0 <= sentence <= 10:
                raise ValueError("Sentence lengths must be between 0 and 10 years")
        
        return mode, rates[0]/100, rates[1]/100, tuple(sentences)
    except (IndexError, ValueError) as e:
        print(f"Error: {str(e)}")
        print_usage()
        sys.exit(1)

def main():
    if len(sys.argv) != 7:
        print_usage()
        sys.exit(1)

    # Validate and parse inputs
    mode, white_rate, black_rate, sentence_lengths = validate_inputs(sys.argv)
    
    # Initialize simulation and visualization
    simulation = Simulation()
    visualizer = Visualizer()
    
    # Run simulation and create plots
    if mode == 'single':
        white_data, black_data = simulation.run_single_simulation(
            white_rate, black_rate, sentence_lengths
        )
        
        fig, _ = visualizer.plot_single_simulation(
            white_data, black_data,
            simulation.white_population,
            simulation.black_population
        )
        
        output_file = 'single_simulation_results.png'
    else:  # multiple simulations
        white_stats, black_stats = simulation.run_multiple_simulations(
            white_rate, black_rate, sentence_lengths
        )
        
        fig = visualizer.plot_multiple_simulations(white_stats, black_stats)
        output_file = 'multiple_simulation_results.png'
    
    # Save plot
    fig.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    print(f"\nSimulation completed successfully!")
    print(f"Results saved to: {output_file}")

if __name__ == "__main__":
    main()