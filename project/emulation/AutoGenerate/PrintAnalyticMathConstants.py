from common import Decimal
from common.constants import FIXED_1
from common.functions import optimalLogTerms
from common.functions import optimalExpTerms


FIXED_LN2 = FIXED_1*Decimal(2).ln()


LN2_MIN = FIXED_LN2.__floor__()
LN2_MAX = FIXED_LN2.__ceil__()
LOG_MID = optimalLogTerms()[0][ 0].exp
EXP_MID = optimalExpTerms()[0][-1].bit//2
EXP_MAX = LN2_MAX*(259-len(bin(FIXED_1*2-1)))


maxLen = len(hex(max([FIXED_1,LN2_MIN,LN2_MAX,LOG_MID,EXP_MID,EXP_MAX])))


print(f'    uint256 internal constant FIXED_1 = {FIXED_1:#0{maxLen}x};')
print(f'    uint256 internal constant LN2_MIN = {LN2_MIN:#0{maxLen}x};')
print(f'    uint256 internal constant LN2_MAX = {LN2_MAX:#0{maxLen}x};')
print(f'    uint256 internal constant LOG_MID = {LOG_MID:#0{maxLen}x};')
print(f'    uint256 internal constant EXP_MID = {EXP_MID:#0{maxLen}x};')
print(f'    uint256 internal constant EXP_MAX = {EXP_MAX:#0{maxLen}x};')
