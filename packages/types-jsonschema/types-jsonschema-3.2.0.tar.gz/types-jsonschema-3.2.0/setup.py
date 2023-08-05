from setuptools import setup

name = "types-jsonschema"
description = "Typing stubs for jsonschema"
long_description = '''
## Typing stubs for jsonschema

This is a PEP 561 type stub package for the `jsonschema` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `jsonschema`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/jsonschema. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `a0f199727b68917a80939432e1e69315afc44608`.
'''.lstrip()

setup(name=name,
      version="3.2.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['jsonschema-stubs'],
      package_data={'jsonschema-stubs': ['_utils.pyi', 'exceptions.pyi', '_validators.pyi', '_reflect.pyi', '_types.pyi', 'cli.pyi', '_format.pyi', 'validators.pyi', 'compat.pyi', '_legacy_validators.pyi', '__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
