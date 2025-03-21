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
        
        tk.Label(subplot_frame, text="Subplot Layout:").grid(row=0, column=0)
        self.num_rows = tk.Spinbox(subplot_frame, from_=1, to=3, width=3)
        self.num_rows.grid(row=0, column=1, padx=5)
        tk.Label(subplot_frame, text="×").grid(row=0, column=2)
        self.num_cols = tk.Spinbox(subplot_frame, from_=1, to=3, width=3)
        self.num_cols.grid(row=0, column=3, padx=5)
        
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


        # Scale options frame
        scale_frame = tk.Frame(root)
        scale_frame.pack(pady=5)
        
        # X-axis scale options
        x_scale_frame = tk.Frame(scale_frame)
        x_scale_frame.grid(row=0, column=0, padx=10)
        tk.Label(x_scale_frame, text="X-axis:").grid(row=0, column=0)
        self.x_scale = tk.StringVar(value='linear')
        tk.Radiobutton(x_scale_frame, text="Linear", variable=self.x_scale, 
                      value="linear").grid(row=0, column=1)
        tk.Radiobutton(x_scale_frame, text="Log", variable=self.x_scale,
                      value="log").grid(row=0, column=2)
        tk.Label(x_scale_frame, text="Label:").grid(row=0, column=3, padx=5)
        self.x_label = tk.Entry(x_scale_frame, width=15)
        self.x_label.grid(row=0, column=4)

        # Y-axis scale options  
        y_scale_frame = tk.Frame(scale_frame)
        y_scale_frame.grid(row=1, column=0, padx=10)
        tk.Label(y_scale_frame, text="Y-axis:").grid(row=0, column=0)
        self.y_scale = tk.StringVar(value='linear')
        tk.Radiobutton(y_scale_frame, text="Linear", variable=self.y_scale,
                      value="linear").grid(row=0, column=1)
        tk.Radiobutton(y_scale_frame, text="Log", variable=self.y_scale,
                      value="log").grid(row=0, column=2)
        tk.Label(y_scale_frame, text="Label:").grid(row=0, column=3, padx=5)
        self.y_label = tk.Entry(y_scale_frame, width=15)
        self.y_label.grid(row=0, column=4)
        
        
        # Grid options frame
        grid_frame = tk.Frame(root)
        grid_frame.pack(pady=5)
        tk.Label(grid_frame, text="Grid:").grid(row=0, column=0)
        self.show_grid = tk.BooleanVar(value=True)
        tk.Checkbutton(grid_frame, text="Show Grid", variable=self.show_grid).grid(row=0, column=1)
        
        # spine options frame
        spine_frame = tk.Frame(root)
        spine_frame.pack(pady=5)
        tk.Label(spine_frame, text="Spines:").grid(row=0, column=0)
        self.show_spines = tk.BooleanVar(value=True)
        tk.Checkbutton(spine_frame, text="Show Spines", variable=self.show_spines).grid(row=0, column=1)
        tk.Label(spine_frame, text="Spine Color:").grid(row=0, column=2)
        self.spine_color = tk.StringVar(value='black')
        colors = ['black', 'red', 'green', 'orange', 'purple']
        tk.OptionMenu(spine_frame, self.spine_color, *colors).grid(row=0, column=3, padx=5)
        tk.Label(spine_frame, text="Spine Width:").grid(row=0, column=4)
        self.spine_width = tk.Spinbox(spine_frame, from_=1, to=10, width=5)
        self.spine_width.grid(row=0, column=5, padx=5)
        
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
            # Get subplot layout dimensions from user input
            rows = int(self.num_rows.get())
            cols = int(self.num_cols.get())
            total_plots = rows * cols
            
            # Create subplot figure with appropriate size
            fig, axes = plt.subplots(rows, cols, figsize=(5*cols, 4*rows))
            
            # Convert single subplot axis to array for consistent handling
            if total_plots == 1:
                axes = np.array([axes])
            axes = axes.flatten()  # Convert 2D array of axes to 1D for easier iteration
            
            # Create each subplot
            for i in range(total_plots):
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
                # Set axis labels if provided
                if self.x_label.get():
                    axes[i].set_xlabel(self.x_label.get())
                if self.y_label.get():
                    axes[i].set_ylabel(self.y_label.get())

                # set logarithmic scale if selected
                if self.x_scale.get() == "log":
                    axes[i].set_xscale("log")
                if self.y_scale.get() == "log":
                    axes[i].set_yscale("log")
                
                # show grid if selected
                if self.show_grid.get():
                    axes[i].grid(True)  

                # show spines if selected
                if self.show_spines.get():
                    axes[i].spines['top'].set_color(self.spine_color.get())
                    axes[i].spines['top'].set_linewidth(float(self.spine_width.get()))
                    axes[i].spines['bottom'].set_color(self.spine_color.get())
                    axes[i].spines['bottom'].set_linewidth(float(self.spine_width.get()))
                    axes[i].spines['left'].set_color(self.spine_color.get())
                    axes[i].spines['left'].set_linewidth(float(self.spine_width.get()))
                    axes[i].spines['right'].set_color(self.spine_color.get())
                    axes[i].spines['right'].set_linewidth(float(self.spine_width.get()))
                else:
                    axes[i].spines['top'].set_visible(False)
                    axes[i].spines['bottom'].set_visible(False)
                    axes[i].spines['left'].set_visible(False)
                    axes[i].spines['right'].set_visible(False)

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
