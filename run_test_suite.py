import os, sys
try:
    import pytest
except:
    os.system('pip3 install pytest')
try:
    import mock
except:
    os.system('pip3 install mock')

if __name__ == "__main__":

    def help():
        print ("\n")
        print ('COMMAND         FUNCTION                                    SAMPLE CODE')
        print ("\n")
        print ('-a              to run all the tests                        python3 run_test_suite.py -a')
        print ("-f <fileName>   to run test for a specific file             python3 run_test_suite.py -f data_source.py")
        print ("-b <folderName> to run all the tests for a specific folder  python3 run_test_suite.py -b timeRule")

#### uninstalling the toolbox
    print ('\33[33m')
    print ("***************************************")
    print ("******* UNINSTALLING THE TOOLBOX ******")
    print ("***************************************")
    print ('\033[0m')
    os.system("pip3 uninstall auquan-toolbox -y")
    print ("\n")

#***********************************************************************************************

    try:
######## for testing a branch of toolbox
        if sys.argv[1] == '-b':
            try:
                print ('\33[31m')
                os.system('python3 -m pytest -x -v '+os.getcwd()+'/tester/'+sys.argv[2]+'_tester')
                print ('\033[0m')
            except:
                print ('\33[91m'+"ERROR\n"+'\033[0m')
                help()

######## for testing a specific file in the toolbox
        elif sys.argv[1] == '-f':
            try:
                flag=0
                for root, dirs, files in os.walk(os.getcwd()):
                    if ('test_' + sys.argv[2]) in files:
                        os.system("python3 -m pytest -s "+root)
                        flag=1
                if flag==0:
                    raise IndexError
            except IndexError:
                print ('\33[91m'+"ERROR\n"+'\033[0m')
                help()

#### for testing everyfile in the toolbox
        elif sys.argv[1] == '-a':
            print ('\33[31m')
            os.system("python3 -m pytest -x -v")
            print ('\033[0m')

        else:
            print ('\33[91m'+"ERROR\n"+'\033[0m')
            help()

#### help
    except:
        print ("\n\n")
        print ('\33[91m'+"ERROR\n"+'\033[0m')
        help()
        print ("\n\n")

#***********************************************************************************************

####installing auquantoolbox
    print ("\n")
    print ('\33[33m')
    print ("***************************************")
    print ("******** INSTALLING THE TOOLBOX *******")
    print ("***************************************")
    print ('\033[0m')
    os.system("pip3 install auquan-toolbox")
