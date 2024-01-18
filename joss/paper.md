---
title: '`taurex-emcee`: a TauREx 3.1 plugin for the emcee sampler'
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

`taurex-emcee` is a plugin for the TauREx 3.1 atmospheric retrieval framework [@Al-Refaie:2021] that extends the choice of sampling methods available to the user. The plugin provides an interface to the [emcee](https://emcee.readthedocs.io/en/stable/) sampler [@Foreman-Mackey:2013], a popular affine-invariant ensemble sampler widely used in the astronomy community. Running the sampler to convergence is automated through the [autoemcee](https://github.com/JohannesBuchner/autoemcee) package, which also supports parallelization with MPI. Thus, the `taurex-emcee` plugin allows users to easily launch parallelized retrievals of atmospheric spectra with `emcee`. This enables reliable, efficient, and fast retrievals, especially when coupled with TauREx's GPU-accelerated forward models [@Al-Refaie:2020].

`taurex-emcee` is released under the BSD 3-Clause license and is available on [GitHub](insert-url-here). The plugin can be installed from the source code or from [PyPI](insert-url-here), so it can be installed as `pip install taurex-emcee`. The documentation is available on [readthedocs](insert-url-here), including a quick-start guide, a tutorial, a description of the software functionalities, and guidelines for developers. The documentation is continuously updated and is versioned to match the software releases.

# Benchmark

<!-- A summary of the results of the benchmarking tests. -->

We benchmarked the `taurex-emcee` plugin against the `MultiNest` sampler [@Feroz:2009; @Feroz:2019], natively implemented in TauREx 3, on a synthetic transmission spectrum of the hot Jupiter HD 209458b. The aim being first to assess the computational time of the two samplers on a controlled case, second to assess the consistency of the results from the retrievals. The synthetic spectrum and the retrievals were performed on a single node of the Sapienza University of Rome ``Melodie`` server, equipped with one NVIDIA A40 GPU. The high-resolution forward spectrum was generated assuming stellar and planetary parameters of HD 209458b from @Edwards:2019, reported in \autoref{tab:hd-params}, and a gaseous atmosphere with hydrogen and helium at a ratio H$_2$/He = 0.172 and an isothermal temperature profile.

| R$_p$ [R$_J$] | M$_p$ [M$_J$] | T$_p$ [K] | P [d] | R$_s$ [R$_\odot$] | Mag K | T$_s$ [K] | M$_s$ [M$_\odot$] |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1.35 | 0.71 | 1613 | 3.52 | 1.18 | 6.31 | 6,086 | 1.18 |
: Summary of the selected target's properties \label{tab:hd-params}

The atmosphere is simulated with five molecular species as trace gases: H$_2$O (100 ppm), CH$_4$ (10 ppm), CO (1 ppm), CO$_2$ (0.1 ppm), and NH$_3$ (0.01 ppm). Molecular abundances are assumed constant with altitude. Cross sections at a resolution of 15,000 are used for all species, as given in \autoref{tab:opacities}. Collision-induced absorption (CIA) with H$_2$–H$_2$ and H$_2$–He and Rayleigh scattering are included in the calculation. We also include grey opaque clouds with a cloud-top pressure of 1000 Pa. Finally, 100 pressure layers are used to sample the atmosphere, from 1 Pa to 10$^6$ Pa, uniformly in log-space.

| Opacity | Reference(s) |
|:---:|:---:|
| H$_2$-H$_2$ | @Abel:2011, @Fletcher:2018 |
| H$_2$-He | @Abel:2012 |
| H$_2$O | @Polyansky:2018 |
| NH$_3$ | @Coles:2019 |
| CO | @Li:2015 |
| CO$_2$ | @Rothman:2010 |
| CH$_4$ | @Yurchenko:2017 |
: Cross sections and CIA used in the simulations \label{tab:opacities}

To simulate the observation of the transmission spectrum, we assume an observation by the `Ariel` space mission [@Tinetti:2018;@Tinetti:2021] in Tier 2 mode [@Edwards:2019]. We utilize radiometric estimates of the total noise on one observation of HD 209458b obtained with `ArielRad` [@Mugnai:2020], the `Ariel` radiometric simulator now available at the online [exodb.space](https://exodb.space/) website. `ArielRad` is based on the generic point source radiometric model `ExoRad2` [@Mugnai:2023], adapted with the `Ariel` payload configuration. The software versions used are: `ExoRad2` v2.1.113, `ArielRad-payloads` v0.0.17, and `ArielRad` v2.4.26.

In our retrieval benchmarks, we attempt to constrain the abundances of the trace gases, alongside the temperature profile, the planetary radius, and the cloud-top pressure. We perform five retrievals each with `MultiNest` and `emcee`, with increasing number of molecules included in the free parameters (the other molecules being fixed to their true values), from only H$_2$O to all five trace gases. With `MultiNest`, we set the evidence tolerance to 0.5 and sample the parameter space through 1500 live points. With `emcee`, we utilize 100 walkers and run two independent chains, each to convergence, where we adopt the default convergence criteria of the [autoemcee](https://github.com/JohannesBuchner/autoemcee) package, i.e. the Geweke convergence diagnostic [@Geweke:1991] is z-score < 2.0 and the Gelman-Rubin rank diagnostic [@Gelman:1992] is $\hat{r}$ < 1.01. When iterating the chains, we increase the number of steps by multiplying the number of steps of the previous iteration by a `growth` factor of 2, a parameter that we have added to the `taurex-emcee` plugin as the default value of 10 was too conservative for our tests. As a first comparison, we report in \autoref{tab:times} the computational time of the retrievals with the two samplers.

|  Fitted molecules                   |  Emcee [s] |  MultiNest [s] |
|:-----------------------------------:|:----------:|:--------------:|
|  H$_2$O                             |   16,465   |      5,423     |
|  H$_2$O, CH$_4$                     |    6,550   |      7,505     |
|  H$_2$O, CH$_4$, CO                 |   15,247   |     10,093     |
|  H$_2$O, CH$_4$, CO, CO$_2$         |   14,930   |     12,847     |
|  H$_2$O, CH$_4$, CO, CO$_2$, NH$_3$ |   30,151   |     17,097     |
: Runtime of the retrievals with `emcee` and `MultiNest` samplers. \label{tab:times}

Figures can be included like this:

![Caption for spectrum figure. \label{fig:spectrum}](spectrum.pdf){height=100%}

and referenced from text using \autoref{fig:spectrum}.

Figure sizes can be customized by adding an optional second parameter:

![Caption for posteriors figure.\label{fig:posteriors}](posteriors.pdf){height=100%}

and referenced from text using \autoref{fig:posteriors}.


<!-- Compared to nested samplers, affine-invariant ensemble samplers sample directly from the Bayesian `posterior`, and therefore the interpretation of the results is more straightforward, even for non-expert users. Moreover, in some instances nested samplers may require to define bespoke priors to ensure that the parameter space is thoroughly explored, whereas affine-invariant ensemble samplers asymptotically sample the entire parameter space. The trade-off being that the latter are more computationally expensive, and the computational time scales much faster with dimensionality. -->

# Statement of need

<!-- A Statement of need section that clearly illustrates the research purpose of the software and places it in the context of related work. -->

Optimized sampling methods are a key component of any retrieval code. Nested samplers [@Feroz:2009; @Feroz:2019] are a powerful and robust sampling method, successfully applied to the retrieval of exoplanet atmospheric spectra [@Changeat:2020; @Barstow:2020; @Bocchieri:2023]. TauREx 3.1 natively implements a suite of nested samplers, including the [MultiNest](https://github.com/JohannesBuchner/MultiNest) sampler, or makes them available as plugins, such as the [UltraNest](https://github.com/JohannesBuchner/UltraNest) sampler. The primary target of nested samplers is the efficient calculation of the Bayesian `evidence`, whilst the inference of the `posterior` is a by-product. This is regarded as a key advantage of nested samplers, as the `evidence` can be readily used for model selection. However, the `evidence` is not always required, and the interpretation of the `posterior` from nested samplers necessitates some care. Additionally, algorithmic assumptions of nested samplers may require to tailor the priors to explore the parameter space thoroughly.

Where the inference of the Bayesian `posterior` is the primary target, a well-established alternative to nested samplers are a family of Markov chain Monte Carlo methods known as affine-invariant ensemble samplers [@Goodman:2010]. The implementation in [emcee](https://emcee.readthedocs.io/en/stable/) [@Foreman-Mackey:2013] is a popular choice in the astronomy community, as it takes care of the heavy lifting of the sampling process, is well documented, and is straightforward to utilize. To date, the `emcee` sampler is not natively implemented in the TauREx 3.1 retrieval framework, nor elsewhere in other retrieval codes, to the knowledge of the authors. To fill this gap, we developed the `taurex-emcee` plugin, which interfaces the `emcee` sampler to TauREx. Key advantages of `taurex-emcee` are that it affords a more straightforward interpretation of the `posterior` and is more robust to the choice of priors. However, the current implementation is not intended to explore multimodal `posteriors`, for which nested samplers will inevitably be more efficient. Moreover, we caveat that it may require substantial computational time to sample high-dimensional parameter spaces with `emcee`, which can be mitigated by coupling `taurex-emcee` with TauREx's GPU-accelerated forward models [@Al-Refaie:2020].

# Acknowledgements

<!-- Acknowledgement of any financial support. -->

This work was supported by the Italian Space Agency (ASI) with `Ariel` grant n. 2021.5.HH.0.

# References

<!-- A list of key references, including to other software addressing related needs. Note that the references should include full names of venues, e.g., journals and conferences, not abbreviations only understood in the context of a specific discipline. -->
