from util import dec_str
from util import hex_str
from core import AdvancedMath
from constants import FIXED_1
from constants import LAMBERT_POS1_TERMS
from constants import LAMBERT_POS2_SIZE_N
from constants import LAMBERT_POS2_SIZE_D
from constants import LAMBERT_POS2_SAMPLES


terms = AdvancedMath.lambertPos1Terms(FIXED_1,LAMBERT_POS1_TERMS,LAMBERT_POS2_SIZE_N,LAMBERT_POS2_SIZE_D,LAMBERT_POS2_SAMPLES)


str0 = hex_str(terms[0],terms[0])
str1 = dec_str(len(terms),len(terms))


print('    function lambertPos1(uint256 x) internal pure returns (uint256) { unchecked {')
print('        uint256 res = 0;')
print('        uint256 xi = x;')
print('')
for n in range(2,len(terms)):
    str2 = hex_str(terms[n],terms[-1])
    str3 = dec_str(n+1,len(terms))
    str4 = ['+'  ,'-'  ][n%2]
    str5 = ['add','sub'][n%2]
    print('        xi = xi * x / FIXED_1; res {}= xi * {}; // {} x^({}-1) * ({}! * {}^({}-1) / {}!)'.format(str4,str2,str5,str3,str1,str3,str3,str3))
print('')
print('        return res / {} + FIXED_1 - x; // divide by {}! and then add x^(1-1) * (1^(1-1) / 1!) - x^(2-1) * (2^(2-1) / 2!)'.format(str0,str1))
print('    }}')
