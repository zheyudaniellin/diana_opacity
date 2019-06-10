# dianatools.py
import numpy as np
import os
import pdb
import zylconst

def writePar(fname, lmin, lmax, nlam,
        amin, amax, apow, na,
        fcarbon, Vcarbon, porosity, fmax):
    with open(fname, 'w') as wfile:
        wfile.write('lmin = %.2e \n'%lmin)
        wfile.write('lmax = %.2e \n'%lmax)
        wfile.write('nlam = %d \n'%nlam)
        wfile.write('amin = %.2e \n'%amin)
        wfile.write('amax = %.2e \n'%amax)
        wfile.write('apow = %.2e \n'%apow)
        wfile.write('na = %d \n'%na)
        wfile.write('fcarbon = %.4e \n'%fcarbon)
        wfile.write('Vcarbon = %.4e \n'%Vcarbon)
        wfile.write('porosity = %.4e \n'%porosity)
        wfile.write('fmax = %.2e \n'%fmax)

def readPar(fname):
    par = {}
    with open(fname, 'r') as rfile:
        for line in rfile:
            splitted = line.split()
            par[splitted[0]] = float(splitted[2])
    return par

def readParticle(fname):
    # read fname which should be particle.dat in some directory
    if os.path.isfile(fname) is False:
        raise ValueError('file does not exist: %s'%fname)

    op = np.loadtxt(fname)
    dat = {}
    dat['wav'] = op[:,0]
    dat['kabs'] = op[:,1]
    dat['ksca'] = op[:,2]
    dat['phaseg'] = op[:,3]

    return dat

def diana2radmc3d(fparticle, fpar, dweights, matdens, ext=None, outdir=None, scatmat=False):
    # translate the opacity files for radmc3d
    # parameters: 
    #   fparticle: list of the file names for particle.dat
    #   fpar: the file name for the parfile.inp
    #   dweights: mass weights for each opacity.
    #   matdens: material density
    #   ext: list of extension names 
    #   outdir: directory for output files
    #   scatmat: bool. whether or not to output the scattering matrix. only False for now
    # outputs: 
    #   dustopac.inp, dustkappa_**.inp, dustinfo.zyl
    from radmc3dPy import dustopac

    # read the data
    if type(fparticle) is str:
        nparticle = 1
        fparticle = [fparticle]
        fpar = [fpar]
    elif type(fparticle) is list:
        nparticle = len(fparticle)
    else:
        raise ValueError('fparticle should be one string or a list of strings')

    dat = []
    par = []
    for ii in range(nparticle):
        datii = readParticle(fparticle[ii])
        parii = readPar(fpar[ii])

        dat.append(datii)
        par.append(parii)

    # set up the extension
    if ext is None:
        ext = range(nparticle)
    if type(ext) is str:
        ext = [ext]
        n_ext = 1
    elif type(ext) is list:
        n_ext = len(ext)
    else:
        raise ValueError('ext should be one string or a list of strings')

    if n_ext != nparticle:
        raise ValueError('extension name setting is not the same as number of particle.dat')

    # set up therm
    therm = [True for ii in range(nparticle)]

    # check dweights
    if dweights.sum() != 1:
        dweights = dweights / dweights.sum()

    # perpare the dustopac
    op = dustopac.radmc3dDustOpac()

    # write master opac
    scatmodemax = 2
    op.writeMasterOpac(ext=ext, therm=therm, scattering_mode_max=scatmodemax,
        old=False, alignment_mode=0, fdir=outdir)

    # write dustinfo.zyl
    gsize = [par[ii]['amax'] for ii in range(nparticle)]
    op.writeDustInfo(ext=ext, matdens=matdens, gsize=gsize,
        dweights=dweights, fdir=outdir)

    for ii in range(nparticle):
        # extension name
        extii = ext[ii]
        op.ext.append(extii)

        # wavlength axis
        wav = dat[ii]['wav']
        nwav = len(wav)
        freq = zylconst.c * 1e4 / wav
        nfreq = nwav

        op.wav.append(wav)
        op.freq.append(freq)
        op.nwav.append(nwav)
        op.nfreq.append(nfreq)

        # opacities
        kabs = dat[ii]['kabs']
        ksca = dat[ii]['ksca']
        phase_g = dat[ii]['phaseg']
        
        op.kabs.append(kabs)
        op.ksca.append(ksca)
        op.phase_g.append(phase_g)

        op.idust.append(ii)

        thermii = 0
        op.therm.append(thermii)

        op.scatmat.append(scatmat)

        # write the opacities
        op.writeOpac(ext=extii, idust=ii, scatmat=scatmat, fdir=outdir)

    return op
