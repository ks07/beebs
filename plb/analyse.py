#!/usr/bin/env python3

import os, glob, numpy, csv, sys

# SUPPORTED MODES: 'full', 'mat', 'best'
MODE = sys.argv[1] if len(sys.argv) > 1 else 'full'

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

    e_sdev_sum = 0.0;
    d_sdev_sum = 0.0;

    # Calculate sample variance
    for no, nrg in enumerate(res):
        if nrg == 0.0:
            # Silently ignore
            continue
        elif no in runs:
            # Get the sum of deviations
            e_sdev_sum += (nrg - e_avg)**2
        else:
            d_sdev_sum += (nrg - d_avg)**2

    e_var = e_sdev_sum / (ecnt - 1)
    d_var = d_sdev_sum / (dcnt - 1)

    return (bname,pname,d_avg,d_var,e_avg,e_var,diff,pcnt)
    #print('{},{},{},{},{},{},{},{}%'.format(bname,pname,d_avg,d_var,e_avg,e_var,diff,pcnt))

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



    if MODE == 'full':
        print('benchmark,pass,MDE,DV,MEE,EV,delta,delta %')
    for b in nrg_dict:
        best_passes = []
        worst_passes = []

        for p in pass_dict:
            bp_info = avg_bmark_pass(pass_dict, nrg_dict, b, p)

            best_passes += [(p, bp_info[7])]
            worst_passes += [(p, bp_info[7])]
            if len(best_passes) > 3:
                # Negative values are better, hence use max
                low = max(best_passes, key=lambda x: x[1])
                best_passes.remove(low)
            if len(worst_passes) > 3:
                hi = min(worst_passes, key=lambda x: x[1])
                worst_passes.remove(hi)

            if MODE == 'mat':
                print('{}\t{}\t{}'.format(bp_info[0], bp_info[1], bp_info[7]))
            elif MODE == 'full':
                print('{},{},{},{},{},{},{},{}%'.format(*bp_info))

        if MODE == 'best':
            best_passes = sorted(best_passes, key=lambda x: x[1])
            worst_passes = sorted(worst_passes, key=lambda x: x[1])
            print('{};{};{};{};...;{};{};{}'.format(*([b] + best_passes + worst_passes)))

