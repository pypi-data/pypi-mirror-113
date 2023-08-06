# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['img2cmd']
setup_kwargs = {
    'name': 'img2cmd',
    'version': '1.0.0',
    'description': 'Functions: drawimg(depth, image_path) | You must install "Color-It" and "Pillow" too',
    'long_description': None,
    'author': 'Mitikas',
    'author_email': 'mitikas333@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
