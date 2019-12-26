# calc_diana.py
# calculate the dianan opacities
import numpy as np
import os
import dianatools

# common setttings
lmin = 0.05 #[micron]
lmax = 1e4 #[micron]
nlam = 300

apow = 3.5
na = 50

fcarbon = 0.13
Vcarbon = 0.15
porosity = 0.25
fmax = 0.8

parfname = 'parfile.inp'
dirfmt = 'a%.2f_%.2f_%.1f'
datdir = '/scratch/zdl3gk/data/dianaOpacResults'

# grid of parameters
aminaxis = np.array([0.01], dtype=np.float64)
namin = len(aminaxis)

#amaxaxis = np.geomspace(1e-1, 1e3, num=10, dtype=np.float64)
amaxaxis=np.array([0.1, 1., 10., 50., 100., 150., 200., 300., 500.,1e3], dtype=np.float64)
namax = len(amaxaxis)

# calculate
for ii in range(namin):
    amin = aminaxis[ii]
    for jj in range(namax):
        amax = amaxaxis[jj]

        # call dianaopacity
        com = 'dianaopacity '
        # wavelength
        com = com + ' -lmin %.2f -lmax %f -nlam %d'%(lmin, lmax, nlam)

        # grain size 
        com = com + ' -amin %.2f -amax %f -na %d -apow %.1f'%(amin, amax, na, apow)

        # carbon
        com = com + ' -fcarbon %.2f -Vcarbon %.2f'%(fcarbon, Vcarbon)

        # porosity and irregularity
        com = com + ' -porosity %.2f -fmax %.2f'%(porosity, fmax)

        # call the code
        os.system(com)

        if os.path.isfile('particle.dat') is False:
            raise ValueError('output does not exist: command = %s'%com)

        # create a parameter file for log purposes
        if datdir is not None:
            parfname = os.path.join(datdir, parfname)
            dianatools.writePar(parfname, lmin, lmax, nlam,
                     amin, amax, apow, na,
                     fcarbon, Vcarbon, porosity, fmax)

        # move the data
        dirname = dirfmt%(amin, amax, apow)
        if datdir is not None:
            dirname = os.path.join(datdir, dirname)
        os.system('mkdir '+dirname)
        os.system('mv particle.dat %s %s'%(parfname, dirname))
