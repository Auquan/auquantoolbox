import pytest
import os, sys
try:
    os.system ("pip uninstall auquan-toolbox")
except:
    pass
os.chdir (os.getcwd()+'/tests/testds')
pytest.main()
os.chdir (os.getcwd()+'/../testtime')
pytest.main()
os.chdir (os.getcwd()+'/../testexec')
pytest.main()
os.chdir (os.getcwd()+'/../testfeature')
pytest.main()
os.system ("pip install auquan-toolbox")
