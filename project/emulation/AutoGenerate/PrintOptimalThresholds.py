import os
import sys

stdout = sys.stdout
sys.stdout = open(os.devnull,'w')

import PrintFunctionOptimalLog
import PrintFunctionOptimalExp

sys.stdout.close()
sys.stdout = stdout

print('    uint256 internal constant OPT_LOG_MAX_VAL = 0x{:x};'.format(PrintFunctionOptimalLog.hiTerms[0].exp))
print('    uint256 internal constant OPT_EXP_MAX_VAL = 0x{:x};'.format(PrintFunctionOptimalExp.hiTerms[-1].bit))
