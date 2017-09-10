__version__ = '1.1.7'
import urllib2
import json


def updateCheck():
    ''' checks for new version of toolbox
    Returns:
        returns True if the version of the toolox on PYPI is not the same as the current version
        returns False if version is the same
    '''
    updateStr = ''
    try:
        toolboxJson = urllib2.urlopen('https://pypi.python.org/pypi/auquan_toolbox/json')
    except Exception as e:
        return False

    toolboxDict = json.loads(toolboxJson.read())

    if __version__ != toolboxDict['info']['version']:
        return True
    else:
        return False
