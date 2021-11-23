import numpy as np
import pytest

from whouserobot import ExampleWarehouse, WareHouseBase


@pytest.fixture
def w():
    w = ExampleWarehouse()
    w.generate()
    return w


def equaliterable(it1, it2):
    return all(it1_i == it2_i for it1_i, it2_i in zip(it1, it2))


def test_warehouse_init(w):

    assert w._w == 4
    assert w._h == 3
    assert w._N == 12
    assert len(w.s) == 12
    assert len(w.s[0]) == 12


def test_coord2state(w):
    assert w.coord2state(0, 0) == 0
    assert w.coord2state(1, 0) == 1
    assert w.coord2state(2, 0) == 2
    assert w.coord2state(3, 0) == 3

    assert w.coord2state(0, 1) == 4
    assert w.coord2state(1, 1) == 5
    assert w.coord2state(2, 1) == 6
    assert w.coord2state(3, 1) == 7

    assert w.coord2state(0, 2) == 8
    assert w.coord2state(1, 2) == 9
    assert w.coord2state(2, 2) == 10
    assert w.coord2state(3, 2) == 11


def test_state2coord(w):

    assert equaliterable(w.state2coord(0), (0, 0))
    assert equaliterable(w.state2coord(1), (1, 0))
    assert equaliterable(w.state2coord(2), (2, 0))
    assert equaliterable(w.state2coord(3), (3, 0))

    assert equaliterable(w.state2coord(4), (0, 1))
    assert equaliterable(w.state2coord(5), (1, 1))
    assert equaliterable(w.state2coord(6), (2, 1))
    assert equaliterable(w.state2coord(7), (3, 1))

    assert equaliterable(w.state2coord(8), (0, 2))
    assert equaliterable(w.state2coord(9), (1, 2))
    assert equaliterable(w.state2coord(10), (2, 2))
    assert equaliterable(w.state2coord(11), (3, 2))


def test_render(w):
    w.generate()
    ax = w.render()
    # TODO: place some test here
    assert True
