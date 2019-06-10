# plotopacdir.py
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import zylconst

#rundir = ['a0.01_0.10_3.5/', 'a0.01_1000.00_3.5/']
gtag = [0.1, 1, 10, 50, 100, 150, 200, 300, 500, 1000]
rundir = []
for ii in gtag:
    rundir.append('a0.01_%.2f_3.5/'%ii)

nrundir = len(rundir)

opacs = range(nrundir)
mopacs = range(nrundir)

pltwav = [434, 851, 1330, 2300, 9098]
pltbeta = [1.0, 0.6]

for ii in range(nrundir):
    fname = rundir[ii] + 'particle.dat'
    op = np.loadtxt(fname)

    opacs[ii] = op
    wav = op[:,0]
    kabs = op[:,1]
    ksca = op[:,2]
    phaseg = op[:,3]
    freq = zylconst.c * 1e4 / wav

    # just plot opacities for each
    nrow, ncol = 2, 1

    fig = plt.figure(0, figsize=(ncol*5, nrow*3))
    # opacity
    ax = fig.add_subplot(nrow, ncol, 1)
    ax.plot(wav, kabs, 'r-', label='kabs')
    ax.plot(wav, ksca, 'b-', label='ksca')
    for ibeta in pltbeta:
        ax.plot(wav, 10.*(freq / 1e12)**ibeta, '--', label=('Beta=%.1f'%ibeta))

    ax.set_title('Opacity')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.legend(loc='best')
    if pltwav is not None:
        for iwav in pltwav:
            ax.axvline(x=iwav, color='k', linestyle=':')
    # asymmetry parameter
    ax = fig.add_subplot(nrow, ncol, 2)
    ax.plot(wav, phaseg)
    ax.set_title('phase g')
    ax.set_xlabel(r'wavelength [$\mu$ m]')
    ax.set_xscale('log')
    ax.set_yscale('log')
    if pltwav is not None:
        for iwav in pltwav:
            ax.axvline(x=iwav, color='k', linestyle=':')

    fig.tight_layout()
    pngname = rundir[ii] + 'opacity.png'
    fig.savefig(pngname)
    plt.close()

