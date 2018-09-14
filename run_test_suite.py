import pytest
import os, sys

if __name__ == "__main__":
    print ('\33[33m')
    print ("***************************************")
    print ("******* UNINSTALLING THE TOOLBOX ******")
    print ("***************************************")
    print ('\033[0m')
    os.system("yes | pip uninstall auquan-toolbox")
    print ("\n\n\n")
    try:
        if sys.argv[1] == '-b':
            try:
                os.chdir(os.getcwd()+'/tester/'+sys.argv[2]+'_tester')
                print ('\33[32m')
                os.system("py.test")
            except:
                print ('\33[91m'+"ERROR:\n"+'\033[0m')
                print ("Specify the Folder correctly to test")
                print ("Try something like:  python run_test_suite.py -b timeRule  \n")
        elif sys.argv[1] == '-f':
            try:
                flag=0
                for root, dirs, files in os.walk(os.getcwd()):
                    if ('test_' + sys.argv[2]) in files:
                        os.chdir(root)
                        print ('\33[32m')
                        os.system("py.test " + ('test_'+sys.argv[2]))
                        flag=1
                if flag==0:
                    raise IndexError
            except IndexError:
                print ('\33[91m'+"ERROR:\n"+'\033[0m')
                print ("Specify the File correctly to test")
                print ("Try something like:  python run_test_suite.py -f data_source.py  \n")
        else:
            print ('\33[91m'+"ERROR:\n"+'\033[0m')
            print ("Try -b for branch testing or -f for file testing")
    except:
        list_of_folders=os.listdir(os.getcwd()+"/tester/")
        current_path=os.getcwd()
        for i in list_of_folders:
            os.chdir(current_path+'/tester/'+i)
            print ('\33[32m')
            os.system("py.test")
    print ("\n\n\n")
    print ('\33[33m')
    print ("***************************************")
    print ("******** INSTALLING THE TOOLBOX *******")
    print ("***************************************")
    print ('\033[0m')
    os.system("pip install auquan-toolbox")
