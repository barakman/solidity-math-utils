from util import dec_str
from util import hex_str
from core import AdvancedMath
from constants import FIXED_1
from constants import LAMBERT_MAX_TERMS


terms = AdvancedMath.lambertNeg1Terms(FIXED_1,LAMBERT_MAX_TERMS)


str0 = hex_str(terms[0],terms[0])
str1 = dec_str(len(terms),len(terms))


print('    function lambertNeg1(uint256 x) internal pure returns (uint256) { unchecked {')
print('        uint256 res = 0;')
print('        uint256 xi = x;')
print('')
for n in range(2,len(terms)):
    str2 = hex_str(terms[n],terms[-1])
    str3 = dec_str(n+1,len(terms))
    print('        xi = (xi * x) / FIXED_1; res += xi * {}; // add x^({}-1) * ({}! * {}^({}-1) / {}!)'.format(str2,str3,str1,str3,str3,str3))
print('')
print('        return res / {} + FIXED_1 + x; // divide by {}! and then add x^(1-1) * (1^(1-1) / 1!) + x^(2-1) * (2^(2-1) / 2!)'.format(str0,str1))
print('    }}')
