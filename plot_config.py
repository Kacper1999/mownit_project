import numpy as np
import matplotlib.pyplot as plt
from tsp import Map


class Plot:
    def __init__(self):
        self.m = Map(0)
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, autoscale_on=False)
        self.line, = self.ax.plot([], [], "o", picker=5)

        self.prev_ind = None  # prev point to draw line

        self.fig.canvas.mpl_connect('button_press_event', self.on_click)

    def update_line(self, new_x, new_y):
        self.line.set_xdata(np.append(self.line.get_xdata(), new_x))
        self.line.set_ydata(np.append(self.line.get_ydata(), new_y))

    def add_line(self, ind):
        prev_p = self.m.get_p(self.prev_ind)
        p = self.m.get_p(ind)
        if not self.m.add_connection(prev_p, p):  # add_connection returns False when connection already exists
            return False
        x = [p.x(), prev_p.x()]
        y = [p.y(), prev_p.y()]
        self.ax.plot(x, y, "r")
        return True

    def add_point(self, event):
        x, y = event.xdata, event.ydata
        self.update_line([x], [y])
        self.m.add_point((x, y))

    def on_click(self, event):
        if self.line.contains(event)[0]:
            ind = self.line.contains(event)[1]["ind"][0]
            if self.prev_ind is not None:
                if self.add_line(ind):
                    self.prev_ind = None
            else:
                self.prev_ind = ind
        else:
            self.add_point(event)
            self.prev_ind = None
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

    print(p.m.is_connected())


if __name__ == '__main__':
    main()
