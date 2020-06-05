import numpy as np
import matplotlib.pyplot as plt
from proj1.tsp import ConnectedGraph, TspSimAnn
from matplotlib.animation import FuncAnimation


def update_line(line, new_x, new_y):
    line.set_xdata(np.append(line.get_xdata(), new_x))
    line.set_ydata(np.append(line.get_ydata(), new_y))


class Plot:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, autoscale_on=False)
        self.line, = self.ax.plot([], [], "o")

        self.fig.canvas.mpl_connect('button_press_event', self.on_click)

    def add_point(self, event):
        x, y = event.xdata, event.ydata
        update_line(self.line, [x], [y])

    def on_click(self, event):
        if self.line.contains(event)[0]:
            return
        self.add_point(event)
        self.fig.canvas.draw()

    def clear(self):
        self.fig.clf()
        self.ax = self.fig.add_subplot(111, autoscale_on=False)
        self.fig.add_subplot(self.ax)
        self.line, = self.ax.plot([], [], "o")
        self.fig.canvas.draw()

    def animate(self, steps=200, t=10, alpha=0.95):
        p_x_coord = self.line.get_xdata().reshape(-1, 1)
        p_y_coord = self.line.get_ydata().reshape(-1, 1)
        points_coord = np.append(p_x_coord, p_y_coord, axis=1)

        g = ConnectedGraph(points_coord=points_coord)
        sim_ann = TspSimAnn(g, t=t, alpha=alpha)

        ln, = self.ax.plot([], [], "r")

        def update(frame):
            sim_ann.step()
            cx, cy = sim_ann.get_connections_data()
            ln.set_data(cx, cy)
            self.ax.legend([], title=f"Step: {frame + 1}", frameon=False)
            return ln,

        ani = FuncAnimation(self.fig, update, save_count=1, frames=steps, repeat=False, interval=20)
        self.fig.canvas.draw()


def main():
    p = Plot()
    #
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # line, = ax.plot(np.random.rand(100), 'o', picker=5)  # 5 points tolerance
    # update_line(line, [0, 10], [0, 0.1])
    # fig.canvas.draw()
    plt.show()


if __name__ == '__main__':
    main()
