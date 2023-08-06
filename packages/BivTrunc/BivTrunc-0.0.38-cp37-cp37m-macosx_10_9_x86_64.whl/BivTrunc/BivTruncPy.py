import numpy as np
import scipy as sp


from BivTrunc.BivTruncF import bivtruncf


def BivTruncP(xydat, datlim, lambdax, lambday, mask, deg=1, maxiters1 = 1000,
                  maxiters2 = 100, datwght=1, calccovs=True):
    """
    --------------------
    This is the help.
    """
    
    # This is an input into the Fortran function, but it's unclear if it
    # has any effect.
    
    verbose = False
    
    if(datwght == 1):
        datwght = np.ones(len(xydat))
    
    if(isinstance(lambdax,float)):
        lambdax = lambdax * np.ones(len(mask))
        
    if(isinstance(lambday,float)):
        lambday = lambday * np.ones(len(mask))
        
    mask2 = mask
    grdsize = len(mask)
    
    
    # The call to the Fortran function
    
    bivest,grdcov,grdest,lvout,fits,info,lscv,likecv,likelihood,fpr,gpr,theta,setheta = \
      bivtruncf(xydat,deg,datlim,lambdax,lambday,mask,maxiters1,
         maxiters2,grdsize,verbose,datwght,mask2,calccovs)

    
    # The grid of values in the x and y directions at which the density is evaluated
    
    xgrid = np.linspace(datlim[0,0],datlim[1,0],grdsize,endpoint=False) + (datlim[1,0]-datlim[0,0])/grdsize/2
    ygrid = np.linspace(datlim[0,1],datlim[1,1],grdsize,endpoint=False) + (datlim[1,1]-datlim[0,1])/grdsize/2
    
   
    # Transform bivest so that it is no longer on the log scale

    bivest = np.exp(bivest)


    # Calculate the marginals
    
    xmarg = np.sum(bivest,1)*(datlim[1,1]-datlim[0,1])/grdsize
    ymarg = np.sum(bivest,0)*(datlim[1,0]-datlim[0,0])/grdsize

    
    class out:
        def __init__(self,bivest,grdcov,lvout,fits,info,lscv,likecv,likelihood,fpr,gpr,theta,setheta,
                     xmarg, ymarg, xgrid, ygrid, grdsize,
                    xydat, datlim, lambdax, lambday, mask, deg, maxiters1, maxiters2, datwght, calccovs):
            self.bivest = bivest
            self.grdcov = grdcov
            self.lvout = lvout
            self.fits = fits
            self.info = info
            self.lscv = lscv
            self.likecv = likecv
            self.likelihood = likelihood
            self.fpr = fpr
            self.gpr = gpr
            self.theta = theta
            self.setheta = setheta
            self.xmarg = xmarg
            self.ymarg = ymarg
            self.xgrid = xgrid
            self.ygrid = ygrid
            self.grdsize = grdsize
            self.xydat = xydat
            self.datlim = datlim
            self.lambdax = lambdax
            self.lambday = lambday
            self.mask = mask
            self.deg = deg
            self.maxiters1 = maxiters1
            self.maxiters2 = maxiters2
            self.datwght = datwght
            self.calccovs = calccovs
            
    return(out(bivest,grdcov,lvout,fits,info,lscv,likecv,likelihood,fpr,gpr,theta,setheta,
               xmarg, ymarg, xgrid, ygrid, grdsize,
               xydat, datlim, lambdax, lambday, mask, deg, maxiters1, maxiters2, datwght, calccovs))

