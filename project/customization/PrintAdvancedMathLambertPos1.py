from util import len_str
from util import len_hex
from core import AdvancedMath
from constants import FIXED_1
from constants import LAMBERT_MAX_COEFS


lambertCoefs = AdvancedMath.lambertCoefs(FIXED_1,LAMBERT_MAX_COEFS,+1)


valueMaxLen = len_hex(lambertCoefs[-1])
indexMaxLen = len_str(len(lambertCoefs))


str0 = '{0:#0{1}x}'.format(lambertCoefs[0]  ,len_hex(lambertCoefs[0]  ))
str1 = '{0:0{1}d}' .format(len(lambertCoefs),len_str(len(lambertCoefs)))


print('    function lambertPos1(uint256 x) internal pure returns (uint256) { unchecked {')
print('        uint256 xi = x;')
print('        uint256 res = (FIXED_1 - x) * {}; // x^(1-1) * ({}! * 1^(1-1) / 1!) - x^(2-1) * ({}! * 2^(2-1) / 2!)'.format(str0,str1,str1))
print('')
for n in range(2,len(lambertCoefs)):
    str2 = '{0:#0{1}x}'.format(lambertCoefs[n],valueMaxLen)
    str3 = '{0:0{1}d}' .format(n+1            ,indexMaxLen)
    str4 = '{:s}'.format(['+'  ,'-'  ][n%2])
    str5 = '{:s}'.format(['add','sub'][n%2])
    print('        xi = (xi * x) / FIXED_1; res {}= xi * {}; // {} x^({}-1) * ({}! * {}^({}-1) / {}!)'.format(str4,str2,str5,str3,str1,str3,str3,str3))
print('')
print('        return res / {}; // divide by {}!'.format(str0,str1))
print('    }}')
