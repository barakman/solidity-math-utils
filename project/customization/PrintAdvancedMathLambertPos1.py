from core import AdvancedMath
from constants import FIXED_1
from constants import LAMBERT_MAX_COEFS


lambertCoefs = AdvancedMath.lambertCoefs(FIXED_1,LAMBERT_MAX_COEFS,+1)


valueMaxLen = len(hex(lambertCoefs[-1]))
indexMaxLen = len(str(len(lambertCoefs)))


print('    function lambertPos1(uint256 x) internal pure returns (uint256) { unchecked {')
print('        uint256 xi = x;')
print('        uint256 res = (FIXED_1 - x) * 0x{:x}; // x^(1-1) * ({}! * 1^(1-1) / 1!) - x^(2-1) * ({}! * 2^(2-1) / 2!)'.format(lambertCoefs[0],len(lambertCoefs),len(lambertCoefs)))
print('')
for i in range(2,len(lambertCoefs)):
    print('        xi = (xi * x) / FIXED_1; res {5:s}= xi * {0:#0{3}x}; // {6:s} x^({1:0{4}d}-1) * ({2:d}! * {1:0{4}d}^({1:0{4}d}-1) / {1:0{4}d}!)'.format(lambertCoefs[i],i+1,len(lambertCoefs),valueMaxLen,indexMaxLen,'+-'[i%2],['add','sub'][i%2]))
print('')
print('        return res / 0x{:x}; // divide by {}!'.format(lambertCoefs[0],len(lambertCoefs)))
print('    }}')
