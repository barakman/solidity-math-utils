from util import dec_str
from util import hex_str
from core import AdvancedMath
from constants import FIXED_1
from constants import LAMBERT_MAX_TERMS


terms = AdvancedMath.lambertPos1Terms(FIXED_1,LAMBERT_MAX_TERMS)


str0 = hex_str(terms[0],terms[0])
str1 = dec_str(len(terms),len(terms))


print('    function lambertPos1(uint256 x) internal pure returns (uint256) { unchecked {')
print('        uint256 xi = x;')
print('        uint256 res = (FIXED_1 - x) * {}; // x^(1-1) * ({}! * 1^(1-1) / 1!) - x^(2-1) * ({}! * 2^(2-1) / 2!)'.format(str0,str1,str1))
print('')
for n in range(2,len(terms)):
    str2 = hex_str(terms[n],terms[-1])
    str3 = dec_str(n+1,len(terms))
    str4 = ['+'  ,'-'  ][n%2]
    str5 = ['add','sub'][n%2]
    print('        xi = (xi * x) / FIXED_1; res {}= xi * {}; // {} x^({}-1) * ({}! * {}^({}-1) / {}!)'.format(str4,str2,str5,str3,str1,str3,str3,str3))
print('')
print('        return res / {}; // divide by {}!'.format(str0,str1))
print('    }}')
