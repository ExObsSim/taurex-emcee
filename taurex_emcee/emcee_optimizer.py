import os
import time

import emcee
import numpy as np
from taurex.optimizer import Optimizer
from taurex.util.util import quantile_corner
from taurex.util.util import recursively_save_dict_contents_to_output


class EmceeSampler(Optimizer):
    os.environ["OMP_NUM_THREADS"] = "1"

    def __init__(
        self,
        observed=None,
        model=None,
        sigma_fraction=0.1,
        nwalkers: int = None,
        nsteps=1e9,
        ntau: int = 100,
        dtau: float = 0.01,
        burnin=None,
        thin=None,
        pool=None,
        moves=None,
        moves_weight=None,
        backend=None,
        run_name=None,
        resume=False,
        progress=True,
    ):
        super().__init__("Emcee", observed, model, sigma_fraction)

        self.nwalkers = int(nwalkers)
        self.nsteps = int(nsteps)
        self.ntau = int(ntau)
        self.dtau = float(dtau)
        self.burnin = burnin
        self.thin = thin
        self.pool = pool

        self.moves = None
        self.get_moves(moves, moves_weight)

        self.backend = (
            emcee.backends.HDFBackend(backend, name=run_name) if backend else None
        )
        self.resume = resume

        self.progress = progress

        self.initial_state = None
        self.mean_acceptance_fraction = None
        self.emcee_output = None
        self.autocorr = None

    def get_moves(self, moves, moves_weight):
        self.moves = moves
        if moves is not None and moves_weight is not None:
            if isinstance(moves, str):
                self.moves = getattr(emcee.moves, moves)()
            elif isinstance(moves_weight, list) and len(moves) != len(moves_weight):
                raise ValueError("Number of moves and moves_weight must be the same")
            elif np.sum(moves_weight) != 1:
                raise ValueError("Moves weights must sum to 1")
            else:
                self.moves = [
                    (getattr(emcee.moves, move)(), weight)
                    for move, weight in zip(moves, moves_weight)
                ]

    def compute_fit(self):
        data = self._observed.spectrum
        datastd = self._observed.errorBar
        sqrtpi = np.sqrt(2 * np.pi)

        def emcee_loglike(params):
            # log-likelihood function called by emcee
            fit_params_container = np.array(params)
            chi_t = self.chisq_trans(fit_params_container, data, datastd)
            loglike = -np.sum(np.log(datastd * sqrtpi)) - 0.5 * chi_t
            return loglike

        def emcee_prior(theta):
            cube = []

            for idx, prior in enumerate(self.fitting_priors):
                if theta[idx] < prior._low_bounds or theta[idx] > prior._up_bounds:
                    val = -np.inf
                else:
                    val = 0

                cube.append(val)

            return np.array(cube)

        def emcee_logprob(params):
            # log-probability function called by emcee
            lp = emcee_prior(params)
            if not np.all(np.isfinite(lp)):
                return np.full(shape=len(params), fill_value=-np.inf)
            return lp + emcee_loglike(params)

        ndim = len(self.fitting_parameters)
        self.warning("Number of dimensions {}".format(ndim))
        self.warning("Fitting parameters {}".format(self.fitting_parameters))

        if self.backend and not self.resume:
            self.backend.reset(self.nwalkers, ndim)

        # Set up the sampler
        self.info("Instantiating fit......")
        sampler = emcee.EnsembleSampler(
            nwalkers=self.nwalkers,
            ndim=ndim,
            log_prob_fn=emcee_logprob,
            moves=self.moves,
            backend=self.backend,
        )

        t0 = time.time()

        # Initialize the walkers
        self.initial_state = (
            np.array(self.fit_values) + np.random.randn(self.nwalkers, ndim) * 1e-3
        )

        # Run the fit
        result = self.run_mcmc(sampler)

        t1 = time.time()
        self.warning("Time taken to run 'Emcee' is %s seconds", t1 - t0)
        self.warning("Fit complete.....")

        # Store the output
        self.emcee_output = self.store_emcee_output(result)

    def run_mcmc(self, sampler):
        self.autocorr = []
        old_tau = tau = np.inf

        for sample in sampler.sample(
            self.initial_state,
            iterations=self.nsteps,
            progress=self.progress,
        ):
            # Only check convergence every 100 steps
            if sampler.iteration % 100:
                continue

            # Compute the autocorrelation time so far
            # Using tol=0 means that we'll always get an estimate even
            # if it isn't trustworthy
            tau = sampler.get_autocorr_time(tol=0)
            self.autocorr.append(np.nanmean(tau))

            # Check convergence
            converged = np.all(tau * self.ntau < sampler.iteration)
            print(f"N x mean tau: {np.nanmean(tau * self.ntau):.3f}")

            self.nsteps = np.nanmean(tau * self.ntau)

            print(f"Sampler iteration: {sampler.iteration}")
            tau_diff = np.abs(old_tau - tau) / tau
            print("tau change:", tau_diff)
            converged &= np.all(tau_diff < self.dtau)
            print(f"Converged? {converged}")
            if converged:
                break
            old_tau = tau

        self.mean_acceptance_fraction = np.nanmean(sampler.acceptance_fraction)
        print(f"Mean acceptance fraction: {self.mean_acceptance_fraction:.3f}")
        # if mean_acceptance_fraction < 0.2, it suggests that the sampler is
        # stuck in a low probability part of parameter space. We can
        # try using more walkers, a different set of starting points, or
        # different parameter limits / priors.
        # if mean_acceptance_fraction > 0.5, it suggests that the sampler
        # is jumping around a lot and wasting time.
        if self.mean_acceptance_fraction < 0.2:
            self.warning("Mean acceptance fraction is low")
        elif self.mean_acceptance_fraction > 0.5:
            self.warning("Mean acceptance fraction is high")

        result = {}

        self.info(f"tau: {tau}")
        result["tau"] = tau

        self.burnin = int(2 * np.max(tau)) if self.burnin is None else self.burnin
        self.info(f"burn-in: {self.burnin}")
        self.thin = int(0.5 * np.min(tau)) if self.thin is None else self.thin
        self.info(f"thin: {self.thin}")

        samples = sampler.get_chain(discard=self.burnin, flat=True, thin=self.thin)
        self.debug(f"flat chain shape: {samples.shape}")
        result["samples"] = samples

        log_prob_samples = sampler.get_log_prob(
            discard=self.burnin, flat=True, thin=self.thin
        )
        self.debug(f"flat log prob shape: {log_prob_samples.shape}")
        weights = np.exp(log_prob_samples - log_prob_samples.max())
        weights /= weights.sum()
        result["weights"] = weights

        return result

    def store_emcee_output(self, result):
        """
        This turns the output from emcee into a dictionary that can
        be output by TauREx

        Parameters
        ----------
        result: :obj:`dict`
            Result from an emcee sample call

        Returns
        -------
        dict
            Formatted dictionary for output

        """

        emcee_output = {}
        emcee_output["Stats"] = {}
        emcee_output["Stats"]["tau"] = result["tau"]
        emcee_output["Stats"]["burnin"] = self.burnin
        emcee_output["Stats"]["thin"] = self.thin
        emcee_output["Stats"][
            "mean_acceptance_fraction"
        ] = self.mean_acceptance_fraction
        emcee_output["Stats"]["autocorr"] = self.autocorr

        fit_param = self.fit_names

        emcee_output["solution"] = {}
        emcee_output["solution"]["samples"] = result["samples"]
        emcee_output["solution"]["weights"] = result["weights"]
        emcee_output["solution"]["fitparams"] = {}

        max_weights = result["weights"].argmax()

        table_data = []

        for idx, param_name in enumerate(fit_param):
            param = {}
            trace = result["samples"][:, idx]
            q_16, q_50, q_84 = quantile_corner(
                trace,
                [0.16, 0.5, 0.84],
                weights=result["weights"],
            )
            param["value"] = q_50
            param["sigma_m"] = q_50 - q_16
            param["sigma_p"] = q_84 - q_50
            param["trace"] = trace
            param["map"] = trace[max_weights]
            table_data.append((param_name, q_50, q_50 - q_16))

            emcee_output["solution"]["fitparams"][param_name] = param

        return emcee_output

    def get_samples(self, solution_idx):
        return self.emcee_output["solution"]["samples"]

    def get_weights(self, solution_idx):
        return self.emcee_output["solution"]["weights"]

    def write_fit(self, output):
        fit = super().write_fit(output)

        if self.emcee_output:
            recursively_save_dict_contents_to_output(output, self.emcee_output)

        return fit

    def chisq_trans(self, fit_params, data, datastd):
        res = super().chisq_trans(fit_params, data, datastd)

        if not np.isfinite(res):
            return np.inf

        return res

    def get_solution(self):
        """

        Generator for solutions and their
        median and MAP values

        Yields
        ------

        solution_no: int
            Solution number (always 0)

        map: :obj:`array`
            Map values

        median: :obj:`array`
            Median values

        extra: :obj:`list`
            Returns Statistics, fitting_params, raw_traces and
            raw_weights

        """

        names = self.fit_names
        opt_map = self.fit_values
        opt_values = self.fit_values
        for k, v in self.emcee_output["solution"]["fitparams"].items():
            # if k.endswith('_derived'):
            #     continue
            idx = names.index(k)
            opt_map[idx] = v["map"]
            opt_values[idx] = v["value"]

        yield 0, opt_map, opt_values, [
            ("Statistics", self.emcee_output["Stats"]),
            ("fit_params", self.emcee_output["solution"]["fitparams"]),
            ("tracedata", self.emcee_output["solution"]["samples"]),
            ("weights", self.emcee_output["solution"]["weights"]),
        ]

    @classmethod
    def input_keywords(self):
        return [
            "emcee",
        ]

    BIBTEX_ENTRIES = [
        """
        @ARTICLE{2013PASP..125..306F,
               author = {{Foreman-Mackey}, Daniel and {Hogg}, David W. and {Lang}, Dustin and et al.},
                title = "{emcee: The MCMC Hammer}",
              journal = {\pasp},
             keywords = {Astrophysics - Instrumentation and Methods for Astrophysics, Physics - Computational Physics, Statistics - Computation},
                 year = 2013,
                month = mar,
               volume = {125},
               number = {925},
                pages = {306},
                  doi = {10.1086/670067},
        archivePrefix = {arXiv},
               eprint = {1202.3665},
         primaryClass = {astro-ph.IM},
               adsurl = {https://ui.adsabs.harvard.edu/abs/2013PASP..125..306F},
              adsnote = {Provided by the SAO/NASA Astrophysics Data System}
        }
        """,
        """
        @ARTICLE{2010CAMCS...5...65G,
               author = {{Goodman}, Jonathan and {Weare}, Jonathan},
                title = "{Ensemble samplers with affine invariance}",
              journal = {Communications in Applied Mathematics and Computational Science},
             keywords = {Markov chain Monte Carlo, affine invariance, ensemble samplers},
                 year = 2010,
                month = jan,
               volume = {5},
               number = {1},
                pages = {65-80},
                  doi = {10.2140/camcos.2010.5.65},
               adsurl = {https://ui.adsabs.harvard.edu/abs/2010CAMCS...5...65G},
              adsnote = {Provided by the SAO/NASA Astrophysics Data System}
        }
        """,
    ]
