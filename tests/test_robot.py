from whouserobot import ExampleWarehouse, QLRobot


def test_routing():
    r = QLRobot(ExampleWarehouse())
    route = r.get_route(4, 10)
    assert all(ri == rj for ri, rj in zip(route, [4, 0, 1, 5, 9, 10]))


def test_render_route():
    # It's enough if the render method does not raise any exception
    r = QLRobot(ExampleWarehouse())
    route = r.get_route(4, 10)
    ax = r.render_route(route)
