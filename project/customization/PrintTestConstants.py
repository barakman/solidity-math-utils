import os
import sys
import constants


stdout = sys.stdout
sys.stdout = open(os.devnull,'w')
import PrintAnalyticMathConstants as AnalyticMath
import PrintAdvancedMathConstants as AdvancedMath
sys.stdout.close()
sys.stdout = stdout


print(f'module.exports.LOG_MAX_HI_TERM_VAL = {constants.LOG_MAX_HI_TERM_VAL};')
print(f'module.exports.LOG_NUM_OF_HI_TERMS = {constants.LOG_NUM_OF_HI_TERMS};')
print(f'module.exports.EXP_MAX_HI_TERM_VAL = {constants.EXP_MAX_HI_TERM_VAL};')
print(f'module.exports.EXP_NUM_OF_HI_TERMS = {constants.EXP_NUM_OF_HI_TERMS};')
print(f'module.exports.FIXED_1 = "{AnalyticMath.FIXED_1:#0{AnalyticMath.maxLen}x}";')
print(f'module.exports.LOG_MID = "{AnalyticMath.LOG_MID:#0{AnalyticMath.maxLen}x}";')
print(f'module.exports.EXP_MID = "{AnalyticMath.EXP_MID:#0{AnalyticMath.maxLen}x}";')
print(f'module.exports.EXP_MAX = "{AnalyticMath.EXP_MAX:#0{AnalyticMath.maxLen}x}";')
print(f'module.exports.LAMBERT_NEG1_MAXVAL = "{AdvancedMath.LAMBERT_NEG1_MAXVAL:#0{AdvancedMath.maxLen}x}";')
print(f'module.exports.LAMBERT_NEG2_MAXVAL = "{AdvancedMath.LAMBERT_NEG2_MAXVAL:#0{AdvancedMath.maxLen}x}";')
print(f'module.exports.LAMBERT_POS1_MAXVAL = "{AdvancedMath.LAMBERT_POS1_MAXVAL:#0{AdvancedMath.maxLen}x}";')
print(f'module.exports.LAMBERT_POS2_MAXVAL = "{AdvancedMath.LAMBERT_POS2_MAXVAL:#0{AdvancedMath.maxLen}x}";')
print(f'module.exports.LAMBERT_EXACT_LIMIT = "{AdvancedMath.LAMBERT_EXACT_LIMIT:#066x}";')
