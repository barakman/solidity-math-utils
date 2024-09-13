from util import hex_len
from core import AdvancedMath
from constants import FIXED_1
from constants import LAMBERT_POS2_EXTENT
from constants import LAMBERT_POS2_SAMPLES


LAMBERT_CONV_RADIUS = AdvancedMath.lambertRadius(FIXED_1)
LAMBERT_POS2_SAMPLE = LAMBERT_POS2_EXTENT*FIXED_1//(LAMBERT_POS2_SAMPLES-1)
LAMBERT_POS2_MAXVAL = LAMBERT_CONV_RADIUS+LAMBERT_POS2_SAMPLE*(LAMBERT_POS2_SAMPLES-1)


samples = AdvancedMath.lambertSamples(FIXED_1,LAMBERT_POS2_SAMPLE,LAMBERT_POS2_SAMPLES)


LAMBERT_POS2_T_SIZE = (len(bin(max(samples)))-3)//8+1
LAMBERT_POS2_T_MASK = (1<<(LAMBERT_POS2_T_SIZE*8))-1
LAMBERT_POS2_VALUES = [f'hex"{sample:0{LAMBERT_POS2_T_SIZE*2}x}"' for sample in samples]


maxLen = hex_len(max([LAMBERT_CONV_RADIUS,LAMBERT_POS2_SAMPLE,LAMBERT_POS2_MAXVAL,LAMBERT_POS2_T_SIZE,LAMBERT_POS2_T_MASK]))


print(f'    uint256 internal constant LAMBERT_CONV_RADIUS = {LAMBERT_CONV_RADIUS:#0{maxLen}x};')
print(f'    uint256 internal constant LAMBERT_POS2_SAMPLE = {LAMBERT_POS2_SAMPLE:#0{maxLen}x};')
print(f'    uint256 internal constant LAMBERT_POS2_MAXVAL = {LAMBERT_POS2_MAXVAL:#0{maxLen}x};')
print(f'    uint256 internal constant LAMBERT_POS2_T_SIZE = {LAMBERT_POS2_T_SIZE:#0{maxLen}x};')
print(f'    uint256 internal constant LAMBERT_POS2_T_MASK = {LAMBERT_POS2_T_MASK:#0{maxLen}x};')
print(f'    bytes   internal constant LAMBERT_POS2_VALUES = {"\n".ljust(53).join(LAMBERT_POS2_VALUES)};')
