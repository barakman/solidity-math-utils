from util import hex_len
from core import AnalyticMath
from constants import FIXED_1
from constants import LOG_MAX_HI_TERM_VAL
from constants import EXP_MAX_HI_TERM_VAL


scaledLn2 = AnalyticMath.scaledLn2(FIXED_1)
optimalLogMax = AnalyticMath.optimalLogMax(FIXED_1,LOG_MAX_HI_TERM_VAL)
optimalExpMax = AnalyticMath.optimalExpMax(FIXED_1,EXP_MAX_HI_TERM_VAL)


LN2_MIN = scaledLn2.__floor__()
LN2_MAX = scaledLn2.__ceil__()
LOG_MID = optimalLogMax+1
EXP_MID = optimalExpMax+1
EXP_MAX = LN2_MAX*(259-len(bin(FIXED_1*2-1)))


maxLen = hex_len(max([FIXED_1,LN2_MIN,LN2_MAX,LOG_MID,EXP_MID,EXP_MAX]))


print(f'    uint256 internal constant FIXED_1 = {FIXED_1:#0{maxLen}x};')
print(f'    uint256 internal constant LN2_MIN = {LN2_MIN:#0{maxLen}x};')
print(f'    uint256 internal constant LN2_MAX = {LN2_MAX:#0{maxLen}x};')
print(f'    uint256 internal constant LOG_MID = {LOG_MID:#0{maxLen}x};')
print(f'    uint256 internal constant EXP_MID = {EXP_MID:#0{maxLen}x};')
print(f'    uint256 internal constant EXP_MAX = {EXP_MAX:#0{maxLen}x};')
