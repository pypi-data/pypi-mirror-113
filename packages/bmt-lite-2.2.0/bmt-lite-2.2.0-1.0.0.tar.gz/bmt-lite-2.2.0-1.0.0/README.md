# Reasoner Utilities

[![pypi](https://github.com/NCATSTranslator/reasoner-validator/workflows/pypi/badge.svg)](https://pypi.org/project/reasoner-validator/)
[![readthedocs](https://readthedocs.org/projects/reasoner-validator/badge/)](https://reasoner-validator.readthedocs.io/)

See the [documentation](https://reasoner-validator.readthedocs.io/) and/or [contributor guidelines](https://github.com/NCATSTranslator/reasoner-validator/blob/master/.github/CONTRIBUTING.md).

### Building

```bash
pip install -rrequirements-build.txt -rrequirements-test.txt
python setup.py sdist bdist_wheel --v1.8.2
tox
```

To build the documentation:

```bash
cd docs
make html
```
