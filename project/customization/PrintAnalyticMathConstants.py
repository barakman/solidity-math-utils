from util import len_hex
from core import AnalyticMath
from constants import FIXED_1
from constants import LOG_MAX_HI_TERM_VAL
from constants import LOG_NUM_OF_HI_TERMS
from constants import EXP_MAX_HI_TERM_VAL
from constants import EXP_NUM_OF_HI_TERMS


scaledLn2 = AnalyticMath.scaledLn2(FIXED_1)
optimalLogTerms = AnalyticMath.optimalLogTerms(FIXED_1,LOG_MAX_HI_TERM_VAL,LOG_NUM_OF_HI_TERMS)
optimalExpTerms = AnalyticMath.optimalExpTerms(FIXED_1,EXP_MAX_HI_TERM_VAL,EXP_NUM_OF_HI_TERMS)


LN2_MIN = scaledLn2.__floor__()
LN2_MAX = scaledLn2.__ceil__()
LOG_MID = optimalLogTerms[0][ 0].exp
EXP_MID = optimalExpTerms[0][-1].bit//2
EXP_MAX = LN2_MAX*(259-len(bin(FIXED_1*2-1)))


maxLen = len_hex(max([FIXED_1,LN2_MIN,LN2_MAX,LOG_MID,EXP_MID,EXP_MAX]))


print(f'    uint256 internal constant FIXED_1 = {FIXED_1:#0{maxLen}x};')
print(f'    uint256 internal constant LN2_MIN = {LN2_MIN:#0{maxLen}x};')
print(f'    uint256 internal constant LN2_MAX = {LN2_MAX:#0{maxLen}x};')
print(f'    uint256 internal constant LOG_MID = {LOG_MID:#0{maxLen}x};')
print(f'    uint256 internal constant EXP_MID = {EXP_MID:#0{maxLen}x};')
print(f'    uint256 internal constant EXP_MAX = {EXP_MAX:#0{maxLen}x};')
