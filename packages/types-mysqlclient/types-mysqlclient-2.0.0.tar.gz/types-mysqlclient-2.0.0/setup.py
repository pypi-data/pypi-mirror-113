from setuptools import setup

name = "types-mysqlclient"
description = "Typing stubs for mysqlclient"
long_description = '''
## Typing stubs for mysqlclient

This is a PEP 561 type stub package for the `mysqlclient` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `mysqlclient`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/mysqlclient. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `2d3bde439eaccb5b5205e25ae9186392a9bb59f5`.
'''.lstrip()

setup(name=name,
      version="2.0.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['MySQLdb-stubs'],
      package_data={'MySQLdb-stubs': ['connections.pyi', 'release.pyi', 'converters.pyi', 'times.pyi', 'cursors.pyi', '_mysql.pyi', '_exceptions.pyi', '__init__.pyi', 'constants/CR.pyi', 'constants/FIELD_TYPE.pyi', 'constants/FLAG.pyi', 'constants/CLIENT.pyi', 'constants/__init__.pyi', 'constants/ER.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
