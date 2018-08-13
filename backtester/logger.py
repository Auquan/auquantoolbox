def log(msg, verbose):
    if verbose:
        print(msg)


def logError(msg, verbose=True):
    log('Error: ' + msg, verbose)


def logInfo(msg, verbose=False):
    log('Info: ' + msg, verbose)


def logWarn(msg, verbose=True):
    log('Warn: ' + msg, verbose)


def logPerf(msg, verbose=False):
    log('Perf: ' + msg, verbose)
