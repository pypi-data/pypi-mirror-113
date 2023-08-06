# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['divbrowse', 'divbrowse.lib']

package_data = \
{'': ['*'], 'divbrowse': ['static/*', 'static/build/*']}

install_requires = \
['bioblend>=0.15.0,<0.16.0',
 'click>=8.0.1,<9.0.0',
 'flask>=1.1.2,<2.0.0',
 'numpy>=1.18.1,<2.0.0',
 'pandas>=1.0.3,<2.0.0',
 'pyyaml>=5.1.2,<6.0.0',
 'scikit-allel>=1.2.1,<2.0.0',
 'scikit-learn>=0.22.1,<0.23.0',
 'tables>=3.6.1,<4.0.0',
 'waitress==2.0.0',
 'zarr>=2.4.0,<3.0.0']

entry_points = \
{'console_scripts': ['divbrowse = divbrowse.cli:main']}

setup_kwargs = {
    'name': 'divbrowse',
    'version': '0.1.0a4',
    'description': 'A web application for interactive exploration and analysis of very large SNP matrices',
    'long_description': None,
    'author': 'Patrick König',
    'author_email': 'koenig@ipk-gatersleben.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
