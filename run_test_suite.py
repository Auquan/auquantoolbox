import os, sys
try:
    import pytest
except:
    os.system('pip install -U pytest')
try:
    import mock
except:
    os.system('pip install mock')

if __name__ == "__main__":

#### uninstalling the toolbox
    print ('\33[33m')
    print ("***************************************")
    print ("******* UNINSTALLING THE TOOLBOX ******")
    print ("***************************************")
    print ('\033[0m')
    os.system("pip uninstall auquan-toolbox -y")
    print ("\n")

#***********************************************************************************************

    try:
######## for testing a branch of toolbox
        if sys.argv[1] == '-b':
            try:
                print ('\33[31m')
                os.system('pytest '+os.getcwd()+'/tester/'+sys.argv[2]+'_tester')
                print ('\033[0m')
            except:
                print ('\33[91m'+"ERROR:\n"+'\033[0m')
                print ("Specify the Folder correctly to test")
                print ("Try something like:  python run_test_suite.py -b timeRule  \n")

######## for testing a specific file in the toolbox
        elif sys.argv[1] == '-f':
            try:
                flag=0
                for root, dirs, files in os.walk(os.getcwd()):
                    if ('test_' + sys.argv[2]) in files:
                        os.system("pytest -s "+root)
                        flag=1
                if flag==0:
                    raise IndexError
            except IndexError:
                print ('\33[91m'+"ERROR:\n"+'\033[0m')
                print ("Specify the File correctly to test")
                print ("Try something like:  python run_test_suite.py -f data_source.py  \n")

#### for testing everyfile in the toolbox
        elif sys.argv[1] == '-a':
            print ('\33[31m')
            os.system("pytest")
            print ('\033[0m')

        else:
            print ('\33[91m'+"ERROR:\n"+'\033[0m')
            print ("Try -b for branch testing or -f for file testing")

#### help
    except:
        print ("\n\n")
        print ('COMMAND         FUNCTION                                    SAMPLE CODE')
        print ("\n")
        print ('-a              to run all the tests                        python run_test_suite.py -a')
        print ("-f <fileName>   to run test for a specific file             python run_test_suite.py -f data_source.py")
        print ("-b <folderName> to run all the tests for a specific folder  python run_test_suite.py -b timeRule")
        print ("\n\n")

#***********************************************************************************************

####installing auquantoolbox
    print ("\n")
    print ('\33[33m')
    print ("***************************************")
    print ("******** INSTALLING THE TOOLBOX *******")
    print ("***************************************")
    print ('\033[0m')
    os.system("pip install auquan-toolbox")
