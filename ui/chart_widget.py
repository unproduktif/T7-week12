# Nama  : Dodi Wijaya
# NIM   : F1D02310047
# Kelas : Pemrograman Visual D

from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg
)

from matplotlib.figure import Figure


class ChartWidget(FigureCanvasQTAgg):

    def __init__(self):

        self.figure = Figure(
            figsize=(8, 5)
        )

        super().__init__(self.figure)

        self.axes = self.figure.add_subplot(111)

    def clear_chart(self):

        self.axes.clear()

    def draw_chart(self):

        self.figure.subplots_adjust(
            left=0.08,
            right=0.95,
            top=0.88,
            bottom=0.25
        )

        self.draw()