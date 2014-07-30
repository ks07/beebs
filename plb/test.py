#!/usr/bin/env python2
# MAGEEC Testing Script
# (C) Embecosm and University of Bristol 2014
# Contributor: Simon Cook <simon.cook@embecosm.com>
# This is GPL (FIXME: ADD HEADER)
# Note: Doesn't (yet) support automatic resuming

import subprocess, sys, os, re

# Size of our matrix
_ENTRIES=120

# Index for resuming
_startfrom = 0

# Passes to always run
# (some of these are important and needed each time)
_PASSES_ALWAYS="""*warn_unused_result
*omplower
lower
eh
cfg
*warn_function_return
*build_cgraph_edges
*free_lang_data
visibility
early_local_cleanups
*free_cfg_annotations
*init_datastrucutres
ssa
mageec-extractor
*all_optimizations
*clean_state
*rebuild_cgraph_edges
*remove_cgraph_callee_edges
*rebuild_cgraph_edges
*free_inline_summary
*free_cfg_annotations
*all_optimizations
*remove_cgraph_callee_edges
*strip_predict_hints
*record_bounds
*rest_of_compilation
*stack_ptr_mod
*all-postreload
*leaf_regs
*free_cfg
veclower
inline_param
cplxlower
"""

# This array should have ENTRIES elements
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

# This string uses the left over tests that we want to run.
_ROUND1_EXTRAS = """local-pure-const
nrv
optimized
expand
vregs
into_cfglayout
jump
subreg1
dfinit
cse1
fwprop1
cprop
rtl pre
cprop
ce1
reginfo
loop2
loop2_init
loop2_invariant
loop2_unswitch
loop2_done
cprop
cse2
dse1
fwprop2
auto_inc_dec
init-regs
ud_dce
combine
ce2
outof_cfglayout
split1
subreg2
asmcons
ira
reload
postreload
gcse2
split2
pro_and_epilogue
dse2
csa
jump2
peephole2
ce3
cprop_hardreg
rtl_dce
compgotos
bbro
alignments
mach
barriers
split5
shorten
nothrow
final
dfinish
"""

STARTDIR = os.getcwd()
_inputfile = open('matrix1','r')

# We use this as a guard to prevent accidental execution of test-pt2, so
# set this here.
os.environ['INMAGEEC'] = "TRUE"

if len(_ROUND1_POSSIBILITIES) != _ENTRIES:
  sys.stderr.write("Entries != Possibilities\n")
  sys.exit(1)

for line in _inputfile:
  test = re.split(' *', line)
  print ' * Running test set %s' % test[0]
  if int(test[0]) < _startfrom:
    continue
  os.mkdir(STARTDIR + '/run-' + test[0])
  os.chdir(STARTDIR + '/run-' + test[0])
  testlist = open('PASSES_TO_RUN','w')
  testlist.write(_PASSES_ALWAYS)
  lower = min(_ENTRIES, len(test))
  if len(test) != _ENTRIES:
    sys.stderr.write("WARNING: test != Entries\n")
  for i in xrange(1, lower):
    if test[i] == '1':
      testlist.write(_ROUND1_POSSIBILITIES[i-1])
      testlist.write('\n')
  testlist.write(_ROUND1_EXTRAS)
  testlist.close()

  # Execute
  proc = subprocess.call(['tsp', STARTDIR + '/test-pt2.sh', test[0]])


