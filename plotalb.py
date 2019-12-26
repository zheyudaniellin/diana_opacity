# plotalb.py
# plots albedo
import numpy as np
import matplotlib.pyplot as plt
import fneq
import fntools
from radmc3dPy import *
from scipy.interpolate import interp1d

datdir = '/scratch/zdl3gk/data/dianaOpacResults'
#rundir = ['a0.01_0.10_3.5/', 'a0.01_1000.00_3.5/']
gtag = [0.1, 1, 10, 50, 100, 150, 200, 300, 500, 1000]
rundir = []
for ii in gtag:
    rundir.append(os.path.join(datdir, 'a0.01_%.2f_3.5/'%ii))


nrundir = len(rundir)


opacs = range(nrundir)
mopacs = range(nrundir)

pltwav = [434, 851, 1330, 2300, 9098]
pltbeta = [1.0, 0.6]

for ii in range(nrundir):
    op = dustopac.radmc3dDustOpac()
    masteropac = op.readMasterOpac(fdir=rundir[ii])
    ext = masteropac['ext']
    for idust in range(len(ext)):
        op.readOpac(ext=ext[idust], scatmat=masteropac['scatmat'][idust], fdir=rundir[ii])
    #if ppar['alignment_mode'] is 1:
    #    op.makeDustAlignFact(ppar=ppar, wav=wav)

    opacs[ii] = op
    mopacs[ii] = masteropac

    # just plot opacities for each
    nspec = len(op.wav)
    ncol = int(np.ceil(np.sqrt(nspec)))
    nrow = int(np.ceil(nspec / float(ncol)))

    fig = plt.figure(0, figsize=(ncol*5, nrow*3))
    for ispec in range(nspec):
        ax = fig.add_subplot(nrow, ncol, ispec+1)
        alb = op.ksca[ispec] / (op.kabs[ispec] + op.ksca[ispec])
        ax.plot(op.wav[ispec], alb, 'r-')

        ax.set_title('ispec=%d'%ispec)
        ax.set_xscale('log')
        plt.legend(loc='best')
        if pltwav is not None:
            for iwav in pltwav:
                ax.axvline(x=iwav, color='k', linestyle=':')
    pngname = rundir[ii] + 'albedo.png'
    fig.savefig(pngname)
    plt.close()

