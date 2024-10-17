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
    str0 = hex_str(hiTerms[n].num,hiTerms[-1].num)
    str1 = hex_str(hiTerms[n].den,hiTerms[-1].den)
    str2 = hex_str(hiTerms[n].bit,hiTerms[+0].bit)
    str3 = '{0:+{1}d}'.format(hiTermIndexMax-n,hiTermIndexLen)
    print('        if (x * {} >= {} * FIXED_1) {{x = x * {} / {}; res |= {};}} // add 2^({})'.format(str0,str1,str0,str1,str2,str3))
print('')
print('        z = y = x - FIXED_1;')
print('        w = y * y / FIXED_1;')
for n in range(len(loTerms)):
    str2 = hex_str(loTerms[n].num,loTerms[+0].num)
    str3 = hex_str(loTerms[n].den,loTerms[-1].den)
    str4 = dec_str(2*n+1,len(loTerms)*2-1)
    str5 = dec_str(2*n+2,len(loTerms)*2-0)
    str6 = ''.join([[c,' '][(n+1)//len(loTerms)] for c in 'z = z * w / FIXED_1;'])
    print('        res += z * ({} - y) / {}; {} // add y^{} / {} - y^{} / {}'.format(str2,str3,str6,str4,str4,str5,str5))
print('')
print('        return res;')
print('    }}')
