FIXED_1 = 2 ** 127 # The scaling factor


LOG_MAX_HI_TERM_VAL = 1 # The input to function 'optimalLog' must be smaller than e ^ LOG_MAX_HI_TERM_VAL
LOG_NUM_OF_HI_TERMS = 8 # Compute LOG_MAX_HI_TERM_VAL / 2 ^ n for n = 1 to LOG_NUM_OF_HI_TERMS


EXP_MAX_HI_TERM_VAL = 4 # The input to function 'optimalExp' must be smaller than 2 ^ EXP_MAX_HI_TERM_VAL
EXP_NUM_OF_HI_TERMS = 7 # Compute e ^ 2 ^ (n - EXP_MAX_HI_TERM_VAL) for n = 1 to EXP_NUM_OF_HI_TERMS


LAMBERT_MAX_TERMS    =  48 # The maximum number of terms used for approximating the Lambert W Function inside the convergence radius
LAMBERT_POS2_EXTENT  =   3 # The size of the extended output range calculated by the Lambert W Function outside the convergence radius
LAMBERT_POS2_SAMPLES = 128 # The size of the lookup table used for approximating the Lambert W Function outside the convergence radius
