---
title: 'taurex-emcee: A TauREx~3.1 plugin for retrievals using the emcee sampler'
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
    orcid: 
    affiliation: "2"
  - name: Lorenzo V. Mugnai
    orcid: 
    affiliation: "3,4,5"
  - name: Enzo Pascale
    orcid: 
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

The `taurex-emcee` plugin is a plugin for the TauREx~3.1 retrieval code that allows users to perform retrievals using the emcee sampler. 

# Statement of need

<!-- A Statement of need section that clearly illustrates the research purpose of the software and places it in the context of related work. -->

Optimized sampling methods are a key component of any retrieval code. Nested samplers are generally considered the most robust sampling method for retrieval of exoplanet atmospheric spectra, and are natively implemented in TauREx~3.1. The estimation of the Bayesian `evidence` is the primary product of nested samplers, whereas the estimation of the Bayesian `posterior` is a by-product. Compared to nested samplers, affine-invariant ensemble samplers sample directly from the Bayesian `posterior`, and therefore the interpretation of the results is more straightforward, even for non-expert users. Moreover, in some instances nested samplers may require to define bespoke priors to ensure that the parameter space is thoroughly explored, whereas affine-invariant ensemble samplers asymptotically sample the entire parameter space. The trade-off being that the latter are more computationally expensive, and the computational time scales much faster with dimensionality.

The emcee sampler is a popular affine-invariant ensemble sampler that has been used in many fields of astronomy, including exoplanet atmospheric retrievals. The emcee sampler is a popular affine-invariant ensemble sampler that has been used in many fields of astronomy, including exoplanet atmospheric retrievals. The emcee sampler is implemented in the Python package [emcee](https://emcee.readthedocs.io/en/stable/), which is widely used in the astronomy community. However, the emcee sampler is not implemented in the TauREx~3.1 retrieval code, which is a popular open-source code for exoplanet atmospheric retrievals. The `taurex-emcee` plugin implements the emcee sampler in TauREx~3.1, allowing users to perform retrievals using the emcee sampler. The `taurex-emcee` plugin is compatible with the TauREx~3.1 parallelization framework, allowing users to perform parallelized retrievals using the emcee sampler.

# Acknowledgements

<!-- Acknowledgement of any financial support. -->

Andrea Bocchieri and Enzo Pascale acknowledge funding by the Italian Space Agency (ASI) with \ARIEL\ grant n. 2021.5.HH.0.

# References

<!-- A list of key references, including to other software addressing related needs. Note that the references should include full names of venues, e.g., journals and conferences, not abbreviations only understood in the context of a specific discipline. -->
