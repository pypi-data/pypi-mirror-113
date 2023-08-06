# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bilibili_dynamic']

package_data = \
{'': ['*'], 'bilibili_dynamic': ['element/*', 'typeface/*']}

install_requires = \
['Pillow>=8.0.1,<9.0.0',
 'aiohttp>=3.7.2,<4.0.0',
 'fonttools>=4.24.4,<5.0.0',
 'matplotlib>=3.4.0,<4.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'qrcode>=6.1,<7.0',
 'urllib3>=1.25.11,<2.0.0']

setup_kwargs = {
    'name': 'bilibili-dynamic',
    'version': '0.0.1',
    'description': '将哔哩哔哩返回的数据渲染为类似与B站APP官方的分享图片',
    'long_description': None,
    'author': 'NGWORKS',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
