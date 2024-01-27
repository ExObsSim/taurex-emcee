.. _overview:

========
Overview
========

The ``taurex-emcee`` plugin enables the use of the ``emcee`` sampler in TauREx3.1 retrievals.

To make use of the plugin, you can simply your existing optimizer with the ``emcee`` sampler.

For example if we have a multinest optimizer defined as::

    [Optimizer]
    optimizer = multinest
    multi_nest_path = ./multinest

The ``taurex-emcee`` enabled version is simply::

    [Optimizer]
    optimizer = emcee

The ``emcee`` sampler has a number of parameters that can be set. These are described in the table below.

+-------------------------+----------------------------------------------------+--------------------+
| Name                    | Description                                        | Default            | 
+=========================+====================================================+====================+
| num_global_samples      | Number of samples to initially draw from the prior | 10000              |
+-------------------------+----------------------------------------------------+--------------------+
| num_chains              | Number of independent ensembles to run             | 4                  |
+-------------------------+----------------------------------------------------+--------------------+
| num_walkers             | Ensemble size                                      | max(100, 4 * ndim) |
+-------------------------+----------------------------------------------------+--------------------+
| max_ncalls              | Maximum number of likelihood function evaluations  | 1000000            |
+-------------------------+----------------------------------------------------+--------------------+
| growth_factor           | Factor by which to increase the number of steps    | 10                 |
+-------------------------+----------------------------------------------------+--------------------+
| max_improvement_loops   | Number of times MCMC should be re-attempted        | 4                  |
+-------------------------+----------------------------------------------------+--------------------+
| num_initial_steps       | Number of sampler steps to take in first iteration | 100                |
+-------------------------+----------------------------------------------------+--------------------+
| min_autocorr_times      | Sets autocorelation criterium to converge (if > 0) | 0                  |
+-------------------------+----------------------------------------------------+--------------------+
| rhat_max                | Sets Gelman-Rubin diagnostic to converge           | 1.01               |
+-------------------------+----------------------------------------------------+--------------------+
| geweke_max              | Sets Geweke diagnostic to converge                 | 2.0                |
+-------------------------+----------------------------------------------------+--------------------+
| progress                | if True, show progress bars                        | True               |
+-------------------------+----------------------------------------------------+--------------------+

.. tip::

    Find detailed information on convergence criteria at `Introduction to Bayesian Analysis Procedures <https://documentation.sas.com/doc/en/statcdc/14.2/statug/statug_introbayes_sect025.htm>`_.