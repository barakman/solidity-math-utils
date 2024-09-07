from common import Decimal
from common.constants import FIXED_1
from common.constants import LAMBERT_POS2_EXTENT
from common.constants import LAMBERT_POS2_SAMPLES


def lambertRatio(x):
    a = x if x < 1 else x.ln()
    for _ in range(8):
        e = a.exp()
        f = a * e
        if f == x: break
        a = (a * f + x) / (f + e)
    return a / x


LAMBERT_CONV_RADIUS = int(Decimal(-1).exp()*FIXED_1)
LAMBERT_POS2_SAMPLE = LAMBERT_POS2_EXTENT*FIXED_1//(LAMBERT_POS2_SAMPLES-1)
LAMBERT_POS2_MAXVAL = LAMBERT_CONV_RADIUS+LAMBERT_POS2_SAMPLE*(LAMBERT_POS2_SAMPLES-1)


weights = [Decimal(LAMBERT_CONV_RADIUS+1+LAMBERT_POS2_SAMPLE*i)/FIXED_1 for i in range(LAMBERT_POS2_SAMPLES)]
samples = [int(lambertRatio(x)*FIXED_1) for x in weights]


LAMBERT_POS2_VALUES = [f'hex"{sample:{len(hex(samples[0]))-2}x}"' for sample in samples]


maxLen = len(hex(max([LAMBERT_CONV_RADIUS,LAMBERT_POS2_SAMPLE,LAMBERT_POS2_MAXVAL])))


print(f'    uint256 internal constant LAMBERT_CONV_RADIUS = {LAMBERT_CONV_RADIUS:#0{maxLen}x};')
print(f'    uint256 internal constant LAMBERT_POS2_SAMPLE = {LAMBERT_POS2_SAMPLE:#0{maxLen}x};')
print(f'    uint256 internal constant LAMBERT_POS2_MAXVAL = {LAMBERT_POS2_MAXVAL:#0{maxLen}x};')
print(f'    bytes   internal constant LAMBERT_POS2_VALUES = {"\n".ljust(53).join(LAMBERT_POS2_VALUES)};')
