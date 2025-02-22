import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from simulation import Simulation
from visualization import Visualizer

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Criminal History Impact Simulation")
        self.root.geometry("1200x800")

        self.simulation = Simulation()
        self.visualizer = Visualizer()
        
        self.setup_ui()
        self.current_figure = None
        self.canvas = None

    def setup_ui(self):
        """Set up the user interface."""
        # Parameters Frame
        params_frame = ttk.LabelFrame(self.root, text="Simulation Parameters", padding="10")
        params_frame.pack(fill="x", padx=10, pady=5)

        # Arrest Rates
        rates_frame = ttk.Frame(params_frame)
        rates_frame.pack(fill="x", pady=5)
        
        ttk.Label(rates_frame, text="Arrest Rates (%)").pack(side="left", padx=5)
        
        ttk.Label(rates_frame, text="White:").pack(side="left", padx=5)
        self.white_rate = ttk.Entry(rates_frame, width=5)
        self.white_rate.insert(0, "1")
        self.white_rate.pack(side="left", padx=5)
        
        ttk.Label(rates_frame, text="Black:").pack(side="left", padx=5)
        self.black_rate = ttk.Entry(rates_frame, width=5)
        self.black_rate.insert(0, "7")
        self.black_rate.pack(side="left", padx=5)

        # Sentence Lengths
        sentence_frame = ttk.Frame(params_frame)
        sentence_frame.pack(fill="x", pady=5)
        
        ttk.Label(sentence_frame, text="Sentence Lengths (years)").pack(side="left", padx=5)
        
        ttk.Label(sentence_frame, text="1st:").pack(side="left", padx=5)
        self.first_sentence = ttk.Entry(sentence_frame, width=5)
        self.first_sentence.insert(0, "0")
        self.first_sentence.pack(side="left", padx=5)
        
        ttk.Label(sentence_frame, text="2nd:").pack(side="left", padx=5)
        self.second_sentence = ttk.Entry(sentence_frame, width=5)
        self.second_sentence.insert(0, "0.5")
        self.second_sentence.pack(side="left", padx=5)
        
        ttk.Label(sentence_frame, text="3rd+:").pack(side="left", padx=5)
        self.third_sentence = ttk.Entry(sentence_frame, width=5)
        self.third_sentence.insert(0, "3")
        self.third_sentence.pack(side="left", padx=5)

        # Buttons
        buttons_frame = ttk.Frame(params_frame)
        buttons_frame.pack(fill="x", pady=10)
        
        ttk.Button(buttons_frame, text="Run Single Simulation", 
                  command=self.run_single_simulation).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Run Multiple Simulations", 
                  command=self.run_multiple_simulations).pack(side="left", padx=5)

        # Canvas Frame for matplotlib
        self.canvas_frame = ttk.Frame(self.root)
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=5)

    def validate_inputs(self):
        """Validate user inputs."""
        try:
            white_rate = float(self.white_rate.get()) / 100
            black_rate = float(self.black_rate.get()) / 100
            first = float(self.first_sentence.get())
            second = float(self.second_sentence.get())
            third = float(self.third_sentence.get())

            if not (0 <= white_rate <= 1 and 0 <= black_rate <= 1):
                raise ValueError("Arrest rates must be between 0 and 100%")
            if not (0 <= first <= 10 and 0 <= second <= 10 and 0 <= third <= 10):
                raise ValueError("Sentence lengths must be between 0 and 10 years")

            return white_rate, black_rate, (first, second, third)
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return None

    def update_canvas(self, figure):
        """Update the matplotlib canvas with a new figure."""
        # Clear existing canvas if it exists
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()

        # Create new canvas
        self.canvas = FigureCanvasTkAgg(figure, self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def run_single_simulation(self):
        """Run and display a single simulation."""
        inputs = self.validate_inputs()
        if inputs is None:
            return

        white_rate, black_rate, sentence_lengths = inputs
        
        # Run simulation
        white_data, black_data = self.simulation.run_single_simulation(
            white_rate, black_rate, sentence_lengths
        )
        
        # Create visualization
        fig, _ = self.visualizer.plot_single_simulation(
            white_data, black_data,
            self.simulation.white_population,
            self.simulation.black_population
        )
        
        self.update_canvas(fig)

    def run_multiple_simulations(self):
        """Run and display multiple simulations."""
        inputs = self.validate_inputs()
        if inputs is None:
            return

        white_rate, black_rate, sentence_lengths = inputs
        
        # Run simulations
        white_stats, black_stats = self.simulation.run_multiple_simulations(
            white_rate, black_rate, sentence_lengths
        )
        
        # Create visualization
        fig = self.visualizer.plot_multiple_simulations(white_stats, black_stats)
        self.update_canvas(fig)

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()