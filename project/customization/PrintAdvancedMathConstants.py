from core import AdvancedMath
from constants import FIXED_1
from constants import LAMBERT_POS2_EXTENT
from constants import LAMBERT_POS2_SAMPLES


LAMBERT_CONV_RADIUS = AdvancedMath.lambertRadius(FIXED_1)
LAMBERT_POS2_SAMPLE = LAMBERT_POS2_EXTENT*FIXED_1//(LAMBERT_POS2_SAMPLES-1)
LAMBERT_POS2_MAXVAL = LAMBERT_CONV_RADIUS+LAMBERT_POS2_SAMPLE*(LAMBERT_POS2_SAMPLES-1)
LAMBERT_POS2_VALUES = [f'hex"{v:032x}"' for v in AdvancedMath.lambertSamples(FIXED_1,LAMBERT_POS2_SAMPLE,LAMBERT_POS2_SAMPLES)]


maxLen = len(hex(max([LAMBERT_CONV_RADIUS,LAMBERT_POS2_SAMPLE,LAMBERT_POS2_MAXVAL])))


print(f'    uint256 internal constant LAMBERT_CONV_RADIUS = {LAMBERT_CONV_RADIUS:#0{maxLen}x};')
print(f'    uint256 internal constant LAMBERT_POS2_SAMPLE = {LAMBERT_POS2_SAMPLE:#0{maxLen}x};')
print(f'    uint256 internal constant LAMBERT_POS2_MAXVAL = {LAMBERT_POS2_MAXVAL:#0{maxLen}x};')
print(f'    bytes   internal constant LAMBERT_POS2_VALUES = {"\n".ljust(53).join(LAMBERT_POS2_VALUES)};')
