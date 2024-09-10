from core import AdvancedMath
from constants import FIXED_1
from constants import LAMBERT_MAX_COEFS


lambertCoefs = AdvancedMath.lambertCoefs(FIXED_1,LAMBERT_MAX_COEFS,-1)


valueMaxLen = len(hex(lambertCoefs[-1]))
indexMaxLen = len(str(len(lambertCoefs)))


print('    function lambertNeg1(uint256 x) internal pure returns (uint256) { unchecked {')
print('        uint256 xi = x;')
print('        uint256 res = 0;')
print('')
for i in range(2,len(lambertCoefs)):
    print('        xi = (xi * x) / FIXED_1; res += xi * {0:#0{3}x}; // add x^({1:0{4}d}-1) * ({2:d}! * {1:0{4}d}^({1:0{4}d}-1) / {1:0{4}d}!)'.format(lambertCoefs[i],i+1,len(lambertCoefs),valueMaxLen,indexMaxLen))
print('')
print('        return res / 0x{:x} + x + FIXED_1; // divide by {}! and then add x^(2-1) * ({}! * 2^(2-1) / 2!) + x^(1-1) * ({}! * 1^(1-1) / 1!)'.format(lambertCoefs[0],len(lambertCoefs),len(lambertCoefs),len(lambertCoefs)))
print('    }}')
