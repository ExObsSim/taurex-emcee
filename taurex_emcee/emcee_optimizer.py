import emcee
import time
from taurex.optimizer import Optimizer
import numpy as np
from taurex.util.util import quantile_corner
from taurex.util.util import recursively_save_dict_contents_to_output


# TODO: implement emcee sampler
class EmceeSampler(Optimizer):

    def __init__(self,
                 observed=None,
                 model=None,
                 ):
        super().__init__('Emcee', observed, model, )
        self.emcee_output = None

        raise NotImplementedError

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
            # prior distributions called by emcee. Implements a uniform prior
            # converting parameters from normalised grid to uniform prior
            cube = []

            for idx, prior in enumerate(self.fitting_priors):
                cube.append(prior.sample(theta[idx]))

            return np.array(cube)

        sampler = emcee.somesampler

        sampler_choice = {
            'key': emcee.smth,
        }

        stepchoice = self.stepsampler.lower()

        if stepchoice is not None and stepchoice in sampler_choice:
            sampler.stepsampler = 'probably do something here'

        t0 = time.time()

        result = sampler.run(
            'some options'
        )
        t1 = time.time()

        self.warning("Time taken to run 'Emcee' is %s seconds", t1 - t0)

        self.warning('Fit complete.....')

        self.emcee_output = self.store_emcee_output(result)

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
        emcee_output['Stats'] = {}
        emcee_output['Stats']['Some stats'] = 'some stats'

        fit_param = self.fit_names

        # The below needs re-implementing
        samples = result['weighted_samples']['points']
        weights = result['weighted_samples']['weights']
        logl = result['weighted_samples']['logl']
        mean, cov = result['posterior']['mean'], result['posterior']['stdev']
        emcee_output['solution'] = {}
        emcee_output['solution']['Some results'] = 'some results'
        # emcee_output['solution']['covariance'] = cov
        emcee_output['solution']['fitparams'] = {}

        max_weight = weights.argmax()

        table_data = []

        for idx, param_name in enumerate(fit_param):
            param = {}
            param['mean'] = mean[idx]
            param['sigma'] = cov[idx]
            trace = samples[:, idx]
            q_16, q_50, q_84 = quantile_corner(trace, [0.16, 0.5, 0.84],
                                               weights=np.asarray(weights))
            param['value'] = q_50
            param['sigma_m'] = q_50 - q_16
            param['sigma_p'] = q_84 - q_50
            param['trace'] = trace
            param['map'] = trace[max_weight]
            table_data.append((param_name, q_50, q_50 - q_16))

            emcee_output['solution']['fitparams'][param_name] = param

        return emcee_output

    def get_samples(self, solution_idx):
        return self.emcee_output['solution']['samples']

    def get_weights(self, solution_idx):
        return self.emcee_output['solution']['weights']

    def write_fit(self, output):
        fit = super().write_fit(output)

        if self.emcee_output:
            recursively_save_dict_contents_to_output(
                output, self.emcee_output)

        return fit

    def chisq_trans(self, fit_params, data, datastd):
        res = super().chisq_trans(fit_params, data, datastd)

        if not np.isfinite(res):
            return 1e20

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
        for k, v in self.emcee_output['solution']['fitparams'].items():
            # if k.endswith('_derived'):
            #     continue
            idx = names.index(k)
            opt_map[idx] = v['map']
            opt_values[idx] = v['value']

        yield 0, opt_map, opt_values, [('Statistics', self.emcee_output['Stats']),
                                       ('fit_params',
                                        self.emcee_output['solution']['fitparams']),
                                       ('tracedata',
                                        self.emcee_output['solution']['samples']),
                                       ('weights', self.emcee_output['solution']['weights'])]

    @classmethod
    def input_keywords(self):
        return ['emcee', ]

    BIBTEX_ENTRIES = [
        """
        @article{Author,
            title={},
            volume={},
            ISSN={},
            url={},
            DOI={},
            number={},
            journal={},
            publisher={},
            author={},
            year={},
            month={},
            pages={}
        }
       """,
    ]
