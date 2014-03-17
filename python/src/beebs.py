import subprocess
import os, os.path
import logging
import pexpect

# Set up logging
logger = logging.getLogger(__name__)
info = logger.info
warning = logger.warning

try:
    import platformrun
except ImportError:
    warning("The platformrun module was not found")
    platformrun = None

# Globals
beebs_src = "beebs"
beebs_build = "beebs_build"

# A mapping of platform name to cross compilation triple
platform_to_host = {
    "atmega328p": "avr",
    "stm32f0discovery": "arm-none-eabi",
    "stm32vldiscovery": "arm-none-eabi",
}

# The directories that get build, but are not benchmarks
benchmark_filter = ["template", "platformcode"]

# This exception is raised when a command doesn't perform correctly
class CommandError(RuntimeError):
    pass

# Logging class
class LogWriter(object):
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
    def write(self, msg):
        for s in msg.split('\n'):
            self.logger.log(self.level, s)
    def flush(self):
        pass
    def close(self):
        pass

def getBuildDir(platform):
    beebs_build_abs = os.path.abspath(beebs_build) + "/" + platform
    return beebs_build_abs


def getBenchmarkList(platform):
    """Get a list of benchmark names"""

    bmarks = set(os.listdir(os.path.join(getBuildDir(platform),"src")))
    return bmarks - set(benchmark_filter)


def getBenchmarkExecutable(platform, benchmark):
    """From the name of a benchmark, get the location of its executable"""

    bdir = os.path.join(getBuildDir(platform), "src", benchmark)

    execs = []
    for f in os.listdir(bdir):
        fname = os.path.join(getBuildDir(platform), "src", benchmark, f)
        if os.access(fname, os.X_OK) and os.path.isfile(fname):
            execs.append(fname)
    if len(execs) != 1:
        logger.fatal("More/less than one executable file was found for the benchmark")

    return execs[0]


def initialise(platform):
    initlog = logger.getChild("initialise")

    beebs_src_abs = os.path.abspath(beebs_src)
    beebs_build_abs = getBuildDir(platform)

    initlog.info("Building beebs in {}".format(beebs_build_abs))
    os.system("mkdir -p "+beebs_build_abs)

    out = pexpect.run("{}/configure --with-platform={} --host={}".format(beebs_src_abs, platform, platform_to_host[platform]), cwd=beebs_build_abs, withexitstatus=True, logfile=LogWriter(initlog, logging.DEBUG))
    ret = out[1]

    if ret != 0:
        for l in out[0].split():
            fatal(l)
        raise CommandError("Configure did not execute as expected")

    if platformrun is not None:
        initlog.info("Initialise platformrun")
        platformrun.loadConfiguration()
        platformrun.loadToolConfiguration()
    

def make(platform, benchmarks=None, cflags=""):
    """Make the benchmarks. If benchmarks is None, build all, else this is a list of benchmarks to compile"""

    makelog = logger.getChild("make")
    beebs_build_abs = getBuildDir(platform)

    # First clean the whole of beebs
    makelog.info("Cleaning beebs")
    pexpect.run("make clean", cwd=beebs_build_abs, logfile=LogWriter(makelog, logging.DEBUG))

    # If we build them all, we don't need to enter individual subdirectories
    if benchmarks is None:
        out = pexpect.run("make CFLAGS=\"{}\"".format(cflags), logfile=LogWriter(makelog, logging.DEBUG), withexitstatus=True)
        ret = out[1]

        if ret != 0:
            for l in out[0].split():
                makelog.fatal(l)
            raise CommandError("Make did not success")
    else:
        for b in benchmarks:
            makelog.info("Making benchmark {}".format(b))
            out = pexpect.run("make CFLAGS=\"{}\"".format(cflags), cwd="{}/src/{}".format(beebs_build_abs,b), logfile=LogWriter(makelog, logging.DEBUG), withexitstatus=True)
            ret = out[1]

            if ret != 0:
                for l in out[0].split():
                    makelog.fatal(l)
                raise CommandError("Make did not success")


def run(platform, benchmarks=None, repeats=3):
    """Run the benchmarks. If benchmarks is None, run them all"""

    beebs_build_abs = getBuildDir(platform)

    if benchmarks is None:
        benchmarks = getBenchmarkList(platform)

    if platformrun is None:
        raise RuntimeError("Error platformrun module is not available")

    measurements = {b: [] for b in benchmarks}
    for r in range(repeats):
        for b in benchmarks:
            f =getBenchmarkExecutable(platform,b)
            info("Running benchmark at {}".format(f))
            m = platformrun.run(platform, f)
            print m
            measurements[b].append(m)

    return measurements

if __name__ == "__main__":
    initialise("atmega328p")
    print "Make"
    make("atmega328p")
