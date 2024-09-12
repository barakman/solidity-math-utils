from util import len_str
from util import len_hex
from core import AnalyticMath
from constants import FIXED_1
from constants import LOG_MAX_HI_TERM_VAL
from constants import LOG_NUM_OF_HI_TERMS


hiTerms,loTerms = AnalyticMath.optimalLogTerms(FIXED_1,LOG_MAX_HI_TERM_VAL,LOG_NUM_OF_HI_TERMS)


hiTermValMaxLen = len_hex(hiTerms[+1].val)
hiTermExpMaxLen = len_hex(hiTerms[+1].exp)
loTermNumMaxLen = len_hex(loTerms[+0].num)
loTermDenMaxLen = len_hex(loTerms[-1].den)


hiTermIndMaxLen = len_str(len(hiTerms)*1-1)
loTermPosMaxLen = len_str(len(loTerms)*2-1)
loTermNegMaxLen = len_str(len(loTerms)*2-0)


print('    function optimalLog(uint256 x) internal pure returns (uint256) { unchecked {')
print('        uint256 res = 0;')
print('')
print('        uint256 y;')
print('        uint256 z;')
print('        uint256 w;')
print('')
for n in range(1,len(hiTerms)):
    str0 = '{0:#0{1}x}'.format(hiTerms[n].exp,hiTermExpMaxLen)
    str1 = '{0:#0{1}x}'.format(hiTerms[n].val,hiTermValMaxLen)
    str2 = '{0:0{1}d}' .format(n             ,hiTermIndMaxLen)
    print('        if (x >= {}) {{res += {}; x = x * FIXED_1 / {};}} // add {} / 2^{}'.format(str0,str1,str0,LOG_MAX_HI_TERM_VAL,str2))
print('')
print('        z = y = x - FIXED_1;')
print('        w = y * y / FIXED_1;')
for n in range(len(loTerms)):
    str3 = '{0:#0{1}x}'.format(loTerms[n].num,loTermNumMaxLen)
    str4 = '{0:#0{1}x}'.format(loTerms[n].den,loTermDenMaxLen)
    str5 = '{0:0{1}d}' .format(2*n+1         ,loTermPosMaxLen)
    str6 = '{0:0{1}d}' .format(2*n+2         ,loTermNegMaxLen)
    str7 = ''.join([[c,' '][(n+1)//len(loTerms)] for c in 'z = z * w / FIXED_1;'])
    print('        res += z * ({} - y) / {}; {} // add y^{} / {} - y^{} / {}'.format(str3,str4,str7,str5,str5,str6,str6))
print('')
print('        return res;')
print('    }}')
