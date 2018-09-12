import pytest
import os, sys
os.chdir (os.getcwd()+'/testds')
pytest.main()
os.chdir (os.getcwd()+'/../testtime')
pytest.main()
os.chdir (os.getcwd()+'/../testexec')
pytest.main()
os.chdir (os.getcwd()+'/../testfeature')
pytest.main()
