import itertools as it
from abc import ABCMeta, abstractmethod

import matplotlib.pyplot as plt
import numpy as np

from whouserobot import Dir


def pairwise(iterable):
    a, b = it.tee(iterable)
    next(b, None)
    return zip(a, b)


class WareHouseBase(metaclass=ABCMeta):
    def __init__(self, width: int, height: int):
        """
        Initialize the warehouse with it's dimensions.

        :param width: The width of the warehouse
        :param type: int

        :param height: The height of the warehouse.
        :param type: int
        """
        self._w = width
        self._h = height
        self._N = self._w * self._h
        self.s = np.zeros((self._N, self._N), dtype=int)

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

        def drawline(x0, y0, x1, y1):
            ax.plot([x0, x1], [y0, y1], "k-", lw=2)

        for si in range(self._N - 1):
            i, j = self.state2coord(si)
            ax.text(i, j, si, horizontalalignment="center", verticalalignment="center")

            if not self.s[si, si + 1]:
                drawline(i + cw / 2, j + ch / 2, i + cw / 2, j - ch / 2)

            if si + self._w < self._N:
                if not self.s[si, si + self._w]:
                    drawline(i - cw / 2, j + ch / 2, i + cw / 2, j + ch / 2)

        ax.axis("equal")
        ax.set_xticks(range(self._w))
        ax.set_yticks(range(self._h))
        return ax

    def validate_states(self):
        """
        Check if a state matrix is valid. Should be symmetric and only
        neighbouring tiles can be connected. Also the robot should be able to
        travel from any tile to any other tile, therefore no isolated tile
        can exist.
        """
        # TODO: fill this
        return True

    def coord2state(self, i: int, j: int):
        return i + j * self._w

    def state2coord(self, si: int):
        assert si > -1
        assert si < self._N
        row = si % self._w
        col = (si - row) // self._w
        return row, col

    def __len__(self):
        return self._N


class ExampleWarehouse(WareHouseBase):
    def __init__(self):
        super().__init__(4, 3)

    def generate(self):
        self.s = np.array(
            [
                [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
                [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            ]
        )


class RandomWareHouse(WareHouseBase):
    """
    This is a random layout generator, it will certainly generate a layout that
    is not fully connected.
    """

    def generate(self):
        """
        Generate a random symmetric matrix.
        """
        self.s = np.random.choice([0, 1], p=(0.12, 0.88), size=(self._N, self._N))
        self.s = (self.s + self.s.T) // 2
        self.s = self.s.astype(int)


if __name__ == "__main__":
    np.random.seed(4812)
    w = ExampleWarehouse()
    w = RandomWareHouse(10, 10)
    w.generate()
    ax = w.render()
    plt.show()
    plt.savefig(Dir.MEDIA / "example_warehouse.png", dpi=450)
