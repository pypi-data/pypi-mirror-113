# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['binding']

package_data = \
{'': ['*']}

install_requires = \
['executing>=0.6.0,<0.7.0', 'forbiddenfruit>=0.1.4,<0.2.0']

setup_kwargs = {
    'name': 'binding',
    'version': '0.3.1',
    'description': 'Bindable properties for Python',
    'long_description': "# Binding\n\nThis package brings property binding to Python.\nIt allows you to bind attributes of one object to other attributes of itself or other objects like so:\n\n```Python\nlabel.text.bind(model.value)\n```\n\nThat means, whenever `model.value` is changed, `label.text` changes as well.\n\n# Installation\n\nThis package can be installed using the Python package installer [pip](https://pypi.org/project/pip/):\n\n```bash\npython3 -m pip install binding\n```\n\nAlternatively you can find the [source code](https://github.com/zauberzeug/binding) on GitHub.\n\n# Usage\n\nYou can apply binding in two different ways: automatic updates using bindable properties or by calling an update functional explicitely.\nFurthermore, you can specify the binding direction as well as converter functions.\n\nThe following examples give a more detailed explanation.\nThe code snippets build upon each other and are meant to be called in succession.\n\n## Bindable properties\n\nIf you have control over the class implementation, you can introduce a `BindableProperty` for the respective attributes. It will intercept each write access the attribute and propagate the changed value to bound properties:\n\n```python\nfrom binding import BindableProperty\n\nclass Person:\n\n    name = BindableProperty()\n\n    def __init__(self, name=None):\n\n        self.name = name\n\nclass Car:\n\n    driver = BindableProperty()\n\n    def __init__(self, driver=None):\n\n        self.driver = driver\n\nperson = Person('Robert')\ncar = Car()\ncar.driver.bind(person.name)\nassert car.driver == person.name == 'Robert'\n\nperson.name = 'Bob'\nassert car.driver == person.name == 'Bob'\n```\n\n## Binding with non-bindable attributes\n\nSuppose you have a class which you cannot or don't want to change.\nThat means it has no `BindableProperty` to observe value changes.\nYou can bind its attributes nevertheless:\n\n```python\nclass License:\n\n    def __init__(self, name=None):\n\n        self.name = name\n\nlicense = License()\nlicense.name.bind(person.name)\nperson.name = 'Todd'\nassert license.name == person.name == 'Todd'\n```\n\nBut if the license name is changed, there is no `BindableProperty` to notice write access to its value.\nWe have to manually trigger the propagation to bound objects.\n\n```python\nfrom binding import update\n\nlicense.name = 'Ben'\nassert person.name != license.name == 'Ben'\n\nupdate()\nassert person.name == license.name == 'Ben'\n```\n\n## One-way binding\n\nThe `.bind()` method registers two-way binding.\nBut you can also specify one-way binding using `.bind_from()` or `.bind_to()`, respectively.\nIn the following example `car` receives updates `person`, but not the other way around.\n\n```python\nperson = Person('Ken')\ncar = Car()\n\ncar.driver.bind_from(person.name)\nassert car.driver == person.name == 'Ken'\n\nperson.name = 'Sam'\nassert car.driver == person.name == 'Sam'\n\ncar.driver = 'Seth'\nassert car.driver != person.name == 'Sam'\n```\n\nLikewise you can specify forward binding to let `person` be updated when `car` changes:\n\n```python\nperson = Person('Keith')\ncar = Car()\n\ncar.driver.bind_to(person.name)\nassert car.driver == person.name == None\n\ncar.driver = 'Kent'\nassert car.driver == person.name == 'Kent'\n\nperson.name = 'Grant'\nassert car.driver != person.name == 'Grant'\n```\n\n## Converters\n\nFor all types of binding - forward, backward, two-way, via bindable properties or non-bindable attributes - you can define converter functions that translate values from one side to another.\nThe following example demonstrates the conversion between Celsius and Fahrenheit.\n\n```python\nclass Temperature:\n\n    c = BindableProperty()\n    f = BindableProperty()\n\n    def __init__(self):\n\n        self.c = 0.0\n        self.f = 0.0\n\nt = Temperature()\nt.f.bind(t.c, forward=lambda f: (f - 32) / 1.8, backward=lambda c: c * 1.8 + 32)\nassert t.c == 0.0 and t.f == 32.0\n\nt.f = 68.0\nassert t.c == 20.0 and t.f == 68.0\n\nt.c = 100.0\nassert t.c == 100.0 and t.f == 212.0\n```\n\nNote that `bind_to()` only needs a `forward` converter.\nSimilarly `bind_from` has only a `backward` converter.\n\n# Implementation and dependencies\n\nTo achieve such a lean API we utilize three main techniques:\n\n- For extending basic types with `bind()`, `bind_to()` and `bind_from()` methods we use `curse` from the [forbiddenfruit](https://pypi.org/project/forbiddenfruit/) package.\n\n- For intercepting write access to attributes we implement `BindableProperties` as [descriptors](https://docs.python.org/3/howto/descriptor.html).\n\n- For finding the object and attribute name of the caller and the argument of our `bind()` methods we use inspection tools from the [inspect](https://docs.python.org/3/library/inspect.html) and [executing](https://pypi.org/project/executing/) packages.\n",
    'author': 'Zauberzeug GmbH',
    'author_email': 'info@zauberzeug.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zauberzeug/binding',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
