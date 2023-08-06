=========
CompNeuro
=========

|Lint| |Test| |Publish| |PyPI| |Coverage|

.. |Lint| image:: https://github.com/TK-21st/CompNeuro/actions/workflows/Lint.yml/badge.svg
        :target: https://github.com/TK-21st/CompNeuro/actions/workflows/Lint.yml

.. |Test| image:: https://github.com/TK-21st/CompNeuro/actions/workflows/Test.yml/badge.svg
        :target: https://github.com/TK-21st/CompNeuro/actions/workflows/Test.yml

.. |Publish| image:: https://github.com/TK-21st/CompNeuro/actions/workflows/python-publish.yml/badge.svg
        :target: https://github.com/TK-21st/CompNeuro/actions/workflows/python-publish.yml

.. |PyPI| image:: https://img.shields.io/pypi/v/compneuro.svg
        :target: https://pypi.python.org/pypi/compneuro

.. |Coverage| image:: /coverage.svg
        :alt: PyTest Coverage

.. .. image:: https://readthedocs.org/projects/compneuro/badge/?version=latest
..         :target: https://compneuro.readthedocs.io/en/latest/?version=latest
..         :alt: Documentation Status


This Module provides source code for Book Chapters and Notebooks for 4020.


* Free software: BSD-3 license


Features
--------

* Utility functions for signal generation, spectral analysis, spike plotting, and other plotting functionalities
* CPU-based simulation and analysis of dynamical system models
* Interactive plotting of results using Bokeh.


Installation
------------

To install the lastest version on PyPI, run the following code:

.. code::

        pip install compneuro

This will install all the necessary requirements as specified in the `setup.py` file.
However, you will
need to install NodeJS with version greater than :code:`14.0` to make sure that the
custom `Bokeh` 3d plotting capability renders correctly in Jupyter. For installing
NodeJS_, you should follow instructions on their official website.

For development, see below.

Development
-----------
Make sure you install NodeJS_ first. Afterwards, you can install the package
including the requirements by executing::

        pip install -e .[dev]

If you want to work on distributing the package, you will need to install a few
additional packages, which can be done by running::

        pip install -e .[dist]

Before committing, use black_ to format the python code by running

.. code::

        black compneuro

For each utility function added, make sure you add a test function in the
`compneuro/tests` folder. All tests should be written using pytest_.

You can also run all tests by running:

.. code::

        py.test

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`black`: https://github.com/psf/black
.. _`pytest`: https://docs.pytest.org/
.. _`NodeJS`: https://nodejs.org/en/