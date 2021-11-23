from abc import ABCMeta, abstractmethod
from itertools import tee

import matplotlib.pyplot as plt
import numpy as np

from whouserobot import Dir, WareHouseBase


def pairwise(iterable):
    """
    A simple pairwise iterator.
    pairwise('ABCD') -> AB BC CD
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class RobotBase(metaclass=ABCMeta):
    """
    This is the base class for any kinds of warehouse robot.
    """

    def __init__(self, warehouse: WareHouseBase):
        self.whouse = warehouse
        self.whouse.generate()
        self._N = len(self.whouse)

    @abstractmethod
    def get_route(
        self,
        from_: int,
        to_: int,
    ):
        """
        This is the method that calculates the route between 2 tiles. All subclass should
        implement this method.
        """
        ...

    def render_route(self, path):
        """
        This method plots the route on the warehouse.
        """
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
    """
    This type of robot implements the Q-learning to find a path
    between 2 tiles.
    """

    def __init__(self, warehouse: WareHouseBase, **kwargs):
        super().__init__(warehouse)

        # Reward matrix
        self.R = np.array(warehouse.s)
        # Q values
        self.Q = np.zeros((self._N, self._N))

        self.gamma = kwargs.get("gamma", 0.75)  # discount factor
        self.alpha = kwargs.get("alpha", 0.9)  # learning rate
        self.niter = kwargs.get("niter", 1000)  # number of rounds for the Q learning

        self.current_goal = 0

    def calculate_q_values(self):
        """
        This function calculates the Q values for a given goal tile.
        """
        self.Q = np.zeros((self._N, self._N))
        for i in range(self.niter):
            current_state = np.random.randint(0, self._N)
            playable_actions = []
            for j in range(self._N):
                if self.R[current_state, j] > 0:
                    playable_actions.append(j)

            next_state = np.random.choice(playable_actions)

            # calculating temporal difference
            TD = self.R[current_state, next_state]
            TD += self.gamma * self.Q[next_state, np.argmax(self.Q[next_state])]
            TD -= self.Q[current_state, next_state]

            self.Q[current_state, next_state] += self.alpha * TD

    def get_route(self, from_: int, to_: int):

        # reset the previous goal
        self.R[self.current_goal, self.current_goal] = 0

        # set the new goal
        self.R[to_, to_] = 1000
        self.current_goal = to_

        # calculate the Q-values based on the new goal
        self.calculate_q_values()

        # build the route
        route = [from_]
        next_location = from_
        while next_location != to_:
            next_location = np.argmax(self.Q[from_])
            route.append(next_location)
            from_ = next_location

        print(route)
        return route


if __name__ == "__main__":
    from whouserobot import ExampleWarehouse

    r = QLRobot(ExampleWarehouse())
    route = r.get_route(3, 8)
    r.render_route(route)
    plt.savefig(Dir.MEDIA / "example_route3.png", dpi=330)
    plt.show()
