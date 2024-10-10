from util import dec_str
from util import hex_str
from core import AnalyticMath
from constants import FIXED_1
from constants import EXP_MAX_HI_TERM_VAL
from constants import EXP_NUM_OF_HI_TERMS


hiTerms,loTerms = AnalyticMath.optimalExpTerms(FIXED_1,EXP_MAX_HI_TERM_VAL,EXP_NUM_OF_HI_TERMS)


hiTermIndexMax = EXP_MAX_HI_TERM_VAL-1
hiTermIndexMin = EXP_MAX_HI_TERM_VAL-EXP_NUM_OF_HI_TERMS
hiTermIndexLen = max(len(str(hiTermIndexMin)),len(str(hiTermIndexMax)))


str0 = hex_str(hiTerms[0].bit,hiTerms[0].bit)
str1 = hex_str(loTerms[0].val,loTerms[0].val)


print('    function optimalExp(uint256 x) internal pure returns (uint256) { unchecked {')
print('        uint256 res = 0;')
print('')
print('        uint256 y;')
print('        uint256 z;')
print('')
print('        z = y = x % {}; // get the input modulo 2^({:+d})'.format(str0,hiTermIndexMin))
for n in range(1,len(loTerms)):
    str2 = hex_str(loTerms[n].val,loTerms[+1].val)
    str3 = dec_str(loTerms[n].ind,loTerms[-1].ind)
    print('        z = z * y / FIXED_1; res += z * {}; // add y^{} * ({}! / {}!)'.format(str2,str3,len(loTerms),str3))
print('        res = res / {} + y + FIXED_1; // divide by {}! and then add y^1 / 1! + y^0 / 0!'.format(str1,len(loTerms)))
print('')
for n in range(len(hiTerms)-1):
    str4 = hex_str(hiTerms[n].bit,hiTerms[-1].bit)
    str5 = hex_str(hiTerms[n].num,hiTerms[+0].num)
    str6 = hex_str(hiTerms[n].den,hiTerms[+0].den)
    str7 = '{0:+{1}d}'.format(hiTermIndexMin+n,hiTermIndexLen)
    print('        if ((x & {}) != 0) res = res * {} / {}; // multiply by e^2^({})'.format(str4,str5,str6,str7))
print('')
print('        return res;')
print('    }}')
