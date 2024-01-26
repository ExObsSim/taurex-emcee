.. _introduction:

Introduction
===============

`taurex-emcee` is a plugin for the TauREx3.1_ atmospheric retrieval framework that extends the choice of sampling methods available to the user. The plugin provides an interface to the emcee_ sampler, a popular affine-invariant ensemble sampler widely used in the astronomy community. Running the sampler to convergence is automated through the autoemcee_ package, which also supports MPI parallelization. Thus, the `taurex-emcee` plugin allows users to easily launch parallelized retrievals of atmospheric spectra with `emcee`. This enables reliable, efficient, and fast retrievals.

.. _TauREx3.1: https://taurex3-public.readthedocs.io/en/latest/
.. _emcee: https://emcee.readthedocs.io/en/stable/
.. _autoemcee: https://github.com/JohannesBuchner/autoemcee