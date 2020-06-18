import numpy as np
import pandas as pd
import glob
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from astropy.coordinates import SkyCoord
from astropy.table import Table
from astropy import units as u
import time
import itertools
import progressbar
import os
import pickle
import scipy.stats as stats
import scipy.special as sf
import scipy.integrate as integrate
import scipy.interpolate as interpolate
import confuse
import argparse
from des_mismatch.simulations.sim import Sim,ZPowerCosmoSchechterSim
from des_mismatch.functions import features, match
from des_mismatch.utils.utils import Constants

def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--pop',help='Type of galaxy population to sample: [ZPowerCosmoSchechter]',default='ZPowerCosmoSchechter')
    parser.add_argument('--Lstar',help='Schechter L*',dest='Luminosity.Schechter.Lstar',required=False)
    parser.add_argument('--alpha',help='Schechter alpha',dest='Luminosity.Schechter.alpha',required=False)
    parser.add_argument('--r_max',help='Max distance or redshift to sample',dest='Spatial.r_max',required=False)
    parser.add_argument('--Lambda',help='Reference to spatial density of galaxies/SNe: [D08_z]',dest='Spatial.Lambda',required=False)
    parser.add_argument('--delta',help='Exponent of redshift evolution of spatial distribution',dest='Spatial.cosmo.delta',required=False)
    args = parser.parse_args()

def main():
    c = Constants()
    args = parser()
    config = confuse.Configuration('des_mismatch')
    config.set_args(args,dots=True)
    sim = ZPowerCosmoSchechterSim(
        Lstar=config['Luminosity']['Schechter']['Lstar'].get(float)*c.Lsun,
        alpha=config['Luminosity']['Schechter']['alpha'].get(float)+1,
        Lambda=getattr(c,config['Spatial']['Lambda'].get(str)),
        delta=config['Spatial']['cosmo']['delta'].get(float),
        r_max=config['Spatial']['r_max'].get(float))
    sim.pop_df = sim.synth_pop()
    sim.plot_pop()
if __name__=="__main__":
    main()
