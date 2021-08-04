============
Contributing
============

This package is under early stages of development it’s open to any
constructive suggestions. Please send bug reports and feature requests
through issue trackers and pull requests.

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at `issues <https://github.com/Vignesh-Desmond/attractors/issues>`_

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it. Those that are
tagged with "first-timers-only" is suitable for those getting started in open-source software.

Write Documentation
~~~~~~~~~~~~~~~~~~~

`attractors` could always use more documentation. `sphinx` is used to build docs.

Feedbacks
~~~~~~~~~~~~~~~

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* This is a solo project so contributions are always welcome :)

Get Started
-----------

Ready to contribute? Here's how to set up `attractors` for local development.

1. Fork the `attractors` repo on GitHub.
2. Clone your fork locally:

.. code:: shell

    $ git clone git@github.com:your_name_here/attractors.git

3. Poetry is recommended for development setup. Install poetry from
`here <https://python-poetry.org/docs/#installation>`_


.. code-block:: shell

    $ cd attractors/
    $ poetry install

4. Create a branch for local development:

.. code:: shell

    $ git checkout -b name-of-your-bugfix-or-feature

Now you can make your changes locally.

5. When you're done making changes, check that your changes pass the tests:

.. code-block:: shell

    $ poetry run flake8 attractors tests
    $ poetry run black attractors tests
    $ poetry run isort attractors tests

Use of pre-commit hooks is recommended.

6. Commit your changes and push your branch to GitHub:

.. code-block:: shell

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

In brief, commit messages should follow these conventions:

* Always contain a subject line which briefly describes the changes made. For example "Update CONTRIBUTING.rst".
* The commit body should contain context about the change - how the code worked before, how it works now and why you decided to solve the issue in the way you did.

More detail on commit guidelines can be found at https://chris.beams.io/posts/git-commit

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests and does not affect coverage.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring.
3. The pull request should work for Python ^3.7, and above. Wait for Github Actions CI to
   run some and check if they pass.
