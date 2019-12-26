# plotopsize.py
# plot opacity to grain size for various wavelengths
import numpy as np
import matplotlib.pyplot as plt
import zylconst
import os
from scipy.interpolate import interp1d
import dianatools

# settings
datdir = '/scratch/zdl3gk/data/dianaOpacResults'
gtag = [0.1, 1, 10, 50, 100, 150, 200, 300, 500, 1000]
rundir = []
for ii in gtag:
    rundir.append(os.path.join(datdir, 'a0.01_%.2f_3.5/'%ii))

pltwav = [850, 1300, 2600]

dodiffalb = True

# -----
nrundir = len(rundir)
npltwav = len(pltwav)

op = []
gsize = []
kabs = np.zeros([npltwav, nrundir], dtype=np.float64)
ksca = np.zeros([npltwav, nrundir], dtype=np.float64)

for ii in range(nrundir):
    opii = dianatools.readParticle(rundir[ii] + '/particle.dat')
    parii = dianatools.readPar(rundir[ii] + '/parfile.inp')

    # interpolate
    fkabsii = interp1d(opii['wav'], opii['kabs'])
    fkscaii = interp1d(opii['wav'], opii['ksca'])

    for iwav in range(npltwav):
        kabs[iwav, ii] = fkabsii(pltwav[iwav])
        ksca[iwav, ii] = fkscaii(pltwav[iwav])

    op.append(opii)
    gsize.append(parii['amax'])

gsize = np.array(gsize)

# plotting
nrow = 2
ncol = npltwav
fig = plt.figure(0, figsize=(12,8))
for iwav in range(npltwav):
    # kabs, ksca
    ax = fig.add_subplot(nrow, ncol, iwav+1)
    ax.plot(gsize, kabs[iwav, :], '-')
    ax.plot(gsize, ksca[iwav, :], '--')
    ax.set_title('%d'%pltwav[iwav])
    ax.set_xlabel(r'gsize $[\mu m]$')
    if iwav == 0:
        ax.set_ylabel('opacity')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_ylim(kabs[iwav,:].min()*1e-2, max(kabs[iwav,:].max(),ksca[iwav,:].max()))
    ax.axvline(x=pltwav[iwav]/2./np.pi, linestyle=':', color='k')

    # albedo
    axalb = fig.add_subplot(nrow, ncol, iwav+1+ncol)
    alb = ksca[iwav, :] / (kabs[iwav,:]+ksca[iwav,:])
    axalb.plot(gsize, alb)
    if iwav == 0:
        axalb.set_ylabel('albedo')
    axalb.set_xlabel(r'gsize $[\mu m]$')
    axalb.set_xscale('log')
    axalb.axvline(x=pltwav[iwav]/2./np.pi, linestyle=':', color='k')
    axalb.set_ylim(0,1)

fig.tight_layout()
plt.show()

# plot albedo differences
if dodiffalb:
    inc = 45.
    nrow = 1
    ncol = npltwav-1
    fig = plt.figure(1, figsize=(8,5))
    for iwav in range(npltwav-1):
        alb0 = ksca[iwav, :] / (kabs[iwav,:]+ksca[iwav,:])
        alb1 = ksca[iwav+1, :] / (kabs[iwav+1,:] + ksca[iwav+1,:])
        delalb = alb1 - alb0
        dlognu = np.log(1. / pltwav[iwav+1] * pltwav[iwav])
        val0 = 1. / (2. * np.cos(inc*zylconst.rad) + np.sqrt(3.) / np.sqrt(1. - alb0))
        val1 = 1. / (2. * np.cos(inc*zylconst.rad) + np.sqrt(3.) / np.sqrt(1. - alb1))
        dlogval = np.log(val1 / val0)
        gam = dlogval / dlognu
        ax = fig.add_subplot(nrow, ncol, iwav+1)
        ax.plot(gsize, gam+2., 'k-+')
        ax.set_xscale('log')
        ax.set_xlabel(r'gsize $[\mu m]$')
        if iwav == 0:
            ax.set_ylabel(r'$\alpha$')
        ax.set_title('%d - %d'%(pltwav[iwav+1], pltwav[iwav]))

    plt.show()

