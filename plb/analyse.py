#!/usr/bin/env python3

from scipy import stats
import os, glob, numpy, csv, sys, re, matplotlib.pyplot as pp

BMARK_EXCLUDE = [
'newlib-log'
]

# SUPPORTED MODES: 'full', 'mat', 'best', 'mwu', 'bpl'
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

    on = []
    off = []

    for no, nrg_reps in enumerate(res):
        for nrg in nrg_reps:
            if nrg == 0.0:
                continue
            elif no in runs:
                on += [nrg]
            else:
                off += [nrg]

    return stats.mannwhitneyu(off, on)

# From SO 16592222
def setBoxColors(bp):
    pp.setp(bp['boxes'][0], color='blue')
    pp.setp(bp['caps'][0], color='blue')
    pp.setp(bp['caps'][1], color='blue')
    pp.setp(bp['whiskers'][0], color='blue')
    pp.setp(bp['whiskers'][1], color='blue')
    pp.setp(bp['fliers'][0], color='blue')
    pp.setp(bp['fliers'][1], color='blue')
    pp.setp(bp['medians'][0], color='blue')

    pp.setp(bp['boxes'][1], color='red')
    pp.setp(bp['caps'][2], color='red')
    pp.setp(bp['caps'][3], color='red')
    pp.setp(bp['whiskers'][2], color='red')
    pp.setp(bp['whiskers'][3], color='red')
    pp.setp(bp['fliers'][2], color='red')
    pp.setp(bp['fliers'][3], color='red')
    pp.setp(bp['medians'][1], color='red')

def boxplot_bmark(pdict, ndict, bname, gyufku):
    res = ndict[bname]

    xticks = []
    xticklabels = []

    y_min = float('inf')
    y_max = 0

    fig = pp.figure(figsize=(14, 6))
    fig.suptitle('Energy for {} (Blue == Enabled)'.format(bname))
    ax = pp.axes()
    pp.hold(True)

    for pname in sorted(pdict):
        # Collect the list of passes and set their respective locations
        xticklabels += [pname]
        xticks += [len(xticklabels) * 3 - 1.5]

        data = ([],[])

        for no, nrg_reps in enumerate(res):
            for nrg in nrg_reps:
                if nrg == 0.0:
                    continue
                elif no in pdict[pname]:
                    data[0].append(nrg)
                else:
                    data[1].append(nrg)

        # Plot the two boxplots for the enabled/disabled pair for this pass
        pos = len(xticklabels) * 3 - 2
        bp = pp.boxplot(data, positions = [pos, pos + 1], widths = 0.6, notch = True, bootstrap = 1000)
        setBoxColors(bp)

        # Adjust axes limits
        y_min = min(min(min(data)), y_min)
        y_max = max(max(max(data)), y_max)

    # Set the boundaries of the graph
    pp.xlim(0, 3 * len(xticklabels))
    pp.ylim(y_min * 0.975, y_max * 1.025)

    # Add pass labels to x axis
    ax.set_xticklabels(xticklabels)
    ax.set_xticks(xticks)

    # Rotate pass labels
    pp.setp(ax.get_xticklabels(), rotation='vertical', fontsize=12)

    # Plot lines for legend where they will definitely be within graph area.
    #hB, = pp.plot([1,y_min],'b-')
    #hR, = pp.plot([1,y_min],'r-')
    #pp.legend((hB, hR), ('E', 'D'), bbox_to_anchor=(1, 1))
    #hB.set_visible(False)
    #hR.set_visible(False)

    pp.subplots_adjust(bottom=0.3)

    #pp.show()
    pp.savefig('boxtest.svg')

def avg_bmark_pass(pdict, ndict, bname, pname):
    runs = pdict[pname]
    res = ndict[bname]

    enabled = 0.0
    disabled = 0.0
    ecnt = 0
    dcnt = 0

    for no, nrg_reps in enumerate(res):
        for nrg in nrg_reps:
            if nrg == 0.0:
                # Ignore any failed measurements, but show warning
                #print('WARNING: ignoring failed benchmark ({} run-{})'.format(bname, no))
                continue
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

    e_sdev_sum = 0.0
    d_sdev_sum = 0.0

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

    if MODE == 'bpl':
        boxplot_bmark(pass_dict, nrg_dict, '2dfir', 'increase_alignment')
    else:
        if MODE == 'full':
            print('benchmark,pass,MDE,DV,MEE,EV,delta,delta %')
        elif MODE == 'mwu':
            print('benchmark,pass,U,p')
        for b in nrg_dict:
            if b in BMARK_EXCLUDE:
                continue

            best_passes = []
            worst_passes = []

            for p in pass_dict:
                if MODE == 'mwu':
                    mw = mw_bmark_pass(pass_dict, nrg_dict, b, p)
                    print('{},{},{},{}'.format(b,p,mw[0],mw[1]))
                else:
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
