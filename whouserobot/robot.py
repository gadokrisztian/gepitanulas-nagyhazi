from abc import ABCMeta, abstractmethod

import matplotlib.pyplot as plt
import numpy as np

from whouserobot import Dir, WareHouseBase
from itertools import tee

def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

class RobotBase(metaclass=ABCMeta):
    def __init__(self, warehouse: WareHouseBase):
        self.whouse = warehouse
        self.whouse.generate()
        self._N = len(self.whouse)

    @abstractmethod
    def get_route(self, from_: int, to_: int):
        ...

    def render_route(self, path):
        ax = self.whouse.render()

        i, j = self.whouse.state2coord(path[0])
        ax.scatter(i + 0.1, j - 0.1, c="red", s=250, zorder=100, label=f"Start: {path[0]}")

        i, j = self.whouse.state2coord(path[-1])
        ax.scatter(i + 0.1, j - 0.1, c="green", s=250, zorder=100, label=f"End: {path[-1]}")

        for si, sj in pairwise(path):
            i, j = self.whouse.state2coord(si)
            k, l = self.whouse.state2coord(sj)

            plt.plot([i + 0.1, k + 0.1], [j - 0.1, l - 0.1], color="purple", lw=5)

        # plt.legend()
        # plt.show()
        return ax


class QLRobot(RobotBase):
    def __init__(self, warehouse: WareHouseBase, **kwargs):
        super().__init__(warehouse)

        self.R = np.array(warehouse.s)
        self.Q = np.zeros((self._N, self._N))

        self.gamma = kwargs.get("gamma", 0.75)
        self.alpha = kwargs.get("alpha", 0.9)
        self.niter = kwargs.get("niter", 1000)

        self.current_goal = 0

    def calculate_q_values(self):
        self.Q = np.zeros((self._N, self._N))
        for i in range(self.niter):
            current_state = np.random.randint(0, self._N)
            playable_actions = []
            for j in range(self._N):
                if self.R[current_state, j] > 0:
                    playable_actions.append(j)

            next_state = np.random.choice(playable_actions)
            TD = (
                self.R[current_state, next_state]
                + self.gamma
                * self.Q[
                    next_state,
                    np.argmax(
                        self.Q[
                            next_state,
                        ]
                    ),
                ]
                - self.Q[current_state, next_state]
            )
            self.Q[current_state, next_state] += self.alpha * TD

    def get_route(self, from_: int, to_: int):
        self.R[self.current_goal, self.current_goal] = 0
        self.R[to_, to_] = 1000
        self.current_goal = to_
        self.calculate_q_values()

        route = [from_]
        next_location = from_
        while next_location != to_:
            next_location = np.argmax(
                self.Q[
                    from_,
                ]
            )
            route.append(next_location)
            from_ = next_location

        print(route)
        return route


if __name__ == "__main__":

    from whouserobot import ExampleWarehouse

    # r = QLRobot(ExampleWarehouse())
    r = QLRobot(ExampleWarehouse())
    route = r.get_route(4, 10)
    r.render_route(route)
    plt.savefig(Dir.MEDIA / "example_route.png", dpi=330)
    plt.show()
