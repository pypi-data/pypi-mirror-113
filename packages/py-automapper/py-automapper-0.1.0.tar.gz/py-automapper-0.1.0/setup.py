# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['automapper', 'automapper.extensions']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'py-automapper',
    'version': '0.1.0',
    'description': 'Library for automatically mapping one object to another',
    'long_description': '# py-automapper\nPython object auto mapper\n\nCurrent mapper can be useful for multilayer architecture which requires constant mapping between objects from separate layers (data layer, presentation layer, etc).\n\nFor more information read the [documentation](https://anikolaienko.github.io/py-automapper).\n\n## Usage example:\n```python\nfrom automapper import mapper\n\n# Add automatic mappings\nmapper.add(SourceClass, TargetClass)\n\n# Map object of SourceClass to output object of TargetClass\nmapper.map(obj)\n\n# Map object to AnotherTargetClass not added to mapping collection\nmapper.to(AnotherTargetClass).map(obj)\n\n# Override specific fields or provide missing ones\nmapper.map(obj, field1=value1, field2=value2)\n\n# Don\'t map None values to target object\nmapper.map(obj, skip_none_values = True)\n```\n\n## Advanced features\n```python\nfrom automapper import Mapper\n\n# Create your own Mapper object without any predefined extensions\nmapper = Mapper()\n\n# Add your own extension for extracting list of fields from class\n# for all classes inherited from base class\nmapper.add_spec(\n    BaseClass,\n    lambda child_class: child_class.get_fields_function()\n)\n\n# Add your own extension for extracting list of fields from class\n# for all classes that can be identified in verification function\nmapper.add_spec(\n    lambda cls: hasattr(cls, "get_fields_function"),\n    lambda cls: cls.get_fields_function()\n)\n```\nFor more information about extensions check out existing extensions in `automapper/extensions` folder\n\n## Not yet implemented features\n```python\n\n# TODO: multiple from classes\nmapper.add(FromClassA, FromClassB, ToClassC)\n\n# TODO: add custom mappings for fields\nmapper.add(ClassA, ClassB, {"Afield1": "Bfield1", "Afield2": "Bfield2"})\n\n# TODO: Advanced: map multiple objects to output type\nmapper.multimap(obj1, obj2)\nmapper.to(TargetType).multimap(obj1, obj2)\n```\n',
    'author': 'Andrii Nikolaienko',
    'author_email': 'anikolaienko14@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/anikolaienko/py-automapper',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
