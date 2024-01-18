import tkinter as tk
from tkinter import ttk
from datetime import datetime


class Graph:

    SAVE_NAME = 'TESTRUN'
    # Class-level constants for easy modification and access
    GRAPH_WIDTH, GRAPH_HEIGHT = 500, 300
    TICK_LENGTH, TICK_NUM = 4, 5
    XMIN, YMIN = -1, -1
    XMAX, YMAX = 6, 6

    DOMAIN, RANGE = XMAX - XMIN, YMAX - YMIN
    DELX, DELY = GRAPH_WIDTH / DOMAIN, GRAPH_HEIGHT / RANGE
    DELTIX, DELTIY = DELX / TICK_NUM, DELY / TICK_NUM

    UPDATE_INTERVAL = 10  # Update interval in milliseconds
    DATA_POINT_STEP = DELX * UPDATE_INTERVAL / 1000
    TABULATE_INTERVAL = 1000
    
    def __init__(self, parent, variable, x, y):
        # Initialize Graph with dimensions, parent, and variable for data plotting
        self.x = x
        self.y = y
        self.datapoints = []
        self.CSV = ''
        self.variable = variable
        self.parent = parent
        self.running = False
        self.graph_frame = tk.Frame(self.parent, bg='#0D0D0D')
        self.graph = tk.Canvas(self.graph_frame, width=self.GRAPH_WIDTH, height=self.GRAPH_HEIGHT, bg='black', highlightthickness=0)
        self.graph.pack()
        self.graph_frame.place(x=self.x, y=self.y)
        self.output_data = []
        self.raw_datapoints = []

        self.bind_movement()
        self.create_graph()
        self.setup_plot_button()

    # Graph Movement Methods
    def bind_movement(self):
        # Bind mouse events for graph movement
        self.graph.bind('<Button-1>', self.start_move)
        self.graph.bind('<B1-Motion>', self.on_move)
        self.graph.bind('<ButtonRelease-1>', self.stop_move)

    def start_move(self, event):
        # Start point for graph movement
        self.x_start, self.y_start = event.x, event.y

    def stop_move(self, event):
        # Reset points after movement
        self.x_start = self.y_start = None

    def on_move(self, event):
        # Handle the movement of the graph
        if self.x_start and self.y_start:
            dx, dy = event.x - self.x_start, event.y - self.y_start
            x_new, y_new = self.graph_frame.winfo_x() + dx, self.graph_frame.winfo_y() + dy
            self.graph_frame.place(x=x_new, y=y_new)

    # Graph Drawing Methods
    def create_graph(self):
        self.graph.delete("all")  # Clear the existing graph
        self.draw_minor_axes()
        self.draw_axes()
        self.draw_ticks()
        self.plot_values()  # Re-plot existing data points if necessary

    def draw_axes(self):
        # Draw major axis lines of the graph
        #yaxis
        self.graph.create_line((-self.XMIN * self.DELX, 0, -self.XMIN * self.DELX, self.GRAPH_HEIGHT), fill='white', width=1)
        #xaxis
        self.graph.create_line((0, self.GRAPH_HEIGHT + self.YMIN * self.DELY, self.GRAPH_WIDTH, self.GRAPH_HEIGHT + self.YMIN * self.DELY), fill='white', width=1)

    def draw_minor_axes(self):
        #x minor
        for i in range(self.DOMAIN):
            self.graph.create_line((i * self.DELX, 0, i * self.DELX, self.GRAPH_HEIGHT), fill = "#0F0F0F", width=1)
        #y minor
        for i in range(self.RANGE):
            self.graph.create_line((0, i * self.DELY, self.GRAPH_WIDTH, i * self.DELY), fill = "#0F0F0F", width=1)

    def draw_ticks(self):
        # Draw minor axis and ticks
        yaxis = -self.XMIN * self.DELX
        xaxis = self.GRAPH_HEIGHT + self.YMIN * self.DELY
        for i in range(self.DOMAIN):
            for j in range(self.TICK_NUM):
                self.graph.create_line((i*self.DELX + j*self.DELTIX, xaxis - self.TICK_LENGTH/2, i*self.DELX + j*self.DELTIX, xaxis + self.TICK_LENGTH/2), fill="white", width=1)

        for i in range(self.RANGE):
            for j in range(self.TICK_NUM):
                self.graph.create_line((yaxis - self.TICK_LENGTH/2, i*self.DELY + j*self.DELTIY, yaxis + self.TICK_LENGTH/2, i*self.DELY + j*self.DELTIY), fill="white", width=1)

    # Graph Plotting Methods
    def setup_plot_button(self):
        # Setup the start/stop button for graph plotting
        self.start_button = ttk.Button(self.graph_frame, text='Start/Stop', command=self.toggle_plotting, width=9)
        self.save_button = ttk.Button(self.graph_frame, text='Save', command=self.create_table, width=4)

        self.start_button.pack(pady=3, side='right')
        self.save_button.pack(pady=3, side='left')

    def toggle_plotting(self):
        # Toggle running state of graph plotting
        self.running = not self.running
        if self.running:
            print('Graph plotting...')
            self.start_plotting()
            self.start_data()

    def start_data(self):
        if self.running:
            self.update_data()
            self.parent.after(self.TABULATE_INTERVAL, self.start_data)

    def start_plotting(self):
        # Continuous plotting of data on the graph
        if self.running:
            self.update_graph()
            self.parent.after(self.UPDATE_INTERVAL, self.start_plotting)
            
        else:
            print('Graph stopped...')

    def update_data(self):
        current_datetime = datetime.now()
        current_time = str(current_datetime).split(' ')[1][0:-5]
        self.output_data.append([current_time, self.variable.get()])

    def update_graph(self):
        # Update graph with new data point
        current_datetime = datetime.now()
        
        self.value =  self.variable.get() * self.DELY - self.YMIN * self.DELY

        self.datapoints.append([self.GRAPH_WIDTH + self.DATA_POINT_STEP, self.GRAPH_HEIGHT - self.value])

        self.raw_datapoints.append([str(current_datetime).split(' ')[1], self.variable.get()])

        if len(self.datapoints) > self.DELY * 1000 / self.UPDATE_INTERVAL:
            self.datapoints.pop(0)

        self.plot_values()

    def plot_values(self):
        # Plot data points on the graph
        for i in self.datapoints:
            i[0] -= self.DATA_POINT_STEP
        self.graph.delete('data_line')  # Clear existing line
        try:
            self.graph.create_line(self.datapoints, fill='red', width=1, tags='data_line')
        except:
            pass
    
    def create_table(self):
        now = str(datetime.now())
        now_filename = self.SAVE_NAME + now[0:-16] + ' OutPut.csv'  # Get the current datetime
        raw_filename = self.SAVE_NAME + now[0:-16] + ' Raw.csv'

        with open(now_filename, 'w') as file: 
            file.write('TIME,VALUE\n')
            for i in self.output_data:
                left = str(i[0])
                right = str(i[1])
                file.write(left + "," + right + '\n')

        with open(raw_filename, 'w') as rawfile: 
            rawfile.write('TIME,VALUE\n')
            for i in self.raw_datapoints:
                left = str(i[0])
                right = str(i[1])
                rawfile.write(left + "," + right + '\n')

        print(f"Files saved to '{now_filename}' and '{raw_filename}")  # Print the current datetime

