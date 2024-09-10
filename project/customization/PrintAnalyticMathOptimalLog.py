from core import AnalyticMath
from constants import FIXED_1
from constants import LOG_MAX_HI_TERM_VAL
from constants import LOG_NUM_OF_HI_TERMS


hiTerms,loTerms = AnalyticMath.optimalLogTerms(FIXED_1,LOG_MAX_HI_TERM_VAL,LOG_NUM_OF_HI_TERMS)


hiTermValMaxLen = len(hex(hiTerms[+1].val))
hiTermExpMaxLen = len(hex(hiTerms[+1].exp))
loTermNumMaxLen = len(hex(loTerms[+0].num))
loTermDenMaxLen = len(hex(loTerms[-1].den))


hiTermIndMaxLen = len(str(len(hiTerms)*1-1))
loTermPosMaxLen = len(str(len(loTerms)*2-1))
loTermNegMaxLen = len(str(len(loTerms)*2-0))


print('    function optimalLog(uint256 x) internal pure returns (uint256) { unchecked {')
print('        uint256 res = 0;')
print('')
print('        uint256 y;')
print('        uint256 z;')
print('        uint256 w;')
print('')
for n in range(1,len(hiTerms)):
    str1 = '{0:#0{1}x}'.format(hiTerms[n].exp,hiTermExpMaxLen)
    str2 = '{0:#0{1}x}'.format(hiTerms[n].val,hiTermValMaxLen)
    str3 = '{0:0{1}d}' .format(n             ,hiTermIndMaxLen)
    print('        if (x >= {}) {{res += {}; x = x * FIXED_1 / {};}} // add {} / 2^{}'.format(str1,str2,str1,LOG_MAX_HI_TERM_VAL,str3))
print('')
print('        z = y = x - FIXED_1;')
print('        w = y * y / FIXED_1;')
for n in range(len(loTerms)-1):
    str1 = '{0:#0{1}x}'.format(loTerms[n].num,loTermNumMaxLen)
    str2 = '{0:#0{1}x}'.format(loTerms[n].den,loTermDenMaxLen)
    str3 = '{0:0{1}d}' .format(2*n+1         ,loTermPosMaxLen)
    str4 = '{0:0{1}d}' .format(2*n+2         ,loTermNegMaxLen)
    print('        res += z * ({} - y) / {}; z = z * w / FIXED_1; // add y^{} / {} - y^{} / {}'.format(str1,str2,str3,str3,str4,str4))
for n in range(len(loTerms)-1,len(loTerms)):
    str1 = '{0:#0{1}x}'.format(loTerms[n].num,loTermNumMaxLen)
    str2 = '{0:#0{1}x}'.format(loTerms[n].den,loTermDenMaxLen)
    str3 = '{0:0{1}d}' .format(2*n+1         ,loTermPosMaxLen)
    str4 = '{0:0{1}d}' .format(2*n+2         ,loTermNegMaxLen)
    print('        res += z * ({} - y) / {};                      // add y^{} / {} - y^{} / {}'.format(str1,str2,str3,str3,str4,str4))
print('')
print('        return res;')
print('    }}')
