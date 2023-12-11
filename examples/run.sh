#!/bin/bash
# taurex -i parfile.par -R -o selfretrieval.h5
mpirun -np 16 taurex -i parfile.par -R -o selfretrieval.h5
taurex-plot -i selfretrieval.h5 -o /plots --all