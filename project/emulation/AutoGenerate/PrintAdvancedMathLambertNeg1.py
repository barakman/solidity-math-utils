from common.functions import lambertCoefs


coefficients = lambertCoefs()


valueMaxLen = len(hex(coefficients[-1]))
indexMaxLen = len(str(len(coefficients)))


print('    function lambertNeg1(uint256 x) internal pure returns (uint256) { unchecked {')
print('        uint256 xi = x;')
print('        uint256 res = 0;')
print('')
for i in range(2,len(coefficients)):
    print('        xi = (xi * x) / FIXED_1; res += xi * {0:#0{3}x}; // add x^({1:0{4}d}-1) * ({2:d}! * {1:0{4}d}^({1:0{4}d}-1) / {1:0{4}d}!)'.format(coefficients[i],i+1,len(coefficients),valueMaxLen,indexMaxLen))
print('')
print('        return res / 0x{:x} + x + FIXED_1; // divide by {}! and then add x^(2-1) * ({}! * 2^(2-1) / 2!) + x^(1-1) * ({}! * 1^(1-1) / 1!)'.format(coefficients[0],len(coefficients),len(coefficients),len(coefficients)))
print('    }}')
