import numpy as np
import scipy as sp

from BivTrunc.BivTruncF import bivtruncf

def BivTruncSimple(xydat, datlim, lambdax, lambday, mask, deg=1, maxiters1 = 1000,
                  maxiters2 = 100, verbose=False, datwght=1, calccovs=False):

	if(datwght == 1):
		datwght = np.ones(len(xydat))
	if(isinstance(lambdax,float)):
		lambdax = lambdax * np.ones(len(mask))
	if(isinstance(lambday,float)):
		lambday = lambday * np.ones(len(mask))
	mask2 = mask
	grdsize = len(mask)
	bivest,grdcov,grdest,lvout,fits,info,lscv,likecv,likelihood,fpr,gpr,theta,setheta = \
         bivtruncf(xydat,deg,datlim,lambdax,lambday,mask,maxiters1,
         maxiters2,grdsize,verbose,datwght,mask2,calccovs)
	return(bivest,grdcov,grdest,lvout,fits,info,lscv,likecv,likelihood,fpr,gpr,theta,setheta)
