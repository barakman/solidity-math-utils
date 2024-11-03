FIXED_1 = 2 ** 127 # The scaling factor


LOG_MAX_HI_TERM_VAL = 0 # The input to function 'optimalLog' must be smaller than e ^ 2 ^ LOG_MAX_HI_TERM_VAL
LOG_NUM_OF_HI_TERMS = 8 # Compute 2 ^ (LOG_MAX_HI_TERM_VAL - LOG_NUM_OF_HI_TERMS + n - 1) for n = LOG_NUM_OF_HI_TERMS to 1


EXP_MAX_HI_TERM_VAL = 3 # The input to function 'optimalExp' must be smaller than 2 ^ EXP_MAX_HI_TERM_VAL
EXP_NUM_OF_HI_TERMS = 6 # Compute e ^ 2 ^ (EXP_MAX_HI_TERM_VAL - EXP_NUM_OF_HI_TERMS + n - 1) for n = 1 to EXP_NUM_OF_HI_TERMS


LAMBERT_NEG1_TERMS  =  48 # The maximum number of terms used for approximating the Lambert W Function inside the negative convergence radius
LAMBERT_NEG1_PART_N =  99 # The portion of the negative convergence radius to approximate via Taylor series instead of Newton-Raphson convergence
LAMBERT_NEG1_PART_D = 100 # The portion of the negative convergence radius to approximate via Taylor series instead of Newton-Raphson convergence


LAMBERT_POS1_TERMS   =  48 # The maximum number of terms used for approximating the Lambert W Function inside the positive convergence radius
LAMBERT_POS2_EXTENT  =  24 # The size of the extended output range calculated by the Lambert W Function outside the positive convergence radius
LAMBERT_POS2_SAMPLES = 128 # The size of the lookup table used for approximating the Lambert W Function outside the positive convergence radius
