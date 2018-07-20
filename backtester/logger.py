import pandas as pd
def log(msg, verbose ):
    if verbose:
        print(msg)

def logError(msg, verbose=True):
    log('Error: ' + msg, verbose)


def logInfo(msg, verbose=False):
    log('Info: ' + msg, verbose)

def logImportantInfo(msg , verbose = False):
        log('ImportantInfo: '+ msg, verbose)

def logImportantInfoMultiple(*args, verbose = False):
        for x in args:
            log(x, verbose)

def logWarn(msg, verbose=True):
    log('Warn: ' + msg, verbose)


def logPerf(msg, verbose=False):
    log('Perf: ' + msg, verbose)
