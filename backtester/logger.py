import pandas as pd
def log(msg, verbose = False ):
    if verbose:
        print(msg)

def logError(msg, verbose=True):
    log('Error: ' + msg, verbose)


def logInfo(msg, verbose=False):
    log('Info: ' + msg, verbose)

def logImportantInfo(msg , verbose = True):
        log('ImportantInfo: '+ msg, verbose)

def logImportantInfoMultiple(*args, **kwargs):
        for x in args:
            log(x, kwargs.pop('verbose', None))

def logWarn(msg, verbose=True):
    log('Warn: ' + msg, verbose)


def logPerf(msg, verbose=False):
    log('Perf: ' + msg, verbose)
