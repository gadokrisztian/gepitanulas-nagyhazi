from abc import ABCMeta

import numpy as np

from whouserobot import WareHouseBase


class Robot(metaclass=ABCMeta):
    def __init__(self, warehouse: WareHouseBase):
        warehouse.generate()
        self.R = np.array(warehouse.s)
        self._N = self.R.shape[0]
        self.Q = np.zeros((self._N, self._N))

        self.gamma = 0.75
        self.alpha = 0.9
        self.niter = 1000

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

    def render_route(self, path):
        ...


if __name__ == "__main__":
    from whouserobot import ExampleWarehouse

    r = Robot(ExampleWarehouse())
    r.get_route(0, 10)
