import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


battery_level = []
dt_stamp = []

def prep_fig_data(file):
    data = pd.read_csv(file)
    battery_level = data.battery.tolist()
    battery_level = battery_level[::30]
    timestamp = data.timestamp.tolist()
    timestamp = timestamp[::30]
    dt_stamp = []
    for i in timestamp:
        datetime_obj = datetime.strptime(i, '%d/%m/%Y %H:%M:%S')
        datetime_time = datetime_obj.time()
        dt_stamp.append(str(datetime_time))

    return battery_level, dt_stamp

def draw_fig_prep(canvas, fig):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)

def draw_fig(window):
    battery_level, dt_stamp = prep_fig_data("live_data.csv")

    fig = plt.gcf()
    plt.clf()
    plt.grid(True)
    DPI = fig.get_dpi()
    fig.set_size_inches(404 * 3 / float(DPI), 404 * 1.1 / float(DPI) + 0.5)
    fig.set_facecolor((0/255., 148/255., 89/255.))
    # -------------------------------
    plt.plot(dt_stamp, battery_level)
    plt.title('Battery plot')
    # plt.xlabel('Time')
    plt.ylabel('Battery percent')
    plt.xticks(rotation=30, fontsize = 'x-small')
    fig.canvas.flush_events()

    # Instead of plt.show()
    draw_fig_prep(window['fig_cv'].TKCanvas, fig)

def drawBlankFig(window):
    fig = plt.gcf()
    plt.clf()
    plt.grid(True)
    DPI = fig.get_dpi()
    fig.set_size_inches(404 * 3 / float(DPI), 404 * 1.1 / float(DPI) + 0.5)
    fig.get_axes()[0].set_xlim(0, 1)
    fig.get_axes()[0].set_ylim(0, 100)
    fig.set_facecolor((0/255., 148/255., 89/255.))
    plt.plot(0, 0)
    plt.title('Battery plot')
    plt.xlabel('Time')
    plt.ylabel('Battery percent')
    plt.xticks(rotation=30, fontsize = 'x-small')
    fig.canvas.flush_events()

    # Instead of plt.show()
    draw_fig_prep(window['fig_cv'].TKCanvas, fig)