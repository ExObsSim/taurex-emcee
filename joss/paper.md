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

`taurex-emcee` is a plugin for the TauREx 3.1 atmospheric retrieval framework [@Al-Refaie:2021] that extends the choice of sampling methods available to the user. The plugin implements an interface to the [emcee](https://emcee.readthedocs.io/en/stable/) sampler [@Foreman-Mackey:2013], which is a popular affine-invariant ensemble sampler widely used in the astronomy community. The interface is automated by adopting the [autoemcee](https://github.com/JohannesBuchner/autoemcee) package by Johannes Buchner, which also handles parallelization. Thus, the `taurex-emcee` plugin enables users to launch parallelized retrievals using the emcee sampler in a straightforward manner. This allows fast retrievals of exoplanet atmospheric spectra, especially when coupled with the GPU-accelerated forward models of the TauREx 3.1 framework [@Al-Refaie:2020].

# Benchmark

<!-- A summary of the results of the benchmarking tests. -->

Emcee vs MultiNest

# Statement of need

<!-- A Statement of need section that clearly illustrates the research purpose of the software and places it in the context of related work. -->

Optimized sampling methods are a key component of any retrieval code. Nested samplers [@Feroz:2009; @Feroz:2019] are a powerful and robust sampling method, successfully applied to the retrieval of exoplanet atmospheric spectra [@Changeat:2020; @Barstow:2020; @Bocchieri:2023]. TauREx 3.1 natively implements a suite of nested samplers, including the [MultiNest](https://github.com/JohannesBuchner/MultiNest) sampler, or makes them available as plugins, such as the [UltraNest](https://github.com/JohannesBuchner/UltraNest) sampler. The primary target of nested samplers is the efficient calculation of the Bayesian `evidence`, whilst the inference of the `posterior` is a by-product. This is regarded as a key advantage of nested samplers, as the `evidence` can be readily used for model selection. However, the `evidence` is not always required, and the interpretation of the `posterior` from nested samplers necessitates some care. Additionally, algorithmic assumptions of nested samplers may require to tailor the priors to explore the parameter space thoroughly.

Where the inference of the Bayesian `posterior` is the primary target, a well-established alternative to nested samplers are a family of Markov chain Monte Carlo methods known as affine-invariant ensemble samplers [@Goodman:2010]. The implementation in [emcee](https://emcee.readthedocs.io/en/stable/) [@Foreman-Mackey:2013] is a popular choice in the astronomy community, as it takes care of the heavy lifting of the sampling process, is well documented, and is straightforward to utilize. To date, the `emcee` sampler is not natively implemented in the TauREx 3.1 retrieval framework. To fill this gap, we developed the `taurex-emcee` plugin, which interfaces the `emcee` sampler to TauREx 3.1, expanding the choice of sampling methods available to the user.

<!-- Compared to nested samplers, affine-invariant ensemble samplers sample directly from the Bayesian `posterior`, and therefore the interpretation of the results is more straightforward, even for non-expert users. Moreover, in some instances nested samplers may require to define bespoke priors to ensure that the parameter space is thoroughly explored, whereas affine-invariant ensemble samplers asymptotically sample the entire parameter space. The trade-off being that the latter are more computationally expensive, and the computational time scales much faster with dimensionality. -->

# Acknowledgements

<!-- Acknowledgement of any financial support. -->

This work was supported by the Italian Space Agency (ASI) with `Ariel` grant n. 2021.5.HH.0.

# References

<!-- A list of key references, including to other software addressing related needs. Note that the references should include full names of venues, e.g., journals and conferences, not abbreviations only understood in the context of a specific discipline. -->
