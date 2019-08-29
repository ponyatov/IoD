# IoD metacircular implementation

from IoD import *

IoD = VM('IoD')

IoD['W'] = IoD
IoD['S'] = IoD

def WEB(ctx): ctx['WEB'] = Web(ctx.val) ; ctx['WEB'].eval(ctx)
IoD << WEB

print(IoD)

IoD['WEB'].eval(IoD)
print(IoD)
