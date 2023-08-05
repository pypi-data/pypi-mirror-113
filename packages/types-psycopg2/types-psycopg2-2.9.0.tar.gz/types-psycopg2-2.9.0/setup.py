from setuptools import setup

name = "types-psycopg2"
description = "Typing stubs for psycopg2"
long_description = '''
## Typing stubs for psycopg2

This is a PEP 561 type stub package for the `psycopg2` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `psycopg2`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/psycopg2. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `a0f199727b68917a80939432e1e69315afc44608`.
'''.lstrip()

setup(name=name,
      version="2.9.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['psycopg2-stubs'],
      package_data={'psycopg2-stubs': ['tz.pyi', '_psycopg.pyi', 'sql.pyi', '_range.pyi', 'errorcodes.pyi', 'errors.pyi', '_json.pyi', '_ipaddress.pyi', '__init__.pyi', 'extensions.pyi', 'pool.pyi', 'extras.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
