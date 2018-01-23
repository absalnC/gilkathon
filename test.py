import numpy as np

x = np.zeros((3, 3))
x[1][1] = 1

class MyApp(QtWidgets.QMainWindow):

    def _func_1_(self):

        global x

        print("x[1][1] =", x[1][1])  # Primera Salida

        self.aux = x
        self.aux[1][1] = _func_2_(aux[1][1])

        print("x[1][1] =", x[1][1])  # Segunda Salida

    def _func_2_(self, value):

        return (value * 10)


    $ x[1][1] = 1
    $ x[1][1] = 10