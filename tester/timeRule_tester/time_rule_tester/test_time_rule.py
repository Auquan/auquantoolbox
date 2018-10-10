import os,sys,shutil,pytest
sys.path.append(os.path.abspath('../../..'))
from backtester.timeRule.time_rule import TimeRule
def test_time_rule():
    timerule=TimeRule()
    with pytest.raises(NotImplementedError):
        TimeRule.emitTimeToTrade(timerule)
