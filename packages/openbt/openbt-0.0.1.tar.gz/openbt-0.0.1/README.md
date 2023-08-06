# Openbt

This package was designed to replicate (almost) all the behavior of the OpenBT project (https://bitbucket.org/mpratola/openbt/wiki/Home). 

OpenBT is a flexible and extensible C++ framework for implementing Bayesian regression tree models. Currently a number of models and inference tools are available for use in the released code with additional models/tools under development. The code makes use of MPI for parallel computing. Currently an R interface is provided via the ROpenbt package to demonstrate use of the software, and this package provides Python functionality.

How to utilize this package:
1. Install the package by typing: python3 -m pip install openbt==[version number you want].
2. In Python (i.e. scripts), to import the package, type: from openbt import openbt. This gives Python access to the main openbt.py class file
3. To utilize the OPENBT class/functions in Python 3 to conduct and interpret fits: create a fit object such as m = openbt.OPENBT() (instance of the class).
4. I attempted to upload example scripts, showing the usage of the OPENBT class on data, to this package. However, if these are difficult to access, you can also simply view them at the github "Homepage": https://github.com/cavan33/openbt_py .

Package Home: https://pypi.org/project/openbt/ .

Note: The old way to use the class was to type from openbt import OPENBT, but that assumed that you had the openbt.py class-creation file in your working directory.
