---
title: '`taurex-emcee`: automated, parallelized atmospheric retrievals with TauREx&thinsp;3.1 and the `emcee` sampler'
tags:
  - Python
  - astronomy
  - exoplanets
  - taurex
  - retrieval
  - emcee
authors:
  - name: Andrea Bocchieri
    orcid: 0000-0002-8846-7961
    # equal-contrib: true
    affiliation: "1"
  - name: Quentin Changeat
    orcid: 0000-0001-6516-4493
    affiliation: "2"
  - name: Lorenzo V. Mugnai
    orcid: 0000-0002-9007-9802
    affiliation: "3,4,5"
  - name: Enzo Pascale
    orcid: 0000-0002-3242-8154
    affiliation: "1"            
affiliations:
 - name: Department of Physics, La Sapienza Università di Roma, Piazzale Aldo Moro 2, Roma, 00185, Italy
   index: 1
 - name: European Space Agency (ESA), ESA Office, Space Telescope Science Institute (STScI), Baltimore, MD, 21218, USA
   index: 2
 - name: School of Physics and Astronomy, Cardiff University, Queens Buildings, The Parade, Cardiff, CF24 3AA, UK
   index: 3     
 - name: Department of Physics and Astronomy, University College London, Gower Street, London, WC1E 6BT, UK
   index: 4      
 - name: INAF, Osservatorio Astronomico di Palermo, Piazza del Parlamento 1, Palermo, I-90134, Italy
   index: 5 
date: 12 January 2024
bibliography: paper.bib

---

# Summary

<!-- A summary describing the high-level functionality and purpose of the software for a diverse, non-specialist audience. -->

