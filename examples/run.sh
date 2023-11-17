#!/bin/bash
taurex -i emcee_selfretrieval_gpu.par -R -o ../output/emcee_selfretrieval.h5
taurex-plot -i ../output/emcee_selfretrieval.h5 -o ../output/plots --all