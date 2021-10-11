import matplotlib.pyplot as plt
from abc import ABCMeta
import numpy as np
import itertools as it


class WareHouseBase(metaclass=ABCMeta):
    def __init__(self, width: int = 6, height: int = 4):
        self._w = width
        self._h = height
        self._N = self._w * self._h
        self.s = np.zeros((self._w, self._h))
        self.s = np.array([[0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                           [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                           [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
                           [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
                           [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]])

    def render(self):
        fig, ax = plt.subplots()

        cw = 1
        ch = 1

        plt.plot([-cw / 2, -cw / 2 + self._w], [-ch / 2, -ch / 2], 'b-', lw=2, zorder=10)
        plt.plot([-cw / 2, -cw / 2 + self._w], [-ch / 2 + self._h, -ch / 2 + self._h], 'b-', lw=2, zorder=10)
        plt.plot([-cw / 2, -cw / 2], [-ch / 2, -ch / 2 + self._h], 'b-', lw=2, zorder=10)
        plt.plot([-cw / 2 + self._w, -cw / 2 + self._w], [-ch / 2, -ch / 2 + self._h], 'b-', lw=2, zorder=10)

        # x0 = i // self._h
        # y0 = i % self._h
        # ax.scatter(x0, y0, c='red')

        for j in range(self._h):
            for i in range(self._w):
                n0 = i + j * self._w
                ax.text(i, j, n0)

                try:
                    if not self.s[n0, n0 + 1]:
                        ax.plot([i + cw / 2, i + cw / 2], [j - ch / 2, j + ch / 2], 'k-')

                    if not self.s[n0, n0 + self._w]:
                        ax.plot([i - cw / 2, i + cw / 2], [j + ch / 2, j + ch / 2], 'k-')

                except IndexError:
                    continue

        ax.text(self._w - 1, self._h - 1, self._N - 1)
        ax.axis('equal')
        ax.set_xticks(range(self._w))
        ax.set_yticks(range(self._h))
        return ax

    def __getitem__(self, idx):
        """
        i: xi
        j: yi

        k: xj
        l: yj

        """
        i, j, k, l = idx
        inrangex = lambda x: (x > -1) and (x < self._w)
        inrangey = lambda y: (y > -1) and (y < self._h)

        if inrangex(i) and inrangey(j):
            if inrangex(k) and inrangey(l):
                s1 = i + j * self._w
                s2 = k + l * self._w
                return self.s[s1][s2]
            else:
                return 0
        else:
            return 0


if __name__ == "__main__":
    w = WareHouseBase(4, 3)
    w.render()
    # plt.show()
    print(w[0, 1, 1, 1])
