__version__ = '2.1.92'
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import json


def updateCheck():
    ''' checks for new version of toolbox
    Returns:
        returns True if the version of the toolox on PYPI is not the same as the current version
        returns False if version is the same
    '''
    updateStr = ''
    try:
        toolboxJson = urlopen('https://pypi.python.org/pypi/auquan_toolbox/json')
    except Exception as e:
        return False

    toolboxDict = json.loads(toolboxJson.read().decode('utf8'))

    if __version__ != toolboxDict['info']['version']:
        return True
    else:
        return False
