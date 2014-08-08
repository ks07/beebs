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

def avg_bmark_pass(pdict, ndict, bname, pname):
    runs = pdict[pname]
    res = ndict[bname]

    enabled = 0.0;
    disabled = 0.0;
    ecnt = 0;
    dcnt = 0;

    for no, nrg in enumerate(res):
        if nrg == 0.0:
            # Ignore any failed measurements, but show warning
            print('WARNING: ignoring failed benchmark ({} run-{})'.format(bname, no))
        elif no in runs:
            enabled += nrg
            ecnt += 1
        else:
            disabled += nrg
            dcnt += 1

    e_avg = enabled/ecnt
    d_avg = disabled/dcnt
    diff = e_avg - d_avg
    pcnt = diff / d_avg * 100
    print('{},{},{},{},{},{}%'.format(bname,pname,d_avg,e_avg,diff,pcnt))

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
        efiles = glob.glob('energy.csv*')
        for ef in efiles:
            with open(ef, 'r', newline='') as run_energy:
                energyreader = csv.reader(run_energy)
                next(energyreader) #Skip header line
                for erow in energyreader:
                    add_runrg(nrg_dict, bname=erow[0], run_no=rnum, nrg=float(erow[1]))

        os.chdir(basedir)

    #print(pass_dict)
    #print(nrg_dict)

    print('benchmark,pass,MDE,MEE,delta,delta %')
    for b in nrg_dict:
        for p in pass_dict:
            avg_bmark_pass(pass_dict, nrg_dict, b, p)
