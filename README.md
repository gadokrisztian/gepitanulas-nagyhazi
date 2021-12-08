# Gépitanulás házi feladat

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
---

## Feladat leírása

## Példa a működésre

A raraktár:

![](media/example_warehouse.png)

Robot a `4`-es pozícióban van és a `10` helyre kell mennie felvenni az árut:
```python
>>> r = QLRobot(ExampleWarehouse())
>>> route = r.get_route(4, 10)
>>> [4, 0, 1, 5, 9, 10]
```

![](media/example_route.png)

```python
>>> route = r.get_route(10, 11)
>>> [10, 6, 7, 11]
```

![](media/example_route2.png)


```python
>>> route = r.get_route(3, 8)
>>> [10, 6, 7, 11]
```

![](media/example_route3.png)

## Generált raktár

```python
>>> w = RandomWarehouse(10, 5, seed=65, walls=25)
>>> r = QLRobot(w, niter=10_000)
>>> route = r.get_route(3, 38)
>>> [3, 2, 12, 22, 32, 33, 34, 35, 36, 37, 47, 48, 49, 39, 38]
```

![](media/example_route4.png)

```python
>>> w = RandomWarehouse(10, 10, seed=65, walls=50)
>>> r = QLRobot(w, niter=10_000)
>>> route = r.get_route(9, 72)
>>> [3, 2, 12, 22, 32, 33, 34, 35, 36, 37, 47, 48, 49, 39, 38]
```

![](media/example_route5.png)
