from util import hex_len
from core import AdvancedMath
from constants import FIXED_1
from constants import LAMBERT_POS2_EXTENT
from constants import LAMBERT_POS2_SAMPLES


lambertRadius = AdvancedMath.lambertRadius(FIXED_1)
lambertSample = AdvancedMath.lambertSample(FIXED_1,LAMBERT_POS2_EXTENT,LAMBERT_POS2_SAMPLES)
samples = AdvancedMath.lambertSamples(FIXED_1,lambertRadius+1,lambertSample,LAMBERT_POS2_SAMPLES)


LAMBERT_NEG1_MAXVAL = lambertRadius*99//100
LAMBERT_NEG2_MAXVAL = lambertRadius
LAMBERT_POS1_MAXVAL = lambertRadius
LAMBERT_POS2_MAXVAL = lambertSample*(LAMBERT_POS2_SAMPLES-1)+LAMBERT_POS1_MAXVAL
LAMBERT_POS2_SAMPLE = lambertSample
LAMBERT_POS2_T_SIZE = (len(bin(max(samples)))-3)//8+1
LAMBERT_POS2_T_MASK = (1<<(LAMBERT_POS2_T_SIZE*8))-1
LAMBERT_POS2_VALUES = [f'hex"{sample:0{LAMBERT_POS2_T_SIZE*2}x}"' for sample in samples]


maxLen = hex_len(max([
    LAMBERT_NEG1_MAXVAL,
    LAMBERT_NEG2_MAXVAL,
    LAMBERT_POS1_MAXVAL,
    LAMBERT_POS2_MAXVAL,
    LAMBERT_POS2_SAMPLE,
    LAMBERT_POS2_T_SIZE,
    LAMBERT_POS2_T_MASK,
]))


print(f'    uint256 internal constant LAMBERT_NEG1_MAXVAL = {LAMBERT_NEG1_MAXVAL:#0{maxLen}x};')
print(f'    uint256 internal constant LAMBERT_NEG2_MAXVAL = {LAMBERT_NEG2_MAXVAL:#0{maxLen}x};')
print(f'    uint256 internal constant LAMBERT_POS1_MAXVAL = {LAMBERT_POS1_MAXVAL:#0{maxLen}x};')
print(f'    uint256 internal constant LAMBERT_POS2_MAXVAL = {LAMBERT_POS2_MAXVAL:#0{maxLen}x};')
print(f'    uint256 internal constant LAMBERT_POS2_SAMPLE = {LAMBERT_POS2_SAMPLE:#0{maxLen}x};')
print(f'    uint256 internal constant LAMBERT_POS2_T_SIZE = {LAMBERT_POS2_T_SIZE:#0{maxLen}x};')
print(f'    uint256 internal constant LAMBERT_POS2_T_MASK = {LAMBERT_POS2_T_MASK:#0{maxLen}x};')
print(f'    bytes   internal constant LAMBERT_POS2_VALUES = {"\n".ljust(53).join(LAMBERT_POS2_VALUES)};')
