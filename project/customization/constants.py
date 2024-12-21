FIXED_1 = 2 ** 127 # The scaling factor


LOG_MAX_HI_TERM_VAL = 0 # The input to function 'optimalLog' must be smaller than e ^ 2 ^ LOG_MAX_HI_TERM_VAL
LOG_NUM_OF_HI_TERMS = 8 # Compute 2 ^ (LOG_MAX_HI_TERM_VAL - LOG_NUM_OF_HI_TERMS + n - 1) for n = LOG_NUM_OF_HI_TERMS to 1


EXP_MAX_HI_TERM_VAL = 3 # The input to function 'optimalExp' must be smaller than 2 ^ EXP_MAX_HI_TERM_VAL
EXP_NUM_OF_HI_TERMS = 6 # Compute e ^ 2 ^ (EXP_MAX_HI_TERM_VAL - EXP_NUM_OF_HI_TERMS + n - 1) for n = 1 to EXP_NUM_OF_HI_TERMS


LAMBERT_NEG1_TERMS   =  48 # The maximum number of terms used for approximating the Lambert W Function inside the negative convergence radius
LAMBERT_NEG2_SIZE_N  =   1 # The portion of the negative convergence radius to approximate using a lookup table instead of with a Taylor series
LAMBERT_NEG2_SIZE_D  = 100 # The portion of the negative convergence radius to approximate using a lookup table instead of with a Taylor series
LAMBERT_NEG2_SAMPLES =  16 # The number of samples used for approximating the Lambert W Function towards the end of the negative convergence radius


LAMBERT_POS1_TERMS   =  48 # The maximum number of terms used for approximating the Lambert W Function inside the positive convergence radius
LAMBERT_POS2_SIZE_N  =  24 # The range above the positive convergence radius to approximate using a lookup table instead of with a Taylor series
LAMBERT_POS2_SIZE_D  =   1 # The range above the positive convergence radius to approximate using a lookup table instead of with a Taylor series
LAMBERT_POS2_SAMPLES = 128 # The number of samples used for approximating the Lambert W Function beyond the end of the positive convergence radius
