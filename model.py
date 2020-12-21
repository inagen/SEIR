import sys
import random
import matplotlib
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import pandas as pd

matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def recalculate_arrays(self):
        h = 1
        self.s[0] = self.people_cnt - (self.begin_e + self.begin_i)
        self.e[0] = self.begin_e
        self.i[0] = self.begin_i
        self.r[0] = 0
        self.n[0] = self.people_cnt;

        self.s1[0] = self.s[0] + h*(self.mu*(self.n[0] - self.s[0]) - self.beta*(self.i[0] / self.n[0])*self.s[0])
        self.e1[0] = self.e[0] + h*(self.beta*(self.i[0] / self.n[0])*self.s[0] - (self.mu + self.alfa)*self.e[0])
        self.i1[0] = self.i[0] + h*(self.alfa*self.e[0] - (self.gamma + self.mu) * self.i[0])
        self.r1[0] = self.r[0] + h*(self.gamma*self.i[0] - self.mu*self.r[0])
        self.n1[0] = self.s1[0] + self.e1[0] + self.i1[0] + self.r1[0]
        for i in range(1, self.day_cnt):
            self.s[i] = self.s[i - 1] + h/2 * (self.mu*(self.n[i-1]+self.n1[i-1]) - self.mu*(self.s[i-1]+self.s1[i-1]) - self.beta*(self.i[i-1]*self.s[i-1]/self.n[i-1] + self.i1[i-1]*self.s1[i-1]/self.n1[i-1]))
            if self.s[i] < 0:
                self.s[i] = 0
            if self.s[i] > self.n[i - 1]:
                self.s[i] = self.n[i - 1]

            self.e[i] = self.e[i - 1] + h/2 * (self.beta*(self.i[i-1]*self.s[i-1]/self.n[i-1] + self.i1[i-1]*self.s1[i-1]/self.n1[i-1]) - (self.mu + self.alfa)*(self.e[i-1] + self.e1[i-1]))
            if self.e[i] < 0:
                self.e[i] = 0
            if self.e[i] > self.n[i - 1]:
                self.e[i] = self.n[i - 1]

            self.i[i] = self.i[i - 1] + h/2 * (self.alfa*(self.e[i-1]+self.e1[i-1]) - (self.gamma + self.mu)*(self.i[i-1]+self.i1[i-1]))
            if self.i[i] < 0:
                self.i[i] = 0
            if self.i[i] > self.n[i - 1]:
                self.i[i] = self.n[i - 1]
            self.r[i] = self.r[i - 1] + h/2 * (self.gamma*(self.i[i-1]+self.i1[i-1]) - self.mu*(self.r[i-1] + self.r1[i-1]))
            if self.r[i] < 0:
                self.r[i] = 0
            if self.r[i] > self.n[i - 1]:
                self.r[i] = self.n[i - 1]

            self.n[i] = self.s[i] + self.e[i] + self.i[i] + self.r[i]
            if self.n[i] == 0:
                self.n[i] = 0
            if self.n[i] > self.n[i - 1]:
                self.n[i] = self.n[i - 1]
            self.s1[i] = self.s[i] + h * (self.mu * (self.n[i] - self.s[i]) - self.beta * (self.i[i] / self.n[i]) * self.s[i])
            self.e1[i] = self.e[i] + h * (self.beta * (self.i[i] / self.n[i]) * self.s[i] - (self.mu + self.alfa) * self.e[i])
            self.i1[i] = self.i[i] + h * (self.alfa * self.e[i] - (self.gamma + self.mu) * self.i[i])
            self.r1[i] = self.r[i] + h * (self.gamma * self.i[i] - self.mu * self.r[i])
            self.n1[i] = self.s1[i] + self.e1[i] + self.i1[i] + self.r1[i]

    def clear_plot(self):
        self.layout.removeWidget(self.canvas)
        self.canvas = MplCanvas(self, width=800, height=600, dpi=100)
        self.canvas.axes.set_xlabel("Время (в днях)")
        self.canvas.axes.set_ylabel("Количество (в человеках)")
        self.layout.addWidget(self.canvas)

    def update_plot(self):
        self.clear_plot()
        self.mu = self.mu_spinbox.value() / 100
        self.alfa = self.alfa_spinbox.value()
        self.beta = self.beta_spinbox.value() / 100
        self.gamma = self.gamma_spinbox.value() / 100
        self.begin_e = self.e_spinbox.value()
        self.begin_i = self.i_spinbox.value()

        self.recalculate_arrays()
        #df = pd.DataFrame(self.s, columns=['S'])
        df = pd.DataFrame([[self.s[i], self.e[i], self.r[i], self.i[i]] for i in range(self.day_cnt)],
                          columns=self.columns_names)
        df = df.astype(float)
        df.plot(ax=self.canvas.axes)

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.begin_e = 10
        self.begin_i = 5
        self.columns_names = ['S', 'E', 'R', 'I']
        self.day_cnt = 365
        self.people_cnt = 100
        self.mu = 0
        self.alfa = 0
        self.beta = 0
        self.gamma = 0

        self.s = [0] * self.day_cnt
        self.e = [0] * self.day_cnt
        self.i = [0] * self.day_cnt
        self.r = [0] * self.day_cnt
        self.n = [0] * self.day_cnt
        self.s1 = [0] * self.day_cnt
        self.e1 = [0] * self.day_cnt
        self.i1 = [0] * self.day_cnt
        self.r1 = [0] * self.day_cnt
        self.n1 = [0] * self.day_cnt



        self.canvas = MplCanvas(self, width=1000, height=700, dpi=100)

        mu_layout = QHBoxLayout()
        mu_label = QLabel("μ — смертность (1/чел)")
        self.mu_spinbox = QDoubleSpinBox(self)
        self.mu_spinbox.setValue(self.mu)
        mu_layout.addWidget(mu_label)
        mu_layout.addWidget(self.mu_spinbox)

        alfa_layout = QHBoxLayout()
        alfa_label = QLabel("α — обр. среднему инкубационному периоду заболевания (дни)")
        self.alfa_spinbox = QDoubleSpinBox(self)
        self.alfa_spinbox.setValue(self.alfa)
        self.alfa_spinbox.setMaximum(1)
        self.alfa_spinbox.setSingleStep(0.01)
        alfa_layout.addWidget(alfa_label)
        alfa_layout.addWidget(self.alfa_spinbox)

        beta_layout = QHBoxLayout()
        beta_label = QLabel("β — интенсивность контактов индивидов (1/день)")
        self.beta_spinbox = QDoubleSpinBox(self)
        self.beta_spinbox.setValue(self.beta)
        beta_layout.addWidget(beta_label)
        beta_layout.addWidget(self.beta_spinbox)

        gamma_layout = QHBoxLayout()
        gamma_label = QLabel("γ — интенсивность выздоровления индивидов (1/день)")
        self.gamma_spinbox = QDoubleSpinBox(self)
        self.gamma_spinbox.setValue(self.gamma)
        gamma_layout.addWidget(gamma_label)
        gamma_layout.addWidget(self.gamma_spinbox)

        e_layout = QHBoxLayout()
        e_label = QLabel("Начальное количество переносчиков заболевания (чел)")
        self.e_spinbox = QDoubleSpinBox(self)
        self.e_spinbox.setValue(self.begin_e)
        e_layout.addWidget(e_label)
        e_layout.addWidget(self.e_spinbox)

        i_layout = QHBoxLayout()
        i_label = QLabel("Начальное количество больных (чел)")
        self.i_spinbox = QDoubleSpinBox(self)
        self.i_spinbox.setValue(self.begin_i)
        i_layout.addWidget(i_label)
        i_layout.addWidget(self.i_spinbox)

        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addLayout(mu_layout)
        self.layout.addLayout(alfa_layout)
        self.layout.addLayout(beta_layout)
        self.layout.addLayout(gamma_layout)
        self.layout.addLayout(e_layout)
        self.layout.addLayout(i_layout)


        self.mu_spinbox.valueChanged.connect(self.update_plot)
        self.alfa_spinbox.valueChanged.connect(self.update_plot)
        self.beta_spinbox.valueChanged.connect(self.update_plot)
        self.gamma_spinbox.valueChanged.connect(self.update_plot)
        self.i_spinbox.valueChanged.connect(self.update_plot)
        self.e_spinbox.valueChanged.connect(self.update_plot)


        widget = QtWidgets.QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        self.setWindowTitle("SEIR model")
        self.setFixedHeight(720)
        self.setFixedWidth(1280)
        self.update_plot()
        self.show()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
jopa = 1