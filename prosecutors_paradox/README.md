# Criminal History Impact Simulation

A Python application that demonstrates the cumulative impact of different arrest rates and sentencing policies over time. This is a simplified desktop version of the web-based simulation.

## Features

- Visual representation of two populations with dots indicating arrest history
- Configurable arrest rates for each population
- Configurable sentence lengths based on arrest count (1st, 2nd, 3rd+)
- Single simulation mode with population visualization and time series
- Multiple simulation mode with statistical analysis (mean and standard deviation)

## Requirements

- Python 3.8+
- matplotlib
- numpy
- tkinter (optional, for GUI version)

## Installation

1. Create and activate a virtual environment using uv:
```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

2. Install dependencies using either uv:
```bash
uv pip install matplotlib numpy
```

Or using the requirements.txt file:
```bash
uv pip install -r requirements.txt
```

## Running the Application

### CLI Version
The command-line interface version saves plots to files instead of displaying them in a window.

```bash
# Run a single simulation
python cli.py single white_rate black_rate first_sentence second_sentence third_sentence

# Run multiple simulations
python cli.py multiple white_rate black_rate first_sentence second_sentence third_sentence
```

Example:
```bash
# Run a single simulation with:
# - White arrest rate: 1%
# - Black arrest rate: 7%
# - First offense sentence: 0 years
# - Second offense sentence: 0.5 years
# - Third+ offense sentence: 3 years
python cli.py single 1 7 0 0.5 3

# Run multiple simulations with the same parameters
python cli.py multiple 1 7 0 0.5 3
```

The results will be saved as PNG files:
- `single_simulation_results.png` for single simulation (includes population grids and time series)
- `multiple_simulation_results.png` for multiple simulations (includes statistical analysis)

### GUI Version (requires tkinter)

If you have tkinter installed, you can run the graphical interface version:

```bash
python main.py
```

To install tkinter:
- Ubuntu/Debian: `sudo apt-get install python3-tk`
- macOS with Homebrew: `brew install python-tk`
- Windows: Tkinter usually comes with Python installation

## Usage (GUI Version)

1. Set the arrest rates (%) for each population:
   - White population rate (default: 1%)
   - Black population rate (default: 7%)

2. Set the sentence lengths (years) for each arrest:
   - First arrest (default: 0 years)
   - Second arrest (default: 0.5 years)
   - Third or more arrests (default: 3 years)

3. Choose simulation mode:
   - "Run Single Simulation" - Shows population grids and a single time series
   - "Run Multiple Simulations" - Runs 1000 simulations and shows statistical results

## Understanding the Visualization

### Single Simulation
- Population grids show individuals as dots
- Dot size increases with number of arrests (1 arrest: small dot, 2 arrests: medium dot, 3+ arrests: large dot)
- Time series graph shows cumulative sentence years over time
- Blue represents the white population, red represents the black population

### Multiple Simulations
- Shows mean cumulative sentence years over time for both populations
- Shaded areas represent one standard deviation above and below the mean
- Helps visualize the variation in outcomes across 1000 independent simulations
- Error bands indicate the range of typical outcomes

## Output Files

The application generates high-resolution PNG files:
- Single simulation output includes both population grids and time series plot
- Multiple simulation output shows statistical results with error bands
- Files are saved in the current directory with clear names
- Images use a clean, professional style with a white background and grid lines