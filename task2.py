import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class PlottingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task 2")
        
        # Input frames
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)
        
        # Data source selection
        tk.Label(input_frame, text="Data Source:").grid(row=0, column=0)
        self.data_source = tk.StringVar(value="manual")
        tk.Radiobutton(input_frame, text="Manual Input", variable=self.data_source, 
                      value="manual", command=self.toggle_input_mode).grid(row=0, column=1)
        tk.Radiobutton(input_frame, text="Random Data", variable=self.data_source,
                      value="random", command=self.toggle_input_mode).grid(row=0, column=2)
        
        # Manual input fields
        self.manual_frame = tk.Frame(input_frame)
        self.manual_frame.grid(row=1, column=0, columnspan=3, pady=5)
        
        tk.Label(self.manual_frame, text="X coordinates (comma separated):").grid(row=0, column=0)
        self.x_coords = tk.Entry(self.manual_frame, width=30)
        self.x_coords.grid(row=0, column=1, padx=5)
        
        tk.Label(self.manual_frame, text="Y coordinates (comma separated):").grid(row=1, column=0)
        self.y_coords = tk.Entry(self.manual_frame, width=30)
        self.y_coords.grid(row=1, column=1, padx=5)
        
        # Random data fields
        self.random_frame = tk.Frame(input_frame)
        tk.Label(self.random_frame, text="Number of points:").grid(row=0, column=0)
        self.num_points = tk.Spinbox(self.random_frame, from_=2, to=1000, width=5)
        self.num_points.grid(row=0, column=1, padx=5)
        
        # Subplot configuration
        subplot_frame = tk.Frame(root)
        subplot_frame.pack(pady=5)
        
        tk.Label(subplot_frame, text="Number of subplots:").grid(row=0, column=0)
        self.num_subplots = tk.Spinbox(subplot_frame, from_=1, to=9, width=3)
        self.num_subplots.grid(row=0, column=1, padx=5)
        
        tk.Label(subplot_frame, text="Orientation:").grid(row=0, column=2)
        self.orientation = tk.StringVar(value="horizontal")
        tk.Radiobutton(subplot_frame, text="Horizontal", variable=self.orientation,
                      value="horizontal").grid(row=0, column=3)
        tk.Radiobutton(subplot_frame, text="Vertical", variable=self.orientation,
                      value="vertical").grid(row=0, column=4)
        
        # Style options frame
        style_frame = tk.Frame(root)
        style_frame.pack(pady=5)
        
        tk.Label(style_frame, text="Line width:").grid(row=0, column=0)
        self.line_width = tk.Spinbox(style_frame, from_=1, to=10, width=5)
        self.line_width.grid(row=0, column=1, padx=5)
        
        tk.Label(style_frame, text="Marker:").grid(row=0, column=2)
        self.marker = tk.StringVar(value='o')
        markers = ['o', 's', '^', 'v', '*', '+', 'x']
        tk.OptionMenu(style_frame, self.marker, *markers).grid(row=0, column=3, padx=5)
        
        tk.Label(style_frame, text="Line style:").grid(row=0, column=4)
        self.line_style = tk.StringVar(value='-')
        styles = ['-', '--', ':', '-.']
        tk.OptionMenu(style_frame, self.line_style, *styles).grid(row=0, column=5, padx=5)
        
        tk.Label(style_frame, text="Color:").grid(row=0, column=6)
        self.color = tk.StringVar(value='blue')
        colors = ['blue', 'red', 'green', 'orange', 'purple']
        tk.OptionMenu(style_frame, self.color, *colors).grid(row=0, column=7, padx=5)
        
        # Plot button
        tk.Button(root, text="Plot", command=self.plot_data).pack(pady=10)
        
        self.toggle_input_mode()
        
    def toggle_input_mode(self):
        if self.data_source.get() == "manual":
            self.manual_frame.grid()
            self.random_frame.grid_remove()
        else:
            self.manual_frame.grid_remove()
            self.random_frame.grid()
            
    def generate_random_data(self):
        n = int(self.num_points.get())
        x = np.linspace(0, 10, n)
        y = np.random.randn(n)
        return x, y
        
    def plot_data(self):
        try:
            # Get number of subplots and orientation
            num_plots = int(self.num_subplots.get())
            is_horizontal = self.orientation.get() == "horizontal"
            
            # Set rows and columns based on orientation
            if is_horizontal:
                rows, cols = 1, num_plots
                figsize = (5*num_plots, 4)
            else:
                rows, cols = num_plots, 1
                figsize = (5, 4*num_plots)
            
            # Create subplot figure
            fig, axes = plt.subplots(rows, cols, figsize=figsize)
            
            # Convert single subplot axis to array for consistent handling
            if num_plots == 1:
                axes = np.array([axes])
            
            # Create each subplot
            for i in range(num_plots):
                # Handle manual data input
                if self.data_source.get() == "manual":
                    try:
                        # Parse x and y coordinates from comma-separated strings
                        x = [float(x.strip()) for x in self.x_coords.get().split(',')]
                        y = [float(y.strip()) for y in self.y_coords.get().split(',')]
                        
                        # Validate coordinate pairs
                        if len(x) != len(y):
                            messagebox.showerror("Error", "X and Y coordinates must have same length")
                            return
                    except ValueError:
                        messagebox.showerror("Error", "Invalid coordinate format")
                        return
                else:
                    # Generate random data if not using manual input
                    x, y = self.generate_random_data()

                # Plot on the current axis
                axes[i].plot(x, y,
                           marker=self.marker.get(),
                           linestyle=self.line_style.get(),
                           linewidth=float(self.line_width.get()),
                           color=self.color.get())
                axes[i].grid(True)

            # create a new tkinter window
            plot_window = tk.Toplevel(self.root)
            plot_window.title("Plot")

            # create a canvas and add the figure to it
            canvas = FigureCanvasTkAgg(fig, master=plot_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PlottingApp(root)
    root.mainloop()
