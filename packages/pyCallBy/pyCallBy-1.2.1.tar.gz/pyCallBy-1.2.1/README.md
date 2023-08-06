[![Sourcecode on GitHub](https://img.shields.io/badge/Paebbels-pyCallBy-323131.svg?logo=github&longCache=true)](https://github.com/Paebbels/pyCallBy)
[![Sourcecode License](https://img.shields.io/pypi/l/pyCallBy?logo=GitHub&label=code%20license)](LICENSE.md)
[![GitHub tag (latest SemVer incl. pre-release)](https://img.shields.io/github/v/tag/Paebbels/pyCallBy?logo=GitHub&include_prereleases)](https://github.com/Paebbels/pyCallBy/tags)
[![GitHub release (latest SemVer incl. including pre-releases)](https://img.shields.io/github/v/release/Paebbels/pyCallBy?logo=GitHub&include_prereleases)](https://github.com/Paebbels/pyCallBy/releases/latest)
[![GitHub release date](https://img.shields.io/github/release-date/Paebbels/pyCallBy?logo=GitHub)](https://github.com/Paebbels/pyCallBy/releases)
[![Dependents (via libraries.io)](https://img.shields.io/librariesio/dependents/pypi/pyCallBy?logo=librariesdotio)](https://github.com/Paebbels/pyCallBy/network/dependents)  
[![GitHub Workflow - Build and Test Status](https://img.shields.io/github/workflow/status/Paebbels/pyCallBy/Unit%20Testing,%20Coverage%20Collection,%20Package,%20Release,%20Documentation%20and%20Publish?label=Pipeline&logo=GitHub%20Actions&logoColor=FFFFFF)](https://github.com/Paebbels/pyCallBy/actions/workflows/Pipeline.yml)
[![Codacy - Quality](https://img.shields.io/codacy/grade/a738753f1b94494b9fa133584e70889c?logo=Codacy)](https://www.codacy.com/manual/Paebbels/pyCallBy)
[![Codacy - Coverage](https://img.shields.io/codacy/coverage/a738753f1b94494b9fa133584e70889c?logo=Codacy)](https://www.codacy.com/manual/Paebbels/pyCallBy)
[![Codecov - Branch Coverage](https://img.shields.io/codecov/c/github/Paebbels/pyCallBy?logo=Codecov)](https://codecov.io/gh/Paebbels/pyCallBy)
[![Libraries.io SourceRank](https://img.shields.io/librariesio/sourcerank/pypi/pyCallBy?logo=librariesdotio)](https://libraries.io/github/Paebbels/pyCallBy/sourcerank)  
[![PyPI](https://img.shields.io/pypi/v/pyCallBy?logo=PyPI&logoColor=FBE072)](https://pypi.org/project/pyCallBy/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyCallBy?logo=PyPI&logoColor=FBE072)
![PyPI - Status](https://img.shields.io/pypi/status/pyCallBy?logo=PyPI&logoColor=FBE072)
[![Libraries.io status for latest release](https://img.shields.io/librariesio/release/pypi/pyCallBy?logo=librariesdotio)](https://libraries.io/github/Paebbels/pyCallBy)
[![Requires.io](https://img.shields.io/requires/github/Paebbels/pyCallBy)](https://requires.io/github/Paebbels/pyCallBy/requirements/?branch=main)  
[![Read the Docs](https://img.shields.io/readthedocs/pycallby?label=ReadTheDocs&logo=readthedocs)](https://pyCallBy.readthedocs.io/)
[![Documentation License](https://img.shields.io/badge/doc%20license-CC--BY%204.0-green?logo=readthedocs)](LICENSE.md)
[![Documentation - Read Now!](https://img.shields.io/badge/doc-read%20now%20%E2%9E%94-blueviolet?logo=readthedocs)](https://pyCallBy.readthedocs.io/)


# pyCallBy

Auxilary classes to implement call by reference.

Python does not allow a user to distinguish between *call-by-value* and *call-by-reference*
parameter passing. Python's standard types are passed by-value to a function or
method. Instances of a class are passed by-reference (pointer) to a function or
method.

By implementing a wrapper-class `CallByRefParam`, any types value can be
passed by-reference. In addition, standard types like `int` or `bool`
can be handled by derived wrapper-classes.


## Example

```Python
# define a call-by-reference parameter for integer values
myInt = CallByRefIntParam()

# a function using a call-by-reference parameter
def func(param : CallByRefIntParam):
  param <<= 3

# call the function and pass the wrapper object
func(myInt)

print(myInt.value)
```


## Contributors

* [Patrick Lehmann](https://github.com/Paebbels) (Maintainer)
* [and more...](https://github.com/paebbels/pyCallBy/graphs/contributors)


## License

This Python package (source code) licensed under [Apache License 2.0](LICENSE.md).  
The accompanying documentation is licensed under [Creative Commons - Attribution 4.0 (CC-BY 4.0)](doc/Doc-License.rst).


-------------------------

SPDX-License-Identifier: Apache-2.0
