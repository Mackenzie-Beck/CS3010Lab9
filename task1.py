import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk



class PlottingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task 1")
        
        # Input frames
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="X coordinates (comma separated):").grid(row=0, column=0)
        self.x_coords = tk.Entry(input_frame, width=30)
        self.x_coords.grid(row=0, column=1, padx=5)
        
        tk.Label(input_frame, text="Y coordinates (comma separated):").grid(row=1, column=0)
        self.y_coords = tk.Entry(input_frame, width=30)
        self.y_coords.grid(row=1, column=1, padx=5)
        
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
        
        # Plot button
        tk.Button(root, text="Plot", command=self.plot_data).pack(pady=10)
        
    def plot_data(self):
        try:
            # Get coordinates
            x = [float(x.strip()) for x in self.x_coords.get().split(',')]
            y = [float(y.strip()) for y in self.y_coords.get().split(',')]
            
            if len(x) != len(y):
                tk.messagebox.showerror("Error", "X and Y coordinates must have same length")
                return
                
            # Create a new Tkinter window
            plot_window = tk.Toplevel(self.root)
            plot_window.title("Plot")

            # Create a Matplotlib figure and plot
            fig, ax = plt.subplots()
            ax.plot(x, y, 
                    marker=self.marker.get(),
                    linestyle=self.line_style.get(),
                    linewidth=float(self.line_width.get()))
            ax.grid(True)

            # Create a canvas and add the figure to it
            canvas = FigureCanvasTkAgg(fig, master=plot_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid coordinate format")
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PlottingApp(root)
    root.mainloop()
