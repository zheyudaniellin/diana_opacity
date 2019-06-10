# trans_radmc3d.py
# translate certain opacity files to radmc3d
import numpy as np
import dianatools
import matplotlib.pyplot as plt
import pdb

# settings
collect = True 	# true to collect into one set, else separate them. If collected, the opacity files are stored into the current directory

outputdir = 'run1/' # if collect=True

# the directories with diana opacities
opacdir = ['a0.01_0.10_3.5/', 'a0.01_10.00_3.5/']
#opacdir = ['a0.01_%.2f_3.5/'%ig for ig in [0.1, 1, 10, 50, 100, 150, 200, 300, 500, 1000]]

ext = ['0.1', '10']
#ext = ['avg' for ii in opacdir]

dweights = np.zeros(len(ext)) + 1.
matdens = np.zeros(len(ext)) + 1.

nopac = len(opacdir)

# other set up
fparticle = [idir + 'particle.dat' for idir in opacdir]
fpar = [idir + 'parfile.inp' for idir in opacdir]

# translation
if collect:
    op = dianatools.diana2radmc3d(fparticle, fpar, dweights, matdens,ext=ext, outdir=outputdir)
else:
    for ii in range(nopac):
        opii = dianatools.diana2radmc3d(fparticle[ii], fpar[ii], 
            np.array([1]), [matdens[ii]],
            ext=ext[ii], outdir=opacdir[ii])


