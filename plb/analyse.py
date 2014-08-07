#!/usr/bin/env python3

import os, glob, numpy, csv

def add_runrg(ndict, bname, run_no, nrg):
    assert type(nrg) == float
    if bname not in ndict:
        ndict[bname] = numpy.zeros([n_runs])
        assert len(ndict) <= n_benches
    ndict[bname][run_no] = nrg

def add_runpass(pdict, pname, run_no):
    assert type(run_no) == int
    if pname not in pdict:
        pdict[pname] = [run_no]
        assert len(pdict) <= n_opt_passes
    else:
        pdict[pname] += [run_no]
        assert len(pdict[pname]) <= n_runs / 2

if __name__ == '__main__':
    basedir = os.getcwd()

    # Read the base passes to work out which optional passes we are working on
    base_passes = set()
    basefile = open('base_passes.txt', 'r')
    for pline in basefile:
        base_passes.add(pline)

    basefile.close()

    #Sort the list of rundirs to make processing simpler
    rundirs = sorted(glob.glob('./run-[0-9]*'), key=lambda x: int(x.split('-')[-1]))

    n_runs = len(rundirs)
    n_opt_passes = 12 # TODO: Calculate from matrix1
    n_benches = 74 # TODO: Calculate from energy.csv (or src dir)
    n_levels = 2

    # Store energy for every benchmark for every run
    rshape = [n_runs, n_benches]
    results = numpy.zeros(rshape)

    # Mapping of passes to enabled runs
    pass_dict = {}

    # Mapping of benchmarks to run results
    nrg_dict = {}


    # Get passes and energy for each run
    for rd in rundirs:
        rnum = int(rd.split('-')[-1])
        assert rnum < n_runs
        os.chdir(rd)

        # Read passes for this run
        with open('PASSES_TO_RUN', 'r') as run_passes:
            for pline in run_passes:
                if pline not in base_passes:
                    pline = pline.strip()
                    add_runpass(pass_dict, pline, rnum)

        # Read energy for this run
        with open('energy.csv', 'r', newline='') as run_energy:
            energyreader = csv.reader(run_energy)
            next(energyreader) #Skip header line
            for erow in energyreader:
                add_runrg(nrg_dict, bname=erow[0], run_no=rnum, nrg=float(erow[1]))

        os.chdir(basedir)

    print(pass_dict)
    print(nrg_dict)
