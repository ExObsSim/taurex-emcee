.. _installation:

Installation
====================================

.. _install pip:

Install with pip
-------------------

The ``taurex-emcee`` package is hosted on PyPI repository. You can install it by

.. code-block:: console

    pip install taurex_emcee

.. _install git:

Install from git
-------------------
You can clone ``taurex-emcee`` from our main git repository

.. code-block:: console

    git clone https://github.com/ExObsSim/taurex-emcee.git

Move into the ``taurex-emcee`` folder

.. code-block:: console

    cd /your_path/taurex-emcee

Then, just do

.. code-block:: console

    pip install .

To test for correct setup you can do

.. code-block:: console

    python -c "import taurex_emcee"

You can verify if the plugin is functioning by seeing if TauREx successfully detects ``taurex-emcee``.

    taurex --plugins

If there are no errors then the installation was successful!

Uninstall ``taurex_emcee``
-------------------

``taurex_emcee`` is installed in your system as a standard python package:
you can uninstall it from your Environment as

.. code-block:: console

    pip uninstall taurex_emcee


Update ``taurex_emcee``
---------------

If you have installed ``taurex_emcee`` using Pip, now you can update the package simply as

.. code-block:: console

    pip install taurex_emcee --upgrade

If you have installed ``taurex_emcee`` from GitHub, you can download or pull a newer version of ``taurex_emcee`` over the old one, replacing all modified data.

Then you have to place yourself inside the installation directory with the console

.. code-block:: console

    cd /your_path/taurex_emcee

Now you can update ``taurex_emcee`` simply as

.. code-block:: console

    pip install . --upgrade

or simply

.. code-block:: console

    pip install .

Modify ``taurex_emcee``
---------------

You can modify ``taurex_emcee`` main code, editing as you prefer, but in order to make the changes effective

.. code-block:: console

    pip install . --upgrade

or simply

.. code-block:: console

    pip install .

To produce new ``taurex_emcee`` functionalities and contribute to the code, please see :ref:`Developer Guide`.