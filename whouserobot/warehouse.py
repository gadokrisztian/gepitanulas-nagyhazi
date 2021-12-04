from abc import ABCMeta, abstractmethod
from random import choices, seed

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


class WareHouseBase(metaclass=ABCMeta):
    """
    This class contains the structure of the warehouse.
    """

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

        # state matrix
        self._init_warehouse()

    @abstractmethod
    def generate(self, **kwargs):
        """
        Every warehouse class should have a generate method where the state matrix is going to be populated.
        """
        ...

    def _init_warehouse(self):
        """
        Initialize the warehouse with no walls between any tiles. This by generating a
        von Neuman grid graph and turning it into an adjacency matrix.
        """
        G = nx.grid_graph(dim=(self._w, self._h))
        self.s = nx.adjacency_matrix(G).todense()

    def render(self):
        """
        Print the warehouse using matplotlib. The function returns the ax object to further modifications and plots.

        :return: ax
        """
        # create the figure
        fig, ax = plt.subplots(figsize=(10, 8))

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

        i, j = self.state2coord(si + 1)
        ax.text(i, j, si + 1, horizontalalignment="center", verticalalignment="center")
        ax.axis("equal")
        ax.set_xticks(range(self._w))
        ax.set_yticks(range(self._h))
        return ax

    def coord2state(self, i: int, j: int):
        """
        This method maps the i,j coordinates of the warehouse to a state.
        """
        return i + j * self._w

    def state2coord(self, si: int):
        """
        This function maps an integer state to the coordinates of the warehouse.
        """
        assert si > -1
        assert si < self._N
        row = si % self._w
        col = (si - row) // self._w
        return row, col

    def __len__(self):
        """
        This method gives back the number of states.
        """
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


class RandomWarehouse(WareHouseBase):
    """
    This is a simple implementation of a random warehouse. The generated
    warehouse will have random walls, but it is ensured that any tile can be
    reached from any other tile.
    """

    def __init__(self, width: int, height: int, **kwargs):
        super().__init__(width, height)
        self.nb_walls = kwargs.get("walls", 2)
        self.seed = kwargs.get("seed", 4812)

    def generate(self):
        """
        This method generates a random warehouse. Be careful it can stuck in an infinite loop if
        the number of walls is too high. In this case try to lower the number of walls or
        use an another seed for the random generator.

        Parameters:
            walls: The number of walls
            seed: seed value for the random generator

        """

        seed(self.seed)

        G = nx.grid_graph(dim=(self._w, self._h))

        while self.nb_walls:
            u, v = choices(tuple(G.nodes), k=2)
            if G.has_edge(u, v):
                G.remove_edge(u, v)
                if nx.is_connected(G):
                    self.nb_walls -= 1
                else:
                    G.add_edge(u, v)

        self.s = nx.adjacency_matrix(G).todense()


# if __name__ == "__main__":
#     from whouserobot import Dir

#     w = RandomWarehouse(3, 3, seed=65, walls=4)
#     # w = ExampleWarehouse()
#     w.generate()
#     ax = w.render()
#     # plt.savefig(Dir.MEDIA / "example_warehouse.png", dpi=330)
#     plt.show()
