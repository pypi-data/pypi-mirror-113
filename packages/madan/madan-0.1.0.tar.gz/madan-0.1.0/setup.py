# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['madan', 'madan.cv']

package_data = \
{'': ['*'], 'madan': ['math/*', 'ml/*', 'nlp/*']}

install_requires = \
['streamlit>=0.84.2,<0.85.0']

setup_kwargs = {
    'name': 'madan',
    'version': '0.1.0',
    'description': 'Open source ai library',
    'long_description': '\n# madan\n--------\n![PyPI](https://img.shields.io/pypi/v/madan)\n\nMadan is an end-to-end open source platform for math,machine learning,Computer Vision, and Natural Language Processing. It has a comprehensive, flexible ecosystem of tools, libraries, and community resources that lets researchers push the state-of-the-art in AI and developers easily build and deploy AI-powered applications.\n\n<!-- Example  : One function that computes the object detection, depth of the object, face recognition, and object tracking.\n<img src="/madanlibrarydemo.gif" alt="GitHub badge" /> -->\n\n\n# Table of content\n## 1. [Math](https://github.com/MadanBaduwal/ai_library/tree/master/madan/math)\n## 2. [Machine learning](https://github.com/MadanBaduwal/ai_library/tree/master/madan/ml)\n## 3. [Computer Vision](https://github.com/MadanBaduwal/ai_library/tree/master/madan/cv)\n## 5. [Natural Language Processing](https://github.com/MadanBaduwal/ai_library/tree/master/madan/nlp)\n-------\n## Install\n\nTo install the current release\n```shell\n$ pip install madan\n```\n<img src="/madaninstalldemo.gif" alt="GitHub badge" />\n\nTo update madan to the latest version, add --upgrade flag to the above commands.\n\n\n\n\n\n',
    'author': 'MadanBaduwal',
    'author_email': 'madanbaduwal100@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MadanBaduwal/madan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
