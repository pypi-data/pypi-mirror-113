# mod_plot.py - Moderation Plots, rcampbel, March 2021
#try:
#...
#except Exception as e:
#    import sys
#    sys.stdout = open('/dev/stdout', 'w')
#    print('...(): "'+str(e)+'"')

import numpy as np
from itertools import cycle
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib import rcParams
from matplotlib import widgets as mpl

ZOOM_OUT = '-'
ZOOM_IN = '+'
X_TOLERANCE = 0.1
Y_TOL_DIV = 50
LOW = 'Low'
HIGH = 'High'

class ModerationPlot:
    """Plot line(s) with movable end markers"""
    # Ref: https://stackoverflow.com/questions/34855074/interactive-line-in-matplotlib

    def __init__(self, out, title, xvar, names, est, values, debug_out, width=3, height=1.75):
        plt.ioff()  # Required to display plots separately  TODO Confirm
        rcParams.update({'font.size': 6})
        rcParams['legend.handlelength'] = 0
        rcParams['legend.numpoints'] = 1
        self.title = title
        self.xvar = xvar
        self.out = out
        self.names = names
        self.est = est
        self.values = values  # List of PredVal's
        self.debug_out = debug_out
        self.xs = []
        self.ys = []
        self.ymin = 0
        self.ymax = 0

        for i in range(len(self.names)):
            self.xs.append([-1.0, 1.0])
            self.ys.append([0, 0])

        self.fig = plt.figure(figsize=[width, height])
        self.axes = self.fig.add_subplot()
        self.lines = []
        self.cur_line = None  # Selected line: index into self.lines or None
        self.ind = None  # Index of selected start/end point: None, 0, or 1
        self.y_tolerance = None  # Y-axis distance for start/end point click detection

        self.fig.suptitle(title, x=0.4, y=0.99, size='large')
        #self.fig.tight_layout(pad=0, w_pad=0, h_pad=0)  #  TODO Remove dead code?
        self.fig.subplots_adjust(right=0.80)

        # Interactive canvas has a lot of features we want to hide
        self.fig.canvas.toolbar_visible = False
        self.fig.canvas.header_visible = False # Hide name at top of figure
        self.fig.canvas.footer_visible = False
        self.fig.canvas.resizable = False
        self.fig.canvas.capture_scroll = False

        # Create plot components, store lines

        line_cycler = cycle(["-"])  # TODO Use different line styles? ,"--","-.",":"])
        marker_cycler = cycle(['d','s','o','+','*','x'])

        for i in range(len(self.names)):
            line = Line2D(self.xs[i],self.ys[i], label=self.names[i],
                          marker=next(marker_cycler), c='black', markerfacecolor='black',
                          linestyle=next(line_cycler), picker=True)
            self.axes.add_line(line)
            self.lines.append(line)

        #self.axes.set_ylabel(est.land.dep_var.value)
        self.axes.set_ylabel(est.model.dep_var)
        self.axes.yaxis.set_label_coords(-0.19,0.5)
        self.fig.subplots_adjust(left=0.17)

        self.axes.autoscale()
        self.axes.legend(loc='right', bbox_to_anchor=(1.27, 0.5), borderaxespad=0.0, frameon=False)
        self.axes.set_xticklabels(['',LOW+' '+self.xvar,'','','',HIGH+' '+self.xvar])

        # Note: Keeping refs to Button()'s to prevent gc
        self.zoom_out = mpl.Button(plt.axes([0.81, 0.79, 0.05, 0.07]), ZOOM_OUT, color='1')
        self.zoom_in = mpl.Button(plt.axes([0.88, 0.79, 0.05, 0.07]), ZOOM_IN, color='1')

        # Register our methods as event callbacks
        self.fig.canvas.mpl_connect('button_press_event', self.on_button_press)
        #self.fig.canvas.mpl_connect('button_release_event', self.on_button_release)
        #self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion_notify)
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)

        self.adjust_y_tolerance()
        plt.ion()  # Required to display plots separately  TODO Confirm

        with self.out:
            self.fig.show()

    def reset_colors(self):

        for line in self.lines:
            line.set_color('black')

    def on_pick(self, event):

        # Calc slope

        x = event.artist.get_xdata()
        y = event.artist.get_ydata()

        if float(x[1]) - float(x[0]) == 0.0:
            slope = 0.0
        else:
            slope = (float(y[1]) - float(y[0])) / (float(x[1]) - float(x[0]))

        # Highlight selected line, update status text
        self.est.on_plot_select(self.title, event.artist.get_label(), slope)
        event.artist.set_color('cyan')

    def debug(self, str, end='\n'):
        with self.debug_out:
            print(str, end)

    def update(self, lines):
        """Change plot to reflect new line start/end point locations"""

        for i, line in enumerate(lines):
            self.lines[i].set_data([line[0][0],line[1][0]], [line[0][1],line[1][1]])

        # Crude auto zoom TODO Why autoscale() no worky worky?

        self.ymin = min(self.ymin, line[0][1], line[1][1])
        self.ymax = max(self.ymin, line[0][1], line[1][1])
        view_low, view_high = self.axes.get_ylim()

        while self.ymin < view_low or self.ymax > view_high:
            self.scale(-1,+1)
            view_low, view_high = self.axes.get_ylim()

        # TODO Auto zoom out? - Currently cancels zoom in

        #prop = abs(self.ymax - self.ymin) / abs(view_high - view_low)

        #while prop < 0.07:
        #    self.scale(+1,-1)
        #    view_low, view_high = self.axes.get_ylim()
        #    prop = abs(self.ymax - self.ymin) / abs(view_high - view_low)

        # self.debug('"'+self.title+'": '+str(self.ymin)+' '+str(self.ymax)+' w/in '+str(view_low)+' '+str(view_high)+' prop='+str(prop))

    def set_layout(self, new_layout):
        self.layout = new_layout

    def adjust_y_tolerance(self):
        ylim = self.axes.get_ylim()
        self.y_tolerance = (ylim[1] - ylim[0]) / Y_TOL_DIV

    def scale(self, lower_change, upper_change):
        """Change Y-axis limits, copensate y click distance, redraw"""
        ylim = self.axes.get_ylim()
        self.axes.set_ylim([ylim[0]+lower_change, ylim[1]+upper_change])
        self.adjust_y_tolerance()
        self.fig.canvas.draw()

    def on_button_press(self, event):
        if event.button == 1:

            # Adjust axes?
            if event.inaxes == self.zoom_out.ax:
                self.scale(-1,+1)
            elif event.inaxes == self.zoom_in.ax:
                self.scale(+1,-1)

            else: # Starting to drag line start/end point?
                self.cur_line = None
                self.ind = None

                for i in range(len(self.names)):
                    x = np.array(self.lines[i].get_xdata())
                    y = np.array(self.lines[i].get_ydata())
                    d = np.sqrt((x-event.xdata)**2 + (y - event.ydata)**2)

                    if min(d) <= self.y_tolerance:
                        self.cur_line = i
                        self.ind = 0 if d[0] < d[1] else 1
                        break

                if self.cur_Line is None:
                    self.est.on_plot_change()
                else:
                    self.est.on_plot_change(self.xvar,self.names[self.cur_line])

    def on_motion_notify(self, event):

        if event.button == 1 and self.ind is not None and self.cur_line is not None:
            if event.inaxes == self.lines[self.cur_line].axes:
                self.xs[self.cur_line][self.ind] = self.ind + 1
                self.ys[self.cur_line][self.ind] = event.ydata
                self.lines[self.cur_line].set_data(self.xs[self.cur_line],
                                                self.ys[self.cur_line])

                # Calc slope
                if self.xs[self.cur_line][1] - self.xs[self.cur_line][0] == 0:
                    slope = 0.0
                else:
                    slope = (self.ys[self.cur_line][1] - self.ys[self.cur_line][0]) / \
                            (self.xs[self.cur_line][1] - self.xs[self.cur_line][0])

                self.est.on_plot_change(self.xvar,self.names[self.cur_line],slope)

    def on_button_release(self, event):

        if event.button == 1:
            self.ind = None
            self.background = None

            if self.cur_line is not None:
                self.lines[self.cur_line].figure.canvas.draw()

            self.cur_line = None
            self.est.on_plot_change()
