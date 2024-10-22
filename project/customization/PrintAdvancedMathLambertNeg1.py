from util import dec_str
from util import hex_str
from core import AdvancedMath
from constants import FIXED_1
from constants import LAMBERT_MAX_TERMS


lambertTerms = AdvancedMath.lambertNeg1Terms(FIXED_1,LAMBERT_MAX_TERMS)


str0 = hex_str(lambertTerms[0],lambertTerms[0])
str1 = dec_str(len(lambertTerms),len(lambertTerms))


print('    function lambertNeg1(uint256 x) internal pure returns (uint256) { unchecked {')
print('        uint256 xi = x;')
print('        uint256 res = 0;')
print('')
for n in range(2,len(lambertTerms)):
    str2 = hex_str(lambertTerms[n],lambertTerms[-1])
    str3 = dec_str(n+1,len(lambertTerms))
    print('        xi = (xi * x) / FIXED_1; res += xi * {}; // add x^({}-1) * ({}! * {}^({}-1) / {}!)'.format(str2,str3,str1,str3,str3,str3))
print('')
print('        return res / {} + x + FIXED_1; // divide by {}! and then add x^(2-1) * ({}! * 2^(2-1) / 2!) + x^(1-1) * ({}! * 1^(1-1) / 1!)'.format(str0,str1,str1,str1))
print('    }}')
