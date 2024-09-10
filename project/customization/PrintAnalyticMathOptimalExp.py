from core import AnalyticMath
from constants import FIXED_1
from constants import EXP_MAX_HI_TERM_VAL
from constants import EXP_NUM_OF_HI_TERMS


hiTerms,loTerms = AnalyticMath.optimalExpTerms(FIXED_1,EXP_MAX_HI_TERM_VAL,EXP_NUM_OF_HI_TERMS)


hiTermBitMaxLen = len(hex(hiTerms[-1].bit))
hiTermNumMaxLen = len(hex(hiTerms[+0].num))
hiTermDenMaxLen = len(hex(hiTerms[+0].den))
loTermValMaxLen = len(hex(loTerms[+1].val))
loTermIndMaxLen = len(str(loTerms[-1].ind))


hiTermIndMin    = EXP_MAX_HI_TERM_VAL-EXP_NUM_OF_HI_TERMS
hiTermIndMaxLen = max(len(str(EXP_MAX_HI_TERM_VAL-1)),len(str(EXP_MAX_HI_TERM_VAL-EXP_NUM_OF_HI_TERMS)))


print('    function optimalExp(uint256 x) internal pure returns (uint256) { unchecked {')
print('        uint256 res = 0;')
print('')
print('        uint256 y;')
print('        uint256 z;')
print('')
print('        z = y = x % 0x{:x}; // get the input modulo 2^({:+d})'.format(hiTerms[0].bit,EXP_MAX_HI_TERM_VAL-EXP_NUM_OF_HI_TERMS))
for n in range(1,len(loTerms)):
    str0 = '{0:#0{1}x}'.format(loTerms[n].val,loTermValMaxLen)
    str1 = '{0:0{1}d}' .format(loTerms[n].ind,loTermIndMaxLen)
    str2 = '{0:0{1}d}' .format(len(loTerms)  ,loTermIndMaxLen)
    print('        z = z * y / FIXED_1; res += z * {}; // add y^{} * ({}! / {}!)'.format(str0,str1,str2,str1))
print('        res = res / 0x{:x} + y + FIXED_1; // divide by {}! and then add y^1 / 1! + y^0 / 0!'.format(loTerms[0].val,len(loTerms)))
print('')
for n in range(len(hiTerms)-1):
    str3 = '{0:#0{1}x}'.format(hiTerms[n].bit,hiTermBitMaxLen)
    str4 = '{0:#0{1}x}'.format(hiTerms[n].num,hiTermNumMaxLen)
    str5 = '{0:#0{1}x}'.format(hiTerms[n].den,hiTermDenMaxLen)
    str6 = '{0:+{1}d}' .format(hiTermIndMin+n,hiTermIndMaxLen)
    print('        if ((x & {}) != 0) res = res * {} / {}; // multiply by e^2^({})'.format(str3,str4,str5,str6))
print('')
print('        return res;')
print('    }}')
