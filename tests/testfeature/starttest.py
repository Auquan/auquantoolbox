import test_movAvg
import unittest

if __name__ == '__main__':
	suiteList = []
	suiteList.append(unittest.TestLoader().loadTestsFromTestCase(test_movAvg.TestMovingAvg))
	comboSuite = unittest.TestSuite(suiteList)
	unittest.TextTestRunner(verbosity=2).run(comboSuite)
