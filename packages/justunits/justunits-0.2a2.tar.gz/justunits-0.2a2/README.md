# Just SI Units 
[![Coverage Status](https://coveralls.io/repos/gitlab/david.scheliga/justunits/badge.svg?branch=release)](https://coveralls.io/gitlab/david.scheliga/justunits?branch=release)
[![Build Status](https://travis-ci.com/david.scheliga/justunits.svg?branch=release)](https://travis-ci.com/david.scheliga/justunits)
[![PyPi](https://img.shields.io/pypi/v/justunits.svg?style=flat-square&label=PyPI)](https://https://pypi.org/project/justunits/)
[![Python Versions](https://img.shields.io/pypi/pyversions/justunits.svg?style=flat-square&label=PyPI)](https://https://pypi.org/project/justunits/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Documentation Status](https://readthedocs.org/projects/justunits/badge/?version=latest)](https://justunits.readthedocs.io/en/latest/?badge=latest)


**justunits** handles (SI-) units within string occurrences. The module's *justunits*
tasks are limited to the interchangeability of different unit formatting styles.
This module focus **just** on **units**, it does not provide unit conversion or
anything related to such a topic. It's purpose is to provide an entry point for a
future unit conversion within another module.

![justunits-icon](https://arithmeticmeancurve.readthedocs.io/en/latest/_images/justunits-icon.svg)

## Installation

```` shell script
    $ pip install justunits
````

If available the latest development state can be installed from gitlab.

```` shell script
    $ pip install git+https://https://gitlab.com/david.scheliga/justunits.git@dev
````

## Alpha Development Status

The current development state of this project is *alpha*. It's published for a first
stress test of 2 major functions.

Towards the beta
- naming of modules, classes and methods will change, since the final wording is not
  done.
- Code inspections are not finished.
- The documentation is broad or incomplete.
- Testing is not complete, as it is added during the first test phase. At this
  state mostly doctests are applied at class or function level.


## Basic Usage

[Read-the-docs](https://justunits.readthedocs.io/en/latest/index.html) for a more detailed documentation.

## Contribution

Any contribution by reporting a bug or desired changes are welcomed. The preferred 
way is to create an issue on the gitlab's project page, to keep track of everything 
regarding this project.

### Contribution of Source Code
#### Code style
This project follows the recommendations of [PEP8](https://www.python.org/dev/peps/pep-0008/).
The project is using [black](https://github.com/psf/black) as the code formatter.

#### Workflow

1. Fork the project on Gitlab.
2. Commit changes to your own branch.
3. Submit a **pull request** from your fork's branch to our branch *'dev'*.

## Authors

* **David Scheliga** 
    [@gitlab](https://gitlab.com/david.scheliga)
    [@Linkedin](https://www.linkedin.com/in/david-scheliga-576984171/)
    - Initial work
    - Maintainer

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the
[LICENSE](LICENSE) file for details

## Acknowledge

[Code style: black](https://github.com/psf/black)
