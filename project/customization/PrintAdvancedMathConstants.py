from util import hex_len
from core import AdvancedMath
from constants import FIXED_1
from constants import LAMBERT_NEG2_SIZE_N
from constants import LAMBERT_NEG2_SIZE_D
from constants import LAMBERT_NEG2_SAMPLES
from constants import LAMBERT_POS2_SIZE_N
from constants import LAMBERT_POS2_SIZE_D
from constants import LAMBERT_POS2_SAMPLES


lambertNegParams = AdvancedMath.lambertNegParams(FIXED_1,LAMBERT_NEG2_SIZE_N,LAMBERT_NEG2_SIZE_D,LAMBERT_NEG2_SAMPLES)
lambertPosParams = AdvancedMath.lambertPosParams(FIXED_1,LAMBERT_POS2_SIZE_N,LAMBERT_POS2_SIZE_D,LAMBERT_POS2_SAMPLES)


LAMBERT_NEG1_MAXVAL = lambertNegParams[0]
LAMBERT_NEG2_MAXVAL = lambertNegParams[1]
LAMBERT_NEG2_SAMPLE = lambertNegParams[2]
LAMBERT_NEG2_T_SIZE = lambertNegParams[3]
LAMBERT_NEG2_T_MASK = lambertNegParams[4]
LAMBERT_NEG2_VALUES = lambertNegParams[5]
LAMBERT_POS1_MAXVAL = lambertPosParams[0]
LAMBERT_POS2_MAXVAL = lambertPosParams[1]
LAMBERT_POS2_SAMPLE = lambertPosParams[2]
LAMBERT_POS2_T_SIZE = lambertPosParams[3]
LAMBERT_POS2_T_MASK = lambertPosParams[4]
LAMBERT_POS2_VALUES = lambertPosParams[5]


maxLen = hex_len(max([
    LAMBERT_NEG1_MAXVAL,
    LAMBERT_NEG2_MAXVAL,
    LAMBERT_NEG2_SAMPLE,
    LAMBERT_NEG2_T_SIZE,
    LAMBERT_NEG2_T_MASK,
    LAMBERT_POS1_MAXVAL,
    LAMBERT_POS2_MAXVAL,
    LAMBERT_POS2_SAMPLE,
    LAMBERT_POS2_T_SIZE,
    LAMBERT_POS2_T_MASK,
]))


def format(values, size): return '\n'.ljust(53).join([f'hex"{value:0{size*2}x}"' for value in values])


print(f'    uint256 internal constant LAMBERT_NEG1_MAXVAL = {LAMBERT_NEG1_MAXVAL:#0{maxLen}x};')
print(f'    uint256 internal constant LAMBERT_NEG2_MAXVAL = {LAMBERT_NEG2_MAXVAL:#0{maxLen}x};')
print(f'    uint256 internal constant LAMBERT_NEG2_SAMPLE = {LAMBERT_NEG2_SAMPLE:#0{maxLen}x};')
print(f'    uint256 internal constant LAMBERT_NEG2_T_SIZE = {LAMBERT_NEG2_T_SIZE:#0{maxLen}x};')
print(f'    uint256 internal constant LAMBERT_NEG2_T_MASK = {LAMBERT_NEG2_T_MASK:#0{maxLen}x};')
print(f'    uint256 internal constant LAMBERT_POS1_MAXVAL = {LAMBERT_POS1_MAXVAL:#0{maxLen}x};')
print(f'    uint256 internal constant LAMBERT_POS2_MAXVAL = {LAMBERT_POS2_MAXVAL:#0{maxLen}x};')
print(f'    uint256 internal constant LAMBERT_POS2_SAMPLE = {LAMBERT_POS2_SAMPLE:#0{maxLen}x};')
print(f'    uint256 internal constant LAMBERT_POS2_T_SIZE = {LAMBERT_POS2_T_SIZE:#0{maxLen}x};')
print(f'    uint256 internal constant LAMBERT_POS2_T_MASK = {LAMBERT_POS2_T_MASK:#0{maxLen}x};')
print(f'    bytes   internal constant LAMBERT_NEG2_VALUES = {format(LAMBERT_NEG2_VALUES,LAMBERT_NEG2_T_SIZE)};')
print(f'    bytes   internal constant LAMBERT_POS2_VALUES = {format(LAMBERT_POS2_VALUES,LAMBERT_POS2_T_SIZE)};')
