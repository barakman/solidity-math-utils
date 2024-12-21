from util import dec_str
from util import hex_str
from core import AnalyticMath
from constants import FIXED_1
from constants import LOG_MAX_HI_TERM_VAL
from constants import LOG_NUM_OF_HI_TERMS


hiTerms,loTerms = AnalyticMath.optimalLogTerms(FIXED_1,LOG_MAX_HI_TERM_VAL,LOG_NUM_OF_HI_TERMS)


hiTermIndexMax = LOG_MAX_HI_TERM_VAL-1
hiTermIndexMin = LOG_MAX_HI_TERM_VAL-LOG_NUM_OF_HI_TERMS
hiTermIndexLen = max(len(str(hiTermIndexMin)),len(str(hiTermIndexMax)))


print('    function optimalLog(uint256 x) internal pure returns (uint256) { unchecked {')
print('        uint256 res = 0;')
print('')
print('        uint256 y;')
print('        uint256 z;')
print('        uint256 w;')
print('')
for n in range(len(hiTerms)):
    str0 = hex_str(hiTerms[n].exp,hiTerms[+0].exp)
    str1 = hex_str(hiTerms[n].bit,hiTerms[+0].bit)
    str2 = hex_str(hiTerms[n].num,hiTerms[-1].num)
    str3 = hex_str(hiTerms[n].den,hiTerms[-1].den)
    str4 = '{0:+{1}d}'.format(hiTermIndexMax-n,hiTermIndexLen)
    print('        if (x > {}) {{res |= {}; x = x * {} / {};}} // add 2^({})'.format(str0,str1,str2,str3,str4))
print('')
print('        z = y = x - FIXED_1;')
print('        w = y * y / FIXED_1;')
for n in range(len(loTerms)):
    str5 = hex_str(loTerms[n].num,loTerms[+0].num)
    str6 = hex_str(loTerms[n].den,loTerms[-1].den)
    str7 = dec_str(2*n+1,len(loTerms)*2-1)
    str8 = dec_str(2*n+2,len(loTerms)*2-0)
    str9 = ''.join([[c,' '][(n+1)//len(loTerms)] for c in 'z = z * w / FIXED_1;'])
    print('        res += z * ({} - y) / {}; {} // add y^{} / {} - y^{} / {}'.format(str5,str6,str9,str7,str7,str8,str8))
print('')
print('        return res;')
print('    }}')