`taurex-emcee` is a plugin for the TauREx&thinsp;3.1 atmospheric retrieval framework [@Al-Refaie:2020;@Al-Refaie:2021] that extends the choice of sampling methods available to the user. The plugin provides an interface to the [emcee](https://emcee.readthedocs.io/en/stable/) sampler [@Foreman-Mackey:2013], a popular affine-invariant ensemble sampler widely used in the astronomy community. Running the sampler to convergence is automated through the [autoemcee](https://github.com/JohannesBuchner/autoemcee) package, which also supports MPI parallelization. Thus, the `taurex-emcee` plugin allows users to easily launch parallelized retrievals of atmospheric spectra with `emcee`. This enables reliable, efficient, and fast retrievals.

`taurex-emcee` is released under the BSD 3-Clause license and is available on [GitHub](https://github.com/ExObsSim/taurex-emcee). The plugin can be installed from the source code or from [PyPI](insert-url-here), so it can be installed as `pip install taurex-emcee`. The documentation is available on [readthedocs](insert-url-here), including a quick-start guide, a tutorial, a description of the software functionalities, and guidelines for developers. The documentation is continuously updated and is versioned to match the software releases.

# Benchmark

<!-- A summary of the results of the benchmarking tests. -->

We benchmarked the `taurex-emcee` plugin against the `MultiNest` sampler [@Feroz:2009; @Feroz:2019], natively implemented in TauREx&thinsp;3, on a synthetic transmission spectrum of a HD-209458&thinsp;b-like hot Jupiter. The aim being first to assess the computational time of the two samplers on a controlled case, second to assess the consistency of the results from the retrievals. The synthetic spectrum and the retrievals were performed on a single node of the Sapienza University of Rome ``Melodie`` server (128-core Intel(R) Xeon(R) Platinum 8358 CPU clocked at 2.60 GHz), equipped with one NVIDIA A40 GPU, and using the TauREx&thinsp;3.1 GPU-accelerated forward model. The software versions used are: `TauREx` v3.1.4, `taurex-cuda` v1.0.1, `MultiNest` v3.10, and `emcee` v3.1.4. The high-resolution forward spectrum was generated assuming stellar and planetary parameters of HD-209458&thinsp;b from @Edwards:2019, reported in \autoref{tab:hd-params}.

| R$_\text{P}$ [R$_\text{J}$] | M$_\text{P}$ [M$_\text{J}$] | T$_\text{P}$ [K] | P$~$[d] | R$_s$ [R$_\odot$] | Mag$_\text{K}$ | T$_\text{s}$ [K] | M$_s$ [M$_\odot$] |
|:---------------------------:|:---------------------------:|:----------------:|:-----:|:-----------------:|:-----:|:----------------:|:-----------------:|
| 1.35                        | 0.71                        | 1613             | 3.52  | 1.18              | 6.31  | 6,086            | 1.18              |
: Summary of the selected target's properties. \label{tab:hd-params}

The stellar spectrum is simulated with PHOENIX stellar models [@Husser:2013], and the planetary atmosphere is gaseous, with hydrogen and helium at a ratio H$_2$/He = 0.172, and has an isothermal temperature profile. We consider five molecular species as atmospheric trace gases: H$_2$O (100 ppm), CH$_4$ (10 ppm), CO (1 ppm), CO$_2$ (0.1 ppm), and NH$_3$ (0.01 ppm). Molecular abundances are assumed constant with altitude. We utilize cross sections at a resolution of 15,000 for all species, as given in \autoref{tab:opacities}. Collision-induced absorption (CIA) with H$_2$–H$_2$ and H$_2$–He and Rayleigh scattering are included in the calculation. We also include fully-opaque gray clouds with a cloud-top pressure of 1000 Pa. Finally, 100 pressure layers are used to sample the atmosphere, from 1 Pa to 10$^6$ Pa, uniformly in log-space.

| Opacity     | Reference(s)               |
|:-----------:|:--------------------------:|
| H$_2$-H$_2$ | @Abel:2011, @Fletcher:2018 |
| H$_2$-He    | @Abel:2012                 |
| H$_2$O      | @Polyansky:2018            |
| NH$_3$      | @Coles:2019                |
| CO          | @Li:2015                   |
| CO$_2$      | @Rothman:2010              |
| CH$_4$      | @Yurchenko:2017            |
: Cross sections and CIA used in the simulations. \label{tab:opacities}

To simulate the observation of the transmission spectrum, we assume an observation by the `Ariel` space mission [@Tinetti:2018;@Tinetti:2021] in Tier 2 mode [@Edwards:2019]. We utilize radiometric estimates of the total noise on one observation of HD-209458&thinsp;b obtained with `ArielRad` [@Mugnai:2020], the `Ariel` radiometric simulator. `ArielRad` is based on the generic point source radiometric model `ExoRad2` [@Mugnai:2023], adapted with the `Ariel` payload configuration. The software versions used are: `ExoRad2` v2.1.113, `ArielRad-payloads` v0.0.17, and `ArielRad` v2.4.26. Furthermore, we fix the data points of the observed spectrum to the expected values, i.e. we do not scatter the spectrum with the noise estimates; this is done to ensure that the results of the retrievals are not affected by the realization of the noise.

In our retrieval benchmarks, we attempt to constrain the abundances of the trace gases, alongside the temperature profile, the planetary radius, and the cloud-top pressure. \autoref{tab:priors} lists each parameter, its units, and the priors (with corresponding scale) used in the retrievals.

| Parameter         | Unit         |        Prior          |  Scale  |
|:-----------------:|:------------:|:---------------------:|:-------:|
| R$_\text{P}$      | R$_\text{J}$ |       \pm10$\%$       |  linear |
| T                 |   K          |       100; 4000       |  linear |
| H$_2$O            |  VMR         | 10$^{-12}$; 10$^{-1}$ |   log   |
| CH$_4$            |  VMR         | 10$^{-12}$; 10$^{-1}$ |   log   |
| CO                |  VMR         | 10$^{-12}$; 10$^{-1}$ |   log   |
| CO$_2$            |  VMR         | 10$^{-12}$; 10$^{-1}$ |   log   |
| NH$_3$            |  VMR         | 10$^{-12}$; 10$^{-1}$ |   log   |
| P$_\text{clouds}$ |   Pa         |        1; 10$^{6}$    |   log   |
: Parameters and priors used in the retrievals. \label{tab:priors}

We perform five retrievals each with `MultiNest` and `emcee`, with increasing number of molecules included in the free parameters (the other molecules being fixed to their true values), from only H$_2$O to all five trace gases. With `MultiNest`, we set the evidence tolerance to 0.5 and sample the parameter space through 1500 live points. With `emcee`, we utilize 100 walkers and run two independent chains, each to convergence, where we adopt the default convergence criteria of the [autoemcee](https://github.com/JohannesBuchner/autoemcee) package, i.e. the Geweke convergence diagnostic [@Geweke:1991] is z-score < 2.0 and the Gelman-Rubin rank diagnostic [@Gelman:1992] is $\hat{r}$ < 1.01. When iterating the chains, we increase the number of steps by multiplying the number of steps of the previous iteration by a `growth` factor of 2, a parameter that we have enabled as the default value of 10 was deemed too conservative for our tests. As a first comparison, we report in \autoref{tab:times} the computational time of the retrievals with `emcee` and `MultiNest`, alongside the number of samples of each retrieval.

| Fitted molecules                   | `emcee`$~$[s] | `MultiNest`$~$[s] | `emcee`$~$[$\#$] | `MultiNest`$~$[$\#$] |
|:----------------------------------:|:-------------:|:-----------------:|:----------------:|:--------------------:|
| H$_2$O                             |      6,342    |         5,423     |         40,000   |           18,779     |
| H$_2$O, CH$_4$                     |      6,550    |         7,505     |         40,000   |           21,975     |
| H$_2$O, CH$_4$, CO                 |     15,247    |        10,093     |         80,000   |           21,851     |
| H$_2$O, CH$_4$, CO, CO$_2$         |     14,930    |        12,847     |         80,000   |           23,137     |
| H$_2$O, CH$_4$, CO, CO$_2$, NH$_3$ |     30,151    |        17,097     |        160,000   |           23,151     |
: Sampling times and number of samples of the retrievals with each sampler. \label{tab:times}

`MultiNest` is faster than `emcee` for all the retrievals except the one with H$_2$O and CH$_4$, where the computational time is around 15 minutes longer. The difference in speed correlates with the number of samples, which is higher for `emcee` than `MultiNest` for all the retrievals. Additionally, run-times with `MultiNest` scale slower with increasing dimensionality of the parameter space.

Next, we compare the results of the retrievals. For simplicity, we only discuss the retrieval with the full stack of trace gases included in the free parameters, as the results of the other retrievals are consistent. \autoref{fig:spectrum} shows the retrieved spectrum yielded by the two samplers, alongside the observed spectrum. The retrieved spectrum is shown as the best-fit model and the 1$\sigma$ and 2$\sigma$ confidence intervals. The retrieved spectra are consistent with each other and with the observed spectrum within the experimental uncertainties.

![Best-fit spectra for the HD-209458&thinsp;b retrievals with `MultiNest` (blue) and `emcee` (orange). The synthetic `observed` spectrum is shown as the black error bars. The 1$\sigma$ and 2$\sigma$ confidence intervals are shown as the shaded regions. The error bars of the observed spectrum are generated with `ArielRad` [@Mugnai:2020] and the spectral grid corresponds to the `Ariel` Tier 2 mode [@Edwards:2019]. \label{fig:spectrum}](spectrum.pdf){height=100%}

\autoref{fig:posteriors} shows the `posteriors` of the retrieved parameters, and \autoref{tab:fit-params} reports the median and 16$\%$ and 84$\%$ quantiles of the marginalized `posteriors` relative to the median.

![Posterior distributions of the retrieved parameters for the HD-209458&thinsp;b simulated observations with `MultiNest` (blue) and `emcee` (orange). The true values are shown as the black lines. The vertical dashed lines in the histograms on the diagonal show the median and 16$\%$ and 84$\%$ quantiles. \label{fig:posteriors}](posteriors.pdf){height=100%}

| Parameter              | True value | `emcee`                   | `MultiNest`               |
|:----------------------:|:----------:|:-------------------------:|:-------------------------:|
| R$_\text{P}$           | 1.35       |  1.34$^{+0.02}_{-0.02}$   |  1.34$^{+0.02}_{-0.02}$   |
| T                      | 1613       |  1635.8$^{+98.9}_{-93.4}$ |  1631.4$^{+97.5}_{-87.0}$ |
| log(H$_2$O)            | -4         |  -3.31$^{+0.71}_{-0.85}$  |  -3.21$^{+0.87}_{-0.91}$  |
| log(CH$_4$)            | -5         |  -4.29$^{+0.72}_{-0.87}$  |  -4.20$^{+0.89}_{-0.92}$  |
| log(CO)                | -6         |  < -3.6                   |  < -3.8                   |
| log(CO$_2$)            | -7         |  -6.40$^{+0.80}_{-0.90}$  |  -6.31$^{+0.93}_{-0.93}$  |
| log(NH$_3$)            | -8         |  < -5.2                   |  < -5.2                   |
| log(P$_\text{clouds}$) | 3          |  $2.27^{+0.91}_{-0.72}$   |  2.19$^{+0.94}_{-0.88}$   |
: Retrieved parameters and their uncertainties. True values are reported for comparison. \label{tab:fit-params}

The similarity of the results from the two samplers is reassuring, and the retrieved parameters are consistent with the true values within 1$\sigma$. It is worth noting that the median values are, to an extent, biased for both samplers, in essentially the same manner. This result is expected, as the retrieval traces the degeneracies between the parameters and the fitted molecules have strong correlations with each other, as seen in \autoref{fig:posteriors}. In addition, for some parameters, namely CO and NH$_3$, due to the combination of opacities and abundances, the retrievals only recover an upper limit. In these cases, mean, median, and mode are not defined, and the reported values depend on the choice of the prior. Therefore, for CO and NH$_3$, \autoref{tab:fit-params} reports the 95$\%$ upper limit, defined as the cumulative of the marginalized `posterior` at the 95$\%$ quantile.

In summary, while the `emcee` sampler is generally slower than `MultiNest`, it is a robust and reliable alternative to nested samplers, as shown by the consistency of the results from the two samplers in our benchmark.

# Statement of need

<!-- A statement of need section that clearly illustrates the research purpose of the software and places it in the context of related work. -->

Optimized sampling methods are a key component of any retrieval code. Nested samplers [@Buchner:2023] are a powerful and robust sampling method, successfully applied to the retrieval of exoplanet atmospheric spectra [@Changeat:2020;@Barstow:2020;@Mugnai:2021;@Changeat:2022;@Bocchieri:2023;@Jaziri:2024]. TauREx&thinsp;3.1 natively implements a suite of nested samplers, including the [MultiNest](https://github.com/JohannesBuchner/MultiNest) sampler, or makes them available as plugins, such as the [UltraNest](https://github.com/JohannesBuchner/UltraNest) sampler. The primary target of nested samplers is the efficient calculation of the Bayesian `evidence`, whilst the inference of the `posterior` is a by-product. This is regarded as a key advantage of nested samplers, as the `evidence` can be readily used for model selection. However, the `evidence` is not always required, and the interpretation of the `posterior` from nested samplers necessitates some care. Additionally, algorithmic assumptions of nested samplers may require to tailor the priors to explore the parameter space thoroughly.

Where the inference of the Bayesian `posterior` is the primary target, a well-established alternative to nested samplers are a family of Markov chain Monte Carlo methods known as affine-invariant ensemble samplers [@Goodman:2010]. The implementation in [emcee](https://emcee.readthedocs.io/en/stable/) is a popular choice in the astronomy community, as it takes care of the heavy lifting of the sampling process, is well documented, and is straightforward to utilize. To date, the `emcee` sampler is not natively implemented in the TauREx&thinsp;3.1 retrieval framework, nor elsewhere in other retrieval codes, to the knowledge of the authors. To fill this gap, we developed the `taurex-emcee` plugin, which interfaces the `emcee` sampler to TauREx.

Key advantages of `taurex-emcee` are that it affords a more straightforward interpretation of the `posterior` and is more robust to the choice of priors. However, the current implementation is not intended to explore multimodal `posteriors`, for which nested samplers are more efficient but also require extra caution in interpreting the results. Moreover, we caveat that it may require substantial computational time to sample high-dimensional parameter spaces with `emcee`, which can be mitigated by coupling `taurex-emcee` with TauREx's GPU-accelerated forward models. To conclude, while `taurex-emcee` is a new and powerful tool for the exoplanet community, comparison of various statistical inference strategies, such as `MultiNest`, `UltraNest`, Variational Inference [@Yip:2024], and now `emcee`, is necessary to ensure un-biased estimates of parameter space in exo-atmospheric studies with HST, JWST, and Ariel.

# Acknowledgements

<!-- Acknowledgement of any financial support. -->

This work was supported by the Italian Space Agency (ASI) with `Ariel` grant n. 2021.5.HH.0.

# References

<!-- A list of key references, including to other software addressing related needs. Note that the references should include full names of venues, e.g., journals and conferences, not abbreviations only understood in the context of a specific discipline. -->
