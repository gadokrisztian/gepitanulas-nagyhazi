from abc import ABCMeta, abstractmethod

import matplotlib.pyplot as plt
import numpy as np


class WareHouseBase(metaclass=ABCMeta):
    def __init__(self, width: int, height: int):
        self._w = width
        self._h = height
        self._N = self._w * self._h
        self.s = np.zeros((self._N, self._N))

    @abstractmethod
    def generate(self):
        ...

    def render(self):
        """
        Print the warehouse using matplotlib. The function returns the ax object to further modifications and plots.

        :return: ax
        """
        # create the figure
        fig, ax = plt.subplots()

        # cell width and cell height
        cw = 1
        ch = 1

        # draw the blue boundary lines
        ax.plot([-cw / 2, -cw / 2 + self._w], [-ch / 2, -ch / 2], "b-", lw=2, zorder=10)
        ax.plot([-cw / 2, -cw / 2 + self._w], [-ch / 2 + self._h, -ch / 2 + self._h], "b-", lw=2, zorder=10)
        ax.plot([-cw / 2, -cw / 2], [-ch / 2, -ch / 2 + self._h], "b-", lw=2, zorder=10)
        ax.plot([-cw / 2 + self._w, -cw / 2 + self._w], [-ch / 2, -ch / 2 + self._h], "b-", lw=2, zorder=10)

        for j in range(self._h):
            for i in range(self._w):
                n0 = i + j * self._w
                ax.text(i, j, n0, horizontalalignment="center", verticalalignment="center")

                def drawline(x0, y0, x1, y1):
                    ax.plot([x0, x1], [y0, y1], "k-", lw=2)

                # right wall
                if not self[i, j, i + 1, j]:
                    drawline(i + cw / 2, j - ch / 2, i + cw / 2, j + ch / 2)

                # left wall
                if not self[i, j, i - 1, j]:
                    drawline(i - cw / 2, j - ch / 2, i - cw / 2, j + ch / 2)

                # ceiling wall
                if not self[i, j, i, j + 1]:
                    drawline(i - cw / 2, j + ch / 2, i + cw / 2, j + ch / 2)

                # floor wall
                if not self[i, j, i, j - 1]:
                    drawline(i - cw / 2, j - ch / 2, i + cw / 2, j - ch / 2)

        ax.axis("equal")
        ax.set_xticks(range(self._w))
        ax.set_yticks(range(self._h))
        return ax

    def __getitem__(self, idx):
        """
        Check if cell (i,j) and (k,l) are connected.
        If they are connected return 1 else 0.

        i: xi
        j: yi

        k: xj
        l: yj
        """
        i, j, k, l = idx

        inrangex = lambda x: (x > -1) and (x < self._w)
        inrangey = lambda y: (y > -1) and (y < self._h)

        if inrangex(i) and inrangey(j) and inrangex(k) and inrangey(l):
            s1 = i + j * self._w
            s2 = k + l * self._w
            return self.s[s1][s2]
        else:
            return 0


class RandomWareHouse(WareHouseBase):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.generate()

    def generate(self):
        self.s = np.random.choice([0, 1], p=(0.12, 0.88), size=(self._N, self._N))
        self.s = (self.s + self.s.T) // 2
