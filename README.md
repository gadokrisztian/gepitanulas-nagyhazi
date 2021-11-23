# Gépitanulás házi feladat

[![tests](https://github.com/gkrisztian1/gepitanulas-nagyhazi/actions/workflows/ci.yml/badge.svg)](https://github.com/robust/actions)
[![codecov](https://codecov.io/gh/gkrisztian1/gepitanulas-nagyhazi/branch/main/graph/badge.svg?token=KMYGW7NHWH)](https://codecov.io/gh/gkrisztian1/gepitanulas-nagyhazi)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/gkrisztian1/gepitanulas-nagyhazi.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/gkrisztian1/gepitanulas-nagyhazi/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/gkrisztian1/gepitanulas-nagyhazi.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/gkrisztian1/gepitanulas-nagyhazi/context:python)

---

## Feladat leírása

## Példa a működésre

A raraktár:

![](media/example_warehouse.png)

Robot a `4`-es pozícióban van és a `10` helyre kell mennie felvenni az árut:
```python
>>> route = r.get_route(0, 10)
>>> [4, 0, 1, 5, 9, 10]
```

![](media/example_route.png)
