from setuptools import setup

name = "types-pyOpenSSL"
description = "Typing stubs for pyOpenSSL"
long_description = '''
## Typing stubs for pyOpenSSL

This is a PEP 561 type stub package for the `pyOpenSSL` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `pyOpenSSL`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/pyOpenSSL. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `0baeef09a2c872951341d69055408671897da9e2`.
'''.lstrip()

setup(name=name,
      version="20.0.4",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=['types-cryptography'],
      packages=['OpenSSL-stubs'],
      package_data={'OpenSSL-stubs': ['crypto.pyi', '__init__.pyi', 'SSL.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
