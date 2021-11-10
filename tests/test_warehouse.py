import numpy as np

from whouserobot import RandomWareHouse, WareHouseBase


class ExampleWarehouse(WareHouseBase):
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


def test_warehouse_init():
    w = ExampleWarehouse(4, 3)

    assert w._w == 4
    assert w._h == 3
    assert w._N == 12
    assert w.s.shape[0] == 12
    assert w.s.shape[1] == 12
    assert np.sum(w.s) == 0


def test_getitem():
    w = ExampleWarehouse(4, 3)
    w.generate()

    # TODO: more checks
    assert w[0, 0, 0, 1] == 1
    # false index
    assert w[-100, 100, 400, 400] == 0


def test_render():
    w = ExampleWarehouse(4, 3)
    w.generate()
    ax = w.render()
    # TODO: place some test here
    assert True


def test_random_warehouse():
    w = RandomWareHouse(10, 2)
    w.generate()
    s0 = w.s.copy()
    s0 = (s0 + s0.T) // 2
    assert np.all(s0 == w.s)