class BlowerCurrent:
    def __init__(self, parent, I2_var):
        self.I2_var = I2_var
        self.parent = parent
        self.current = tk.DoubleVar(value = 0)
        self.label = ttk.Label(self.parent, textvariable=self.current)
        self.running = False

    def toggle_updating(self):
        self.running = not self.running
        if self.running:
            print('Starting Blower Adjustment')
            self.start_adjusting()

    def start_adjusting(self):
        if self.running:
            self.update_current()
            self.parent.after(1000, self.start_adjusting)

    def update_current(self):
        ratio = self.I2_var.get()
        if ratio > 1.75:
            self.current.set(self.current.get() - 0.00005)
        elif 1.07 <= ratio and ratio <= 1.75:
            self.current.set(self.current.get() - 0.00001)
        elif 0.93 < ratio and ratio < 1.07:
            self.current = self.current
        elif 0.25 <= ratio and ratio <= 0.93:
            self.current.set(self.current.get() + 0.00001)
        elif ratio < 0.25:
            self.current.set(self.current.get() + 0.00005)

        if self.current.get() >= 0.02:
            self.current.set(0.02)
        elif self.current.get() <= 0.000:
            self.current.set(0.000)
        
        
        

        
    



window = tk.Tk()
window.title("Test Window")
window.geometry("1600x900")

def global_start_stop():
    I2_ratio_graph.toggle_plotting()
    Blower_current.toggle_updating()

#initialize frames
datetime_frame = ttk.Frame(window)
data_in_frame = ttk.Frame(window)
data_out_frame = ttk.Frame(window)
parameter_frame = ttk.Frame(window)
graph_frame = ttk.Frame(window)
user_input_frame = ttk.Frame(window)


I2_ratio_var = tk.DoubleVar(value=.2)

I2_ratio_canvas = tk.Canvas(graph_frame, bg="#AAAAAA")
I2_ratio_graph = Graph(I2_ratio_canvas, I2_ratio_var, 1050, 10)

Blower_current = BlowerCurrent(user_input_frame, I2_ratio_var)
Blower_current.label.pack()

start_stop_global = ttk.Button(user_input_frame, text='Start/Stop', command=global_start_stop)
start_stop_global.pack()




user_input_frame.pack(pady=20, padx=20, anchor=tk.W)

I2_ratio_canvas.pack(fill='both', expand=True)

graph_frame.pack(padx=20, pady=20, anchor=tk.E, fill='both', expand=True)




window.mainloop()