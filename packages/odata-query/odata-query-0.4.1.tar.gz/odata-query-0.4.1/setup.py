# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odata_query',
 'odata_query.django',
 'odata_query.sql',
 'odata_query.sqlalchemy']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.1,<3.0.0', 'sly>=0.4,<0.5']

extras_require = \
{'dev': ['bump2version>=1.0,<2.0'],
 'django': ['django>=2.2'],
 'docs': ['sphinx<4.0',
          'sphinx-rtd-theme>=0.5,<0.6',
          'myst-parser>=0.14,<0.15'],
 'linting': ['black==20.8b1',
             'flake8>=3.8,<4.0',
             'isort>=5.7,<6.0',
             'mypy>=0.800,<0.801',
             'vulture>=2.3,<3.0'],
 'sqlalchemy': ['sqlalchemy>=1.4,<2.0'],
 'testing': ['pytest>=6.2,<7.0', 'pytest-cov']}

setup_kwargs = {
    'name': 'odata-query',
    'version': '0.4.1',
    'description': 'An OData query parser and transpiler.',
    'long_description': '# OData-Query\n\n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=gorillaco_odata-query&metric=alert_status&token=cb35257e036d950788a0f628af7062929318482b)](https://sonarcloud.io/dashboard?id=gorillaco_odata-query)\n[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=gorillaco_odata-query&metric=coverage&token=cb35257e036d950788a0f628af7062929318482b)](https://sonarcloud.io/dashboard?id=gorillaco_odata-query)\n[![Documentation Status](https://readthedocs.org/projects/odata-query/badge/?version=latest)](https://odata-query.readthedocs.io/en/latest/?badge=latest)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n`odata-query` is a library that parses [OData v4](https://www.odata.org/) filter strings, and can convert\nthem to other forms such as\n[Django Queries](https://docs.djangoproject.com/en/3.2/topics/db/queries/),\n[SQLAlchemy Queries](https://docs.sqlalchemy.org/en/14/orm/loading_objects.html),\nor just plain SQL.\n\n\n## Installation\n\n`odata-query` is available on pypi, so can be installed with the package manager\nof your choice:\n\n```bash\npip install odata-query\n# OR\npoetry add odata-query\n# OR\npipenv install odata-query\n```\n\nThe package defines the following optional `extra`s:\n\n- `django`: If you want to pin a compatible Django version.\n- `sqlalchemy`: If you want to pin a compatible SQLAlchemy version.\n\n\nThe following `extra`s relate to the development of this library:\n\n- `linting`: The linting and code style tools.\n- `testing`: Packages for running the tests.\n- `docs`: For building the project documentation.\n\n\nYou can install `extra`s by adding them between square brackets during\ninstallation:\n\n```bash\npip install odata-query[sqlalchemy]\n```\n\n## Quickstart\n\nThe most common use case is probably parsing an OData query string, and applying\nit to a query your ORM understands. For this purpose there is an all-in-one function:\n`apply_odata_query`.\n\nExample for Django:\n\n```python\nfrom odata_query.django import apply_odata_query\n\norm_query = MyModel.objects  # This can be a Manager or a QuerySet.\nodata_query = "name eq \'test\'"  # This will usually come from a query string parameter.\n\nquery = apply_odata_query(orm_query, odata_query)\nresults = query.all()\n```\n\n\nExample for SQLAlchemy:\n\n```python\nfrom odata_query.sqlalchemy import apply_odata_query\n\norm_query = select(MyModel)  # This is any form of Query or Selectable.\nodata_query = "name eq \'test\'"  # This will usually come from a query string parameter.\n\nquery = apply_odata_query(orm_query, odata_query)\nresults = session.execute(query).scalars().all()\n```\n\n<!--- splitinclude-1 -->\n\n## Advanced Usage\n\nNot all use cases are as simple as that. Luckily, `odata-query` is very modular\nand extensible. See the [Documentation](https://odata-query.readthedocs.io/en/latest)\nfor advanced usage or extending the library for other cases.\n\n<!--- splitinclude-2 -->\n\n## Contact\n\nGot any questions or ideas? We\'d love to hear from you. Check out our\n[contributing guidelines](CONTRIBUTING.md) for ways to offer feedback and\ncontribute.\n\n\n## License\n\nCopyright (c) [Gorillini NV](https://gorilla.co/).\nAll rights reserved.\n\nLicensed under the [MIT](LICENSE) License.\n',
    'author': 'Oliver Hofkens',
    'author_email': 'oliver@gorilla.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
