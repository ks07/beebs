import string

opt_list = {}

def getOptimisationList(platform):
    """
        This returns a list of optimisations which are valid for the
        compiler for this platform.
    """

    with open("optimisations_"+platform,"r") as f:
        opt_list[platform] = map(string.strip, f.readlines())
        return opt_list[platform]

def createOptimisationString(platform, vals):
    """
        From a list of true/false values, create an command line string
        that can be passed to the compiler, enabling or disabling specific
        optimisations
    """

    opt_base = "-O1"

    for opt, val in zip(opt_list[platform], vals):
        if val:
            opt_base += " " + opt
        else:
            opt_base += " -fno-" + opt[2:]

    return opt_base

