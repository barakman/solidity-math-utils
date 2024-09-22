from util import dec_str
from util import hex_str
from core import AnalyticMath
from constants import FIXED_1
from constants import LOG_MAX_HI_TERM_VAL
from constants import LOG_NUM_OF_HI_TERMS


hiTerms,loTerms = AnalyticMath.optimalLogTerms(FIXED_1,LOG_MAX_HI_TERM_VAL,LOG_NUM_OF_HI_TERMS)


hiTermMinIndex = LOG_MAX_HI_TERM_VAL-LOG_NUM_OF_HI_TERMS
hiTermMaxIndex = LOG_MAX_HI_TERM_VAL-1


print('    function optimalLog(uint256 x) internal pure returns (uint256) { unchecked {')
print('        uint256 res = 0;')
print('')
print('        uint256 y;')
print('        uint256 z;')
print('        uint256 w;')
print('')
for n in range(1,len(hiTerms)):
    str0 = hex_str(hiTerms[n].exp,hiTerms[+1].exp)
    str1 = hex_str(hiTerms[n].val,hiTerms[+1].val)
    str2 = '{0:+{1}d}'.format(hiTermMaxIndex-n+1,max(len(str(hiTermMinIndex)),len(str(hiTermMaxIndex))))
    print('        if (x >= {}) {{res |= {}; x = x * FIXED_1 / {};}} // add 2^({})'.format(str0,str1,str0,str2))
print('')
print('        z = y = x - FIXED_1;')
print('        w = y * y / FIXED_1;')
for n in range(len(loTerms)):
    str3 = hex_str(loTerms[n].num,loTerms[+0].num)
    str4 = hex_str(loTerms[n].den,loTerms[-1].den)
    str5 = dec_str(2*n+1,len(loTerms)*2-1)
    str6 = dec_str(2*n+2,len(loTerms)*2-0)
    str7 = ''.join([[c,' '][(n+1)//len(loTerms)] for c in 'z = z * w / FIXED_1;'])
    print('        res += z * ({} - y) / {}; {} // add y^{} / {} - y^{} / {}'.format(str3,str4,str7,str5,str5,str6,str6))
print('')
print('        return res;')
print('    }}')
