import os
import sys


stdout = sys.stdout
sys.stdout = open(os.devnull,'w')
import PrintAnalyticMathConstants as AnalyticMath
import PrintAdvancedMathConstants as AdvancedMath
sys.stdout.close()
sys.stdout = stdout


print(f'module.exports.FIXED_1 = "{AnalyticMath.FIXED_1:#0{AnalyticMath.maxLen}x}";')
print(f'module.exports.LN2_MIN = "{AnalyticMath.LN2_MIN:#0{AnalyticMath.maxLen}x}";')
print(f'module.exports.LN2_MAX = "{AnalyticMath.LN2_MAX:#0{AnalyticMath.maxLen}x}";')
print(f'module.exports.LOG_MID = "{AnalyticMath.LOG_MID:#0{AnalyticMath.maxLen}x}";')
print(f'module.exports.EXP_MID = "{AnalyticMath.EXP_MID:#0{AnalyticMath.maxLen}x}";')
print(f'module.exports.EXP_MAX = "{AnalyticMath.EXP_MAX:#0{AnalyticMath.maxLen}x}";')
print(f'module.exports.LAMBERT_CONV_RADIUS = "{AdvancedMath.LAMBERT_CONV_RADIUS:#0{AdvancedMath.maxLen}x}";')
print(f'module.exports.LAMBERT_POS2_SAMPLE = "{AdvancedMath.LAMBERT_POS2_SAMPLE:#0{AdvancedMath.maxLen}x}";')
print(f'module.exports.LAMBERT_POS2_MAXVAL = "{AdvancedMath.LAMBERT_POS2_MAXVAL:#0{AdvancedMath.maxLen}x}";')
