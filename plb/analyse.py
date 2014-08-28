#!/usr/bin/env python3

from scipy import stats
import os, glob, numpy, csv, sys, re

BMARK_EXCLUDE = [
'newlib-log'
]

# SUPPORTED MODES: 'full', 'mat', 'best', 'mwu'
MODE = sys.argv[1] if len(sys.argv) > 1 else 'full'

# TODO: Take from test.py
_ROUND1_POSSIBILITIES = [
'inline_param',
'einline',
'early_optimizations',
'copyrename',
'ccp',
'forwprop',
'ealias',
'esra',
'fre',
'copyprop',
'mergephi',
'cddce',
'eipa_sra',
'tailr',
'switchconv',
'ehcleanup',
'profile_estimate',
'local-pure-const',
'fnsplit',
'release_ssa',
'inline_param',
'profile',
'increase_alignment',
'tmipa',
'emutls',
'whole-program',
'profile_estimate',
'devirt',
'cp',
'cdtor',
'inline',
'pure-const',
'static-var',
'pta',
'simdclone',
'ehdisp',
'copyrename',
'ccp',
'copyprop',
'cunrolli',
'phiprop',
'forwprop',
'objsz',
'alias',
'retslot',
'fre',
'copyprop',
'mergephi',
'vrp',
'dce',
'cdce',
'cselim',
'ifcombine',
'phiopt',
'tailr',
'ch',
'stdarg',
'', #cplxlower
'sra',
'copyrename',
'dom',
'isolate-paths',
'phicprop',
'dse',
'reassoc',
'dce',
'forwprop',
'phiopt',
'strlen',
'ccp',
'copyprop',
'sincos',
'bswap',
'crited',
'pre',
'sink',
'', #asan
'', #tsan
'loop',
'loopinit',
'lim',
'copyprop',
'dceloop',
'unswitch',
'sccp',
'ckdd',
'ldist',
'copyprop',
'graphite0',
'ivcanon',
'parloops',
'ifcvt',
'vect',
'dceloop',
'pcom',
'cunroll',
'slp',
'aprefetch',
'ivopts',
'lim',
'loopdone',
'veclower2',
'recip',
'reassoc',
'slsr',
'dom',
'phicprop',
'vrp',
'cddce',
'tracer',
'dse',
'forwprop',
'phiopt',
'fab',
'widening_mul',
'tailc',
'copyrename',
'crited',
'uninit',
'uncprop',
]

# TODO: Update this method in test.py and re-use it
def parse_matrix(path, pass_dict):
    with open(path, 'r') as _inputfile:
        for line in _inputfile:
            test = re.split(' *', line.strip())
            rno = int(test.pop(0))
            for idx, gate in enumerate(test):
                if int(gate) == 1:
                    pname = _ROUND1_POSSIBILITIES[idx]
                    add_runpass(pass_dict, pname, rno)

def add_runrg(ndict, bname, run_no, rpt_no, nrg):
    assert type(nrg) == float
    if bname not in ndict:
        ndict[bname] = numpy.zeros((n_runs, n_repeats))
        assert len(ndict) <= n_benches
    ndict[bname][run_no][rpt_no] = nrg

def add_runpass(pdict, pname, run_no):
    assert type(run_no) == int
    if pname not in pdict:
        pdict[pname] = [run_no]
        assert len(pdict) <= n_opt_passes
    elif run_no not in pdict[pname]:
        pdict[pname] += [run_no]
        assert len(pdict[pname]) <= n_runs + 1 / 2

def mw_bmark_pass(pdict, ndict, bname, pname):
    runs = pdict[pname]
    res = ndict[bname]

#    for no, nrg in enumerate

def avg_bmark_pass(pdict, ndict, bname, pname):
    runs = pdict[pname]
    res = ndict[bname]

    enabled = 0.0;
    disabled = 0.0;
    ecnt = 0;
    dcnt = 0;

    for no, nrg_reps in enumerate(res):
        for nrg in nrg_reps:
            if nrg == 0.0:
                # Ignore any failed measurements, but show warning
                print('WARNING: ignoring failed benchmark ({} run-{})'.format(bname, no))
            elif no in runs:
                enabled += nrg
                ecnt += 1
            else:
                disabled += nrg
                dcnt += 1

    if ecnt <= 0 or dcnt <= 0:
        return (bname,pname,0.0,0.0,0.0,0.0,0.0,0.0)
    e_avg = enabled/ecnt
    d_avg = disabled/dcnt
    diff = e_avg - d_avg
    pcnt = diff / d_avg * 100

    e_sdev_sum = 0.0;
    d_sdev_sum = 0.0;

    # Calculate sample variance
    for no, nrg_reps in enumerate(res):
        for nrg in nrg_reps:
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

    #Sort the list of rundirs to make processing simpler
    rundirs = sorted(glob.glob('./run-[0-9]*'), key=lambda x: int(x.split('-')[-1]))

    n_runs = len(rundirs)
    n_opt_passes = 31 # TODO: Calculate from matrix1
    n_benches = 61 # TODO: Calculate from energy.csv (or src dir)
    n_levels = 2
    n_repeats = 3

    # Store energy for every benchmark for every run
    rshape = [n_runs, n_benches]
    results = numpy.zeros(rshape)

    # Mapping of passes to enabled runs
    pass_dict = {}

    # Mapping of benchmarks to run results
    nrg_dict = {}

    parse_matrix('matrix1', pass_dict)

    # Get passes and energy for each run
    for rd in rundirs:
        rnum = int(rd.split('-')[-1])
        assert rnum < n_runs
        os.chdir(rd)

        # Read passes for this run
        # with open('PASSES_TO_RUN', 'r') as run_passes:
        #     for pline in run_passes:
        #         if pline not in base_passes:
        #             pline = pline.strip()
        #             add_runpass(pass_dict, pline, rnum)

        # Read energy for this run
        efiles = glob.glob('energy.csv.?')
        for i, ef in enumerate(efiles):
            with open(ef, 'r', newline='') as run_energy:
                energyreader = csv.reader(run_energy)
                next(energyreader) #Skip header line
                for erow in energyreader:
                    add_runrg(nrg_dict, bname=erow[0], run_no=rnum, rpt_no=i, nrg=float(erow[1]))

        os.chdir(basedir)

    #print(pass_dict)
    #print(nrg_dict)



    if MODE == 'full':
        print('benchmark,pass,MDE,DV,MEE,EV,delta,delta %')
    for b in nrg_dict:
        if b in BMARK_EXCLUDE:
            continue

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

