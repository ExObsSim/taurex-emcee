.. _mpi:

==============
Using with MPI
==============

``taurex-emcee`` can be used with MPI to perform retrievals using multiple CPU or GPU cores.
The latter assumes you have a CUDA enabled GPU and have installed the taurex_cuda_ package.

To use ``taurex-emcee`` with MPI, you need to install the ``mpi4py`` package. This can be done using ``pip``::

    pip install mpi4py

Once installed, you can run ``taurex-emcee`` using MPI by using the ``mpirun`` command::

    mpirun -n 4 taurex -i parfile.par -R -o retrieval.h5

where the ``-n`` flag specifies the number of cores to use.

If interested, you can also use multiple GPUs. Please refer to taurex_cuda_ for more information.

.. _taurex_cuda: https://taurex-cuda-public.readthedocs.io/en/latest/index.html