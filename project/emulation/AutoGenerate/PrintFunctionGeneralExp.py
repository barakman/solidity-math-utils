from common.functions import getTaylorCoefs
from common.constants import NUM_OF_TAYLOR_COEFS


coefficients = getTaylorCoefs(NUM_OF_TAYLOR_COEFS)


valueMaxLen = len(hex(coefficients[1]))
indexMaxLen = len(str(len(coefficients)))


print('    function generalExp(uint256 x, uint8 precision) internal pure returns (uint256) { unchecked {')
print('        uint256 xi = x;')
print('        uint256 res = 0;')
print('')
for i in range(1,len(coefficients)):
    print('        xi = (xi * x) >> precision; res += xi * {0:#0{4}x}; // add x^{1:0{5}d} * ({2:0{5}d}! / {3:0{5}d}!)'.format(coefficients[i],i+1,len(coefficients),i+1,valueMaxLen,indexMaxLen))
print('')
print('        return res / 0x{:x} + x + (1 << precision); // divide by {}! and then add x^1 / 1! + x^0 / 0!'.format(coefficients[0],len(coefficients)))
print('    }}')
