from setuptools import setup

name = "types-jmespath"
description = "Typing stubs for jmespath"
long_description = '''
## Typing stubs for jmespath

This is a PEP 561 type stub package for the `jmespath` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `jmespath`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/jmespath. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `2a4cc033079cf0a1ebf7b323016a01aadb36c5e8`.
'''.lstrip()

setup(name=name,
      version="0.10.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['jmespath-stubs'],
      package_data={'jmespath-stubs': ['parser.pyi', 'exceptions.pyi', 'lexer.pyi', 'visitor.pyi', 'functions.pyi', 'ast.pyi', '__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
