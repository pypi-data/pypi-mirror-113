from setuptools import setup

name = "types-psutil"
description = "Typing stubs for psutil"
long_description = '''
## Typing stubs for psutil

This is a PEP 561 type stub package for the `psutil` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `psutil`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/psutil. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `2a4cc033079cf0a1ebf7b323016a01aadb36c5e8`.
'''.lstrip()

setup(name=name,
      version="5.8.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['psutil-stubs'],
      package_data={'psutil-stubs': ['_psutil_linux.pyi', '_psutil_windows.pyi', '_psosx.pyi', '_common.pyi', '_psbsd.pyi', '_pswindows.pyi', '__init__.pyi', '_pslinux.pyi', '_compat.pyi', '_psutil_posix.pyi', '_psposix.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
