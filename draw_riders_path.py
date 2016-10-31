"""
Show how to override basic methods so an artist can contain another
artist.  In this case, the line contains a Text instance to label it.
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import matplotlib.transforms as mtransforms
import matplotlib.text as mtext


class MyLine(lines.Line2D):
    def __init__(self, *args, **kwargs):
        # we'll update the position when the line data is set
        self.text = mtext.Text(0, 0, '')
        lines.Line2D.__init__(self, *args, **kwargs)

        # we can't access the label attr until *after* the line is
        # inited
        self.text.set_text(self.get_label())

    def set_figure(self, figure):
        self.text.set_figure(figure)
        lines.Line2D.set_figure(self, figure)

    def set_axes(self, axes):
        self.text.set_axes(axes)
        lines.Line2D.set_axes(self, axes)

    def set_transform(self, transform):
        # 2 pixel offset
        texttrans = transform + mtransforms.Affine2D().translate(2, 2)
        self.text.set_transform(texttrans)
        lines.Line2D.set_transform(self, transform)

    def set_data(self, x, y):
        if len(x):
            self.text.set_position((x[-1], y[-1]))

        lines.Line2D.set_data(self, x, y)

    def draw(self, renderer):
        # draw my label at the end of the line with 2 pixel offset
        lines.Line2D.draw(self, renderer)
        self.text.draw(renderer)


riders_path = {}
colors = ('b', 'g', 'r', 'c', 'm', 'y', 'k')

def prepare(input_file):
    with open(input_file, "r") as f:
        for line in f:
            fields = line.strip().split(",")
            rider_id = int(fields[0])
            point = (float(fields[2]), float(fields[3]))
            if (riders_path.get(rider_id, None) == None):
                riders_path.setdefault(rider_id, [point])
            else:
                riders_path.get(rider_id).append(point)


def prepare_plot():
    fig, ax = plt.subplots()
    ax.set_title("alex")
    ax.set_ylim((31.1, 31.3))
    ax.set_xlim((121.3, 121.5))

    return ax


def generate_lines(ax):
    count = 0
    for rider, path in riders_path.items():
        count += 1
        x = []
        y = []
        for p in path:
            x.append(p[0])
            y.append(p[1])

        x = np.array(x)
        y = np.array(y)
        color = colors[count%len(colors)]
        line = MyLine(x, y, mfc=color, ms=12, label='rider {}'.format(str(rider)))
        line.set_color(color)
        line.text.set_color(color)
        line.text.set_fontsize(16)

        ax.add_line(line)

        if count >= 5:
            break


def run(input_file):
    prepare(input_file)
    ax = prepare_plot()
    generate_lines(ax)
    plt.show()



if __name__ == "__main__":
    run(sys.argv[1])