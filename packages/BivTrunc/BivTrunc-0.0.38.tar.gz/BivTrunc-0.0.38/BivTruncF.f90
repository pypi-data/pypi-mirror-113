C-----------------------------------------------------------------------
C The BivTrunc Procedure
C Chad M. Schafer
C Department of Statistics, Carnegie Mellon University
C cschafer@stat.cmu.edu
C Work supported by NSF Grants #0434343 and #0240019
C This was originally developed in 2007, but was updated in 2021




      subroutine BivTruncF(xd,np,resx,resy,deg,xlim,lambdax,lambday,
     *       mask,
     *       bivest,maxiters1,maxiters2,grdcov,grdest,grdsize,lvout,
     *       fits,verbose,info,lscv,likecv,likelihood,datwght,mask2,
     *       resx2,resy2,fpr,gpr,theta,setheta,calccovs)

      implicit none

      double precision, intent(in) :: xd(np,2)
      integer, intent(in) :: np
      integer, intent(in) :: resx,resy
      integer, intent(in) :: deg
      double precision, intent(in) :: xlim(2,2)
      double precision, intent(inout) :: lambdax(resx)
      double precision, intent(inout) :: lambday(resy)
      logical, intent(in) :: mask(resx,resy)
      double precision, intent(out) :: bivest(resx,resy)
      integer, intent(in) :: maxiters1,maxiters2
      double precision, intent(out) :: 
     *   grdcov(grdsize*grdsize,grdsize*grdsize)
      double precision, intent(out) :: grdest(grdsize,grdsize)
      integer, intent(in) :: grdsize
      double precision, intent(out) :: lvout(np)
      double precision, intent(out) :: fits(np)
      logical, intent(in) :: verbose
      integer, intent(out) :: info
      double precision, intent(out) :: lscv,likecv,likelihood
      double precision, intent(in) :: datwght(np)
      logical, intent(in) :: mask2(resx2,resy2)
      integer, intent(in) :: resx2,resy2
      double precision, intent(out) :: fpr(resx)
      double precision, intent(out) :: gpr(resy)
      double precision, intent(out) :: theta,setheta
      logical, intent(in) :: calccovs


      double precision sumxy

      double precision holdscl

      double precision Kernel
      double precision tol
      integer info2

      double precision, allocatable :: lhsx(:,:)
      double precision, allocatable :: lhsy(:,:)
      double precision, allocatable :: intmatx(:,:,:)
      double precision, allocatable :: intmaty(:,:,:)
      double precision, allocatable :: Xmatx(:,:,:)
      double precision, allocatable :: Xmaty(:,:,:)
      double precision, allocatable :: coefsx(:,:)
      double precision, allocatable :: coefsy(:,:)

      double precision, allocatable :: xymat(:,:)
      double precision, allocatable :: A(:)
      double precision, allocatable :: xg(:)
      double precision, allocatable :: yg(:)
      double precision, allocatable :: hpr(:,:)
      double precision, allocatable :: offsetx(:,:)
      double precision, allocatable :: offsety(:,:)
      double precision, allocatable :: m1(:)
      double precision, allocatable :: normconstx(:)
      double precision, allocatable :: normconsty(:)
      double precision, allocatable :: datnormconst(:,:)
      double precision, allocatable :: WZW(:,:)
      double precision, allocatable :: grad(:,:)
      double precision, allocatable :: grad2(:,:)
      double precision, allocatable :: mj(:,:)
      double precision, allocatable :: dlj(:)
      double precision, allocatable :: graddlj(:,:)
      double precision, allocatable :: summj(:)
      double precision, allocatable :: betacovmat(:,:)
      double precision, allocatable :: trans(:,:)
      double precision, allocatable :: hold(:)
      double precision xval,yval
      double precision nconstx,nconsty
      double precision datnormconsttmp(2)
      double precision inlscvregion
      double precision neff
      integer jj


      double precision bfa,bfb
    
      integer i,j,k

      integer x,y
      integer u,ud,ud2,v,row,col,vd,vd2
      double precision, allocatable :: axK(:)
      double precision, allocatable :: byK(:)
      double precision hxy,sclx,scly
      integer numpar,pos

      integer lwork
      double precision, allocatable :: work(:)
      integer, allocatable :: iwork(:)

      double precision vl,vu,abstol
      integer il,iu,numeigsfnd
      double precision, allocatable :: eigvals(:)
      double precision, allocatable :: eigvecs(:,:)
      integer, allocatable :: ifail(:)


C neff is the "effective sample size"
C over which the lscv is calcualted

      neff = sum(datwght)


      tol = dble(0.00000000001)
      allocate(A((deg+2)))
      allocate(m1((deg+2)))
      allocate(datnormconst(np,2))

      allocate(lhsx((deg+1),resx))
      allocate(lhsy((deg+1),resy))
      allocate(intmatx((deg+2),resx,resx))
      allocate(intmaty((deg+2),resy,resy))
      allocate(Xmatx(resx,(deg+1),resx))
      allocate(Xmaty(resy,(deg+1),resy))

      allocate(coefsx((deg+1),resx))
      allocate(coefsy((deg+1),resy))
      allocate(xg(resx))
      allocate(yg(resy))
      allocate(offsetx((deg+1),resx))
      allocate(offsety((deg+1),resy))
      allocate(hpr(resx,resy))
      allocate(normconstx(resx))
      allocate(normconsty(resy))


      if(verbose) then
         write(*,'(A)') 'Building Matrices'
      endif

      sumxy = sum(datwght*xd(:,1)*xd(:,2))/sum(datwght)


C Scale lambdax and lambday

      lambdax = lambdax * (xlim(2,1)-xlim(1,1))
      lambday = lambday * (xlim(2,2)-xlim(1,2))


C Build xg and yg
C Note that now, xo and xg are the same since gp=res

      do j=1,resx
        xg(j) = xlim(1,1) + (xlim(2,1)-xlim(1,1))*
     *        dble(j-1)/dble(resx) + 
     *        (xlim(2,1)-xlim(1,1))/dble(resx)/dble(2.0)
      enddo

      do j=1,resy
        yg(j) = xlim(1,2) + (xlim(2,2)-xlim(1,2))*
     *        dble(j-1)/dble(resy) + 
     *        (xlim(2,2)-xlim(1,2))/dble(resy)/dble(2.0)
      enddo

C Find the normalizing constants

      normconstx = dble(0.0)
      normconsty = dble(0.0)

      do i=1,resx
         do j=1,resx
            normconstx(i) = normconstx(i) + 
     *          Kernel((xg(i)-xg(j))/lambdax(j))
         enddo
         normconstx(i) = normconstx(i)*
     *            (xlim(2,1)-xlim(1,1))/dble(resx)
      enddo

      do i=1,resy
         do j=1,resy
            normconsty(i) = normconsty(i) + 
     *          Kernel((yg(i)-yg(j))/lambday(j))
         enddo
         normconsty(i) = normconsty(i)*
     *            (xlim(2,2)-xlim(1,2))/dble(resy)
      enddo

      datnormconst = dble(0.0)

      do i=1,np
         do j=1,resx
            datnormconst(i,1) = datnormconst(i,1) + 
     *          Kernel((xd(i,1)-xg(j))/lambdax(j))
         enddo
         datnormconst(i,1) = datnormconst(i,1)*
     *                 (xlim(2,1)-xlim(1,1))/dble(resx)
      enddo

      do i=1,np
         do j=1,resy
            datnormconst(i,2) = datnormconst(i,2) + 
     *          Kernel((xd(i,2)-yg(j))/lambday(j))
         enddo
         datnormconst(i,2) = datnormconst(i,2)*
     *                 (xlim(2,2)-xlim(1,2))/dble(resy)
      enddo


C Build xymat

      allocate(xymat(resx,resy))

      do i=1,resx
         do j=1,resy
            xymat(i,j) = xg(i)*yg(j)
         enddo
      enddo

C Build lhsx and lhsy
    
      lhsx = dble(0.0)
      lhsy = dble(0.0)

      i=1
         do j=1,resx
            do k=1,np
               call Avec((xd(k,i)-xg(j))/lambdax(j),A,deg)
               lhsx(:,j) = lhsx(:,j) + 
     *          Kernel((xd(k,i)-xg(j))/lambdax(j))/datnormconst(k,i)*
     *                A(1:(deg+1))*datwght(k)
            enddo
            if(sum(lhsx(:,j)) .eq. 0.0) then
               print *,"WARNING: lhsx equals zero!!!",j,i
               lhsx(:,j) = 0.000000001
            endif
         enddo
c     enddo

      i=2
         do j=1,resy
            do k=1,np
               call Avec((xd(k,i)-yg(j))/lambday(j),A,deg)
               lhsy(:,j) = lhsy(:,j) + 
     *          Kernel((xd(k,i)-yg(j))/lambday(j))/datnormconst(k,i)*
     *                A(1:(deg+1))*datwght(k)
            enddo
            if(sum(lhsy(:,j)) .eq. 0.0) then
               print *,"WARNING: lhsy equals zero!!!",j,i
               lhsy(:,j) = 0.000000001
            endif
         enddo
c     enddo

      lhsx = lhsx / sum(datwght)
      lhsy = lhsy / sum(datwght)

 
C Build intmatx and inmaty, without offset term

         do j=1,resx
            do k=1,resx
               call Avec((xg(k)-xg(j))/lambdax(j),A,(deg+1))
               intmatx(1:(deg+2),k,j) = Kernel((xg(k)-xg(j))/
     *            lambdax(j))/normconstx(k)*A
            enddo
         enddo

         do j=1,resy
            do k=1,resy
               call Avec((yg(k)-yg(j))/lambday(j),A,(deg+1))
               intmaty(1:(deg+2),k,j) = Kernel((yg(k)-yg(j))/
     *            lambday(j))/normconsty(k)*A
            enddo
         enddo


C Build Xmatx and Xmaty
      
      do j=1,resx
         do k=1,resx
            call Avec((xg(k)-xg(j)),Xmatx(k,:,j),deg)
         enddo
      enddo

      do j=1,resy
         do k=1,resy
            call Avec((yg(k)-yg(j)),Xmaty(k,:,j),deg)
         enddo
      enddo


C Initialize coefsx and coefsy
     
      coefsx = 0.0
      coefsy = 0.0


C Initialize fpr, gpr, hpr
    

      call LocDenWrap(fpr,gpr,hpr,bivest,resx,resy,lhsx,lhsy,
     *       theta,xymat,xlim,
     *       coefsx,coefsy,maxiters1,verbose,mask,maxiters2,
     *       deg,offsetx,offsety,Xmatx,Xmaty,
     *       intmatx(1:(deg+1),1:resx,1:resx),
     *       intmaty(1:(deg+1),1:resy,1:resy),
     *       sumxy,info)


      deallocate(lhsx)
      deallocate(lhsy)
      deallocate(intmatx)
      deallocate(intmaty)
      deallocate(Xmatx)
      deallocate(Xmaty)
      deallocate(A)
      deallocate(offsetx)
      deallocate(offsety)
      deallocate(m1)
      deallocate(xymat)



      sclx = (xlim(2,1)-xlim(1,1))/dble(resx)
      scly = (xlim(2,2)-xlim(1,2))/dble(resy)

C Calculate the standard errors

      if(calccovs) then

      numpar = (deg+1)*(resx+resy) + 1
      allocate(WZW(numpar,numpar))
      allocate(grad(numpar,numpar))
      allocate(grad2(numpar,numpar))
      allocate(axK(resx))
      allocate(byK(resy))
      WZW = dble(0.0)
      grad = dble(0.0)
     
C Build mj()

      allocate(mj(np,numpar))

C TAKE A LOOK HERE

      mj = dble(0.0)

      do i=1,np
          pos = 0
          do u=1,resx
             do ud=1,(deg+1)
                pos = pos + 1
                mj(i,pos) = (xd(i,1)-xg(u))**(dble(ud-1))*sclx*
     *             Kernel((xd(i,1)-xg(u))/lambdax(u))/
     *              datnormconst(i,1)
             enddo
          enddo 
          do u=1,resy
             do ud=1,(deg+1)
                pos = pos + 1
                mj(i,pos) = (xd(i,2)-yg(u))**(dble(ud-1))*scly*
     *             Kernel((xd(i,2)-yg(u))/lambday(u))/
     *               datnormconst(i,2)
             enddo
          enddo 
          pos = pos + 1
          mj(i,pos) = xd(i,1)*xd(i,2)
      enddo 

      allocate(dlj(numpar))
      dlj = 0.0

C Building the matrix grad

      grad = dble(0.0)

C Loop over (x,y) pairs
      do x=1,resx
         do y=1,resy
            if(mask(x,y)) then
               WZW = dble(0.0)

C Find hxy
               hxy = dexp(hpr(x,y))

C Find axK() and byK()
                
               do u=1,resx
                  bfa = 0.0
                  do i=1,(deg+1)
                     bfa = bfa + coefsx(i,u)*
     *                    ((xg(x)-xg(u))**dble(i-1))
                  enddo
                  axK(u) = dexp(bfa)*sclx*
     *             Kernel((xg(x)-xg(u))/lambdax(u))/normconstx(x)
               enddo

               do u=1,resy
                  bfb = 0.0
                  do i=1,(deg+1)
                     bfb = bfb + coefsy(i,u)*
     *                    ((yg(y)-yg(u))**dble(i-1))
                  enddo
                  byK(u) = dexp(bfb)*scly*
     *             Kernel((yg(y)-yg(u))/lambday(u))/normconsty(y)
               enddo

C CAREFUL HERE: CHECK THE row and col  !!!!!!

               row = 0
               do u=1,resx
                  do ud=1,(deg+1)
                     row = row + 1
                     do ud2=ud,(deg+1)
                        col = row+ud2-ud
C Take inner product of (row,row+ud2-ud)
                        do i=1,resy
                           WZW(row,col) = WZW(row,col) + 
     *                            axK(u)*byK(i)*hxy
     *                            *((xg(x)-xg(u))**dble(ud-1))
     *                            *((xg(x)-xg(u))**dble(ud2-1))
                        enddo
                     enddo
C Now inner products with b's
                     do v=1,resy
                        do vd=1,(deg+1)
                           col = (deg+1)*resx + (v-1)*(deg+1) + vd
                              WZW(row,col) =
     *                            axK(u)*byK(v)*hxy
     *                            *((xg(x)-xg(u))**dble(ud-1))
     *                            *((yg(y)-yg(v))**dble(vd-1))
                        enddo
                     enddo
C Inner product with ones
                     col = numpar
                     do i=1,resy
                        WZW(row,col) = WZW(row,col) + 
     *                         axK(u)*byK(i)*hxy
     *                         *((xg(x)-xg(u))**dble(ud-1))
     *                         *xg(x)*yg(y)
                     enddo

                  enddo
               enddo 

C Now inner products of b's with themselves
               do v=1,resy
                  do vd=1,(deg+1)
                     row = row + 1
                     do vd2=vd,(deg+1)
                        col = row+vd2-vd
C Take inner product of (row,row+vd2-vd)
                        do i=1,resx
                           WZW(row,col) = WZW(row,col) + 
     *                            axK(i)*byK(v)*hxy
     *                            *((yg(y)-yg(v))**dble(vd-1))
     *                            *((yg(y)-yg(v))**dble(vd2-1))
c    *                            *sclx
                        enddo
                     enddo

C Inner product with ones
                     col = numpar
                     do i=1,resx
                        WZW(row,col) = WZW(row,col) + 
     *                         axK(i)*byK(v)*hxy
     *                         *((yg(y)-yg(v))**dble(vd-1))
     *                         *xg(x)*yg(y)
                     enddo

                  enddo
               enddo

C Fill in the bottom corner entry (the theta,theta entry)
               do u=1,resx
                  do v=1,resy
                     WZW(numpar,numpar) = WZW(numpar,numpar) +
     *                   axK(u)*byK(v)*hxy
     *                   *((xg(x)*yg(y))**dble(2.0))
                  enddo
               enddo

               grad = grad + WZW
                
            endif
         enddo
      enddo

      grad = grad *sclx * scly*dble(-1.0)


C Do the "shift" for the restriction
C No need to shift dlj, since sum of a0j is already zero

      do u=1,resx
         row = (u-1)*(deg+1) + 1
         do v=u,resx
            col = (v-1)*(deg+1) + 1
            grad(row,col) = grad(row,col) - dble(2.0)*sclx*sclx
         enddo
      enddo


C Find eigenvalues of the matrix grad
C This is not necessary, I was using it for diagnostic purposes. It
C is now skipped

      if(1 == 0) then
         numeigsfnd = numpar
         vl = 0.0
         vu = 1.0
         il = 1
         iu = numeigsfnd
         abstol = dble(-1.0)
         allocate(eigvals(numpar))
         allocate(eigvecs(numpar,numeigsfnd))
         lwork = 100000
         allocate(work(lwork))
         allocate(iwork(5*numpar))
         allocate(ifail(numpar))

         call dsyevx('V','I','U',numpar,grad,numpar,vl,vu,il,iu,
     *     abstol,numeigsfnd,eigvals,eigvecs,numpar,work,lwork,
     *     iwork,ifail,info2)

         print *,'dsyevx: ',info2


         do i=1,numeigsfnd
            print *,i,eigvals(i)
         enddo
      endif


C Invert -grad

      grad = grad * dble(-1.0)

      call dpotrf('U',numpar,grad,numpar,info2)
      if(info2 .ne. 0) then
         print *,'Problem with dpotrf:', info2
         stop
      endif
      call dpotri('U',numpar,grad,numpar,info2)
      if(info2 .ne. 0) then
         print *,'Problem with dpotri:', info2
         stop
      endif

      grad = grad * dble(-1.0)

C For each observation, calculate gradinv times dlj, graddlj


      allocate(summj(numpar))
      allocate(graddlj(numpar,np))

      summj = dble(0.0)
      do j=1,numpar
         do i=1,np
            summj(j) = summj(j) + datwght(i)*mj(i,j)
         enddo
      enddo
      summj = summj / dble(neff)

c     summj = sum(mj,1)/dble(np)
      graddlj = 0.0


      do i=1,np

C Up to now, the only purpose of dlj was to verify that it equals
C mj. Now we will find the real dlj

         dlj = mj(i,:) - summj
         do row=1,numpar
            do col=1,numpar
               if(row .gt. col) then
                  graddlj(row,i) = graddlj(row,i) + 
     *               grad(col,row)*dlj(col)
               else
                  graddlj(row,i) = graddlj(row,i) + 
     *               grad(row,col)*dlj(col)
               endif
            enddo
         enddo
      enddo


C Find the transform mat, which maps from the raw parameters
C to the actual observations. 

      allocate(trans(grdsize**2,numpar))

      row = 0
      do x=1,grdsize
         xval = xlim(1,1) + 
     *         (xlim(2,1)-xlim(1,1))*dble(x-1)/dble(grdsize)
     *          + (xlim(2,1)-xlim(1,1))/dble(2.0)/dble(grdsize)
         do y=1,grdsize
            row = row + 1
            yval = xlim(1,2) + 
     *         (xlim(2,2)-xlim(1,2))*dble(y-1)/dble(grdsize)
     *         + (xlim(2,2)-xlim(1,2))/dble(2.0)/dble(grdsize)

            hxy = dexp(xval*yval*theta)

            nconstx = 0.0
            nconsty = 0.0
            do j=1,resx
               nconstx = nconstx + 
     *             Kernel((xval-xg(j))/lambdax(j))
            enddo
            nconstx = nconstx*(xlim(2,1)-xlim(1,1))/dble(resx)
            do j=1,resy
               nconsty = nconsty + 
     *             Kernel((yval-yg(j))/lambday(j))
            enddo
            nconsty = nconsty*(xlim(2,2)-xlim(1,2))/dble(resy)


            do u=1,resx
               bfa = 0.0
               do i=1,(deg+1)
                  bfa = bfa + coefsx(i,u)*
     *                 ((xval-xg(u))**dble(i-1))
               enddo
               axK(u) = dexp(bfa)*sclx*
     *          Kernel((xval-xg(u))/lambdax(u))/nconstx
            enddo

            do u=1,resy
               bfb = 0.0
               do i=1,(deg+1)
                  bfb = bfb + coefsy(i,u)*
     *                 ((yval-yg(u))**dble(i-1))
               enddo
               byK(u) = dexp(bfb)*scly*
     *             Kernel((yval-yg(u))/lambday(u))/nconsty
            enddo

            grdest(x,y) = sum(axK)*sum(byK)*hxy
            col = 0
            do u=1,resx
               do ud=1,(deg+1)
                  col = col + 1
                  trans(row,col) = ((xval-xg(u))**dble(ud-1))*
     *              axK(u)*sum(byK)*hxy
               enddo
            enddo
            do v=1,resy
               do vd=1,(deg+1)
                  col = col + 1
                  trans(row,col) = ((yval-yg(v))**dble(vd-1))*
     *              sum(axK)*byK(v)*hxy
               enddo
            enddo
            trans(row,numpar) = xval*yval*sum(axK)*sum(byK)*hxy
         enddo
      enddo


C Form the betacovmat, only store the upper triangle
 
      allocate(betacovmat(numpar,numpar))
      betacovmat = 0.0
      do i=1,numpar
         do j=i,numpar
            do k=1,np
c              betacovmat(i,j) = betacovmat(i,j) + 
c    *                      graddlj(i,k)*graddlj(j,k)
c I made this change to take the weighting into account.
c Not sure yet if it is going to work well.
               betacovmat(i,j) = betacovmat(i,j) + 
     *              datwght(k)*datwght(k)*graddlj(i,k)*graddlj(j,k)
            enddo
         enddo
      enddo

      betacovmat = betacovmat/dble(neff)/dble(neff)
      setheta = dsqrt(betacovmat(numpar,numpar))

C THIS IS THE CHANGE

c     betacovmat = grad/dble(np)*dble(-1.0)


C Form the grid covmat, it is trans * betacovmat * trans^T
C Store only upper triangle


      allocate(hold(numpar))
      grdcov = dble(0.0)

      do row=1,(grdsize**2)
         hold = dble(0.0)
         do j=1,numpar
            do i=1,numpar
               if(i .gt. j) then
                  hold(j) = hold(j) + trans(row,i)*betacovmat(j,i)
               else
                  hold(j) = hold(j) + trans(row,i)*betacovmat(i,j)
               endif
            enddo
         enddo
         do col=row,(grdsize**2)
            do i=1,numpar
               grdcov(row,col) = grdcov(row,col) + hold(i)*trans(col,i)
            enddo 
         enddo
      enddo
      deallocate(hold)
      deallocate(betacovmat)
      deallocate(trans)
     
      
C Find the leave-one-out estimators at each data point

c     graddlj = graddlj / neff * dble(-1.0)
      graddlj = graddlj * dble(-1.0)


      lvout = dble(0.0)

      do j=1,np
c        graddlj(:,j) = graddlj(:,j)*datwght(j)/(neff-datwght(j))
c        graddlj(:,j) = graddlj(:,j)/(neff-datwght(j))
         graddlj(:,j) = graddlj(:,j)/(neff-dble(1.0))
         hxy = dexp(xd(j,1)*xd(j,2)*(theta-graddlj(numpar,j)))
         do u=1,resx
            bfa = dble(0.0)
            do i=1,(deg+1)
               pos = (u-1)*(deg+1) + i
               bfa = bfa + (coefsx(i,u)-graddlj(pos,j))*
     *              ((xd(j,1)-xg(u))**dble(i-1))
            enddo
            axK(u) = dexp(bfa)*sclx*
     *       Kernel((xd(j,1)-xg(u))/lambdax(u))/datnormconst(j,1)
         enddo
         do u=1,resy 
            bfb = dble(0.0)
            do i=1,(deg+1)
               pos = resx*(deg+1) + (u-1)*(deg+1) + i
               bfb = bfb + (coefsy(i,u)-graddlj(pos,j))*
     *              ((xd(j,2)-yg(u))**dble(i-1))
            enddo
            byK(u) = dexp(bfb)*scly*
     *       Kernel((xd(j,2)-yg(u))/lambday(u))/datnormconst(j,2)
         enddo
         lvout(j) = sum(axK)*sum(byK)*hxy
c        write(*,'(I5,2F12.5)') j,lvout(j),notlvout
      enddo

C find the "fitted values" for each observation
C I am cheating and doing this by simply setting graddlj back to
C zero and reusing the code above.

      fits = dble(0.0)
      graddlj = dble(0.0)

      do j=1,np
         hxy = dexp(xd(j,1)*xd(j,2)*(theta))

         do u=1,resx
            bfa = dble(0.0)
            do i=1,(deg+1)
               bfa = bfa + (coefsx(i,u))*
     *              ((xd(j,1)-xg(u))**dble(i-1))
            enddo
            axK(u) = dexp(bfa)*sclx*
     *       Kernel((xd(j,1)-xg(u))/lambdax(u))/datnormconst(j,1)
         enddo

         do u=1,resy
            bfb = dble(0.0)
            do i=1,(deg+1)
               bfb = bfb + (coefsy(i,u))*
     *              ((xd(j,2)-yg(u))**dble(i-1))
            enddo
            byK(u) = dexp(bfb)*scly*
     *       Kernel((xd(j,2)-yg(u))/lambday(u))/datnormconst(j,2)
         enddo

         fits(j) = sum(axK)*sum(byK)*hxy
c        write(*,'(I5,2F12.5)') j,lvout(j),notlvout
      enddo

c find the estimates on a finer grid, for the purpose of calculating
c the lscv

c     open(10,file="datfile",form="formatted")
      lscv = dble(0.0)
      inlscvregion = dble(0.0)
      do j=1,resx2
         xval = xlim(1,1) + dble(j-1)/dble(resx2)*(xlim(2,1)-xlim(1,1))
     *            + (xlim(2,1)-xlim(1,1))/dble(2.0)/dble(resx2)

         datnormconsttmp(1) = dble(0.0)
         do jj=1,resx
            datnormconsttmp(1) = datnormconsttmp(1) + 
     *          Kernel((xval-xg(jj))/lambdax(jj))
         enddo
         datnormconsttmp(1) = datnormconsttmp(1)*
     *          (xlim(2,1)-xlim(1,1))/dble(resx)

      do k=1,resy2

         yval = xlim(1,2) + dble(k-1)/dble(resy2)*(xlim(2,2)-xlim(1,2))
     *            + (xlim(2,2)-xlim(1,2))/dble(2.0)/dble(resy2)

         datnormconsttmp(2) = dble(0.0)
         do jj=1,resy
            datnormconsttmp(2) = datnormconsttmp(2) + 
     *          Kernel((yval-yg(jj))/lambday(jj))
         enddo
         datnormconsttmp(2) = datnormconsttmp(2)*
     *          (xlim(2,2)-xlim(1,2))/dble(resy)
      
         hxy = dexp(xval*yval*theta)

         do u=1,resx
            bfa = dble(0.0)
            do i=1,(deg+1)
               bfa = bfa + (coefsx(i,u))*
     *              ((xval-xg(u))**dble(i-1))
            enddo
            axK(u) = dexp(bfa)*sclx*
     *       Kernel((xval-xg(u))/lambdax(u))/datnormconsttmp(1)
         enddo

         do u=1,resy
            bfb = dble(0.0)
            do i=1,(deg+1)
               bfb = bfb + (coefsy(i,u))*
     *              ((yval-yg(u))**dble(i-1))
            enddo
            byK(u) = dexp(bfb)*scly*
     *       Kernel((yval-yg(u))/lambday(u))/datnormconsttmp(2)
         enddo

         if(mask2(j,k)) then
            lscv = lscv + (sum(axK)*sum(byK)*hxy)**dble(2.0)
            inlscvregion = inlscvregion + (sum(axK)*sum(byK)*hxy)
c           write(10,'(A6,2F8.4,F15.8)') 'HERE',xval,yval,
c    *       (sum(axK)*sum(byK)*hxy)
         endif
      enddo
      enddo
c     close(10)

      inlscvregion = inlscvregion/(dble(resx2)*dble(resy2))*
     *    (xlim(2,1)-xlim(1,1))*(xlim(2,2)-xlim(1,2))
      lscv = lscv/(dble(resx2)*dble(resy2))*
     *    (xlim(2,1)-xlim(1,1))*(xlim(2,2)-xlim(1,2))
c    *    /(inlscvregion**dble(2.0))

      deallocate(WZW)
      deallocate(grad)
      deallocate(grad2)
      deallocate(axK)
      deallocate(byK)
      deallocate(dlj)
      deallocate(graddlj)
      deallocate(summj)


C Find lscv

c     lscv = sum(bivest[mask]^2)*(xlim[2]-xlim[1])*(ylim[2]-ylim[1])/(res^2) - 2*mean(lvout)
c     lscv = dble(0.0)
      likecv = dble(0.0)
      likelihood = dble(0.0)
      holdscl = dble(0.0)

      do x=1,resx
         do y=1,resy
            if(mask(x,y)) then
c              print *,x,y,bivest(x,y)
c              lscv = lscv + (dexp(bivest(x,y))**dble(2.0))
               holdscl = holdscl + bivest(x,y)
            endif
         enddo
      enddo

c     lscv = lscv/(dble(res)**dble(2.0))*
c    *    (xlim(2,1)-xlim(1,1))*(xlim(2,2)-xlim(1,2))
c    *    - dble(2.0)*sum(lvout)/dble(np)
c     lscv = lscv*(xlim(2,1)-xlim(1,1))*(xlim(2,2)-xlim(1,2))/
c    *    (dble(res)**2.0) - dble(2.0)*sum(lvout)/dble(np)
c     print *,holdscl,sum(lvout),lscv,np

      likecv = dble(0.0)

c take out this line
      likelihood = lscv

      do i=1,np
c        lscv = lscv - dble(2.0)*lvout(i)/dble(np)
         lscv = lscv - dble(2.0)*lvout(i)*datwght(i)/dble(neff)


c the correct versions     
         likecv = likecv + datwght(i)*dlog(lvout(i))/neff
c        likelihood = likelihood + datwght(i)*dlog(fits(i))/neff
      enddo

      endif

      deallocate(normconstx)
      deallocate(normconsty)
      deallocate(xg)
      deallocate(yg)
      deallocate(coefsx)
      deallocate(coefsy)
      deallocate(hpr)

      return
      end





      subroutine LocDenWrap(fpr,gpr,hpr,cur,resx,resy,lhsx,lhsy,
     *    theta,xymat,xlim,
     *    coefsx,coefsy,maxiters1,verbose,mask,maxiters2,
     *    deg,offsetx,offsety,Xmatx,Xmaty,
     *    intmatx,intmaty,sumxy,info)

      implicit none

c     integer myid,numprocs
      integer resx,resy
      integer deg
      integer maxiters1,maxiters2
      logical verbose
      integer info
      integer g,r
c     integer lo,hi,ierror

      double precision holdsum,holdsum2
c     integer np
c     double precision x(np,2)
      double precision theta
      double precision lhsx((deg+1),resx)
      double precision lhsy((deg+1),resy)
      double precision intmatx((deg+1),resx,resx)
      double precision intmaty((deg+1),resy,resy)
      double precision Xmatx(resx,(deg+1),resx)
      double precision Xmaty(resy,(deg+1),resy)
c     double precision xg(resx)
c     double precision yg(resy)
      double precision coefsx((deg+1),resx)
      double precision coefsy((deg+1),resy)

      double precision fpr(resx)
      double precision cur(resx,resy)
      double precision gpr(resy)
      double precision offsetx((deg+1),resx)
      double precision offsety((deg+1),resy)
      double precision hpr(resx,resy)
c     double precision normconstx(resx)
c     double precision normconsty(resy)
      logical mask(resx,resy)
c     double precision evallike

      double precision xlim(2,2)
      double precision xymat(resx,resy)
     
      double precision, allocatable :: pfpr(:)
      double precision, allocatable :: pcur(:,:)
      double precision tol
c     double precision intconst1, intconst2
c     double precision pdiff
      double precision pintconst
      double precision sumxy
      double precision holdderiv
      double precision thetaprev
      double precision stepsize
      logical posder

      integer i,j,k
      allocate(pcur(resx,resy))
      tol = dble(0.000000000000000001)
      tol = dble(0.00001)
      pintconst = dble(-9999.0)
      thetaprev = dble(-9999.0)
      pcur = dble(-9999)

C Begin the old stuff

      allocate(pfpr(resx))

      do i=1,maxiters1
         if(verbose) then
C        if(mod(i,100) .eq. 0) then
            write(*,'(A,I5)') 'Beginning Main Iteration',i
C        endif 
         endif


         do j=1,resx
            do k=1,resy
               cur(j,k) = fpr(j) + gpr(k)
            enddo
         enddo

C CHANGED
         hpr = theta*xymat
C        hpr = theta*xymat - dlog(sum(dexp(cur+theta*xymat))*
C    *      (xlim(2,1)-xlim(1,1))*(xlim(2,2)-xlim(1,2))/dble(res**2))

         if(sum(dexp(cur+hpr)) .eq. pintconst) then
c           print *,i,pintconst
c           exit
         endif

         pintconst = sum(dexp(cur+hpr))

C Fix Y direction, estimate X direction

       
         do j=1,resx
            cur(j,:) = gpr
         enddo
         cur = cur + hpr
         cur = dexp(cur)

         offsetx(1,:)= sum(cur,2,mask)*(xlim(2,2)-xlim(1,2))/dble(resy)
c    *       *normconst(:,2)
         do k=2,(deg+1)
            offsetx(k,:)=offsetx(1,:)
         enddo


         do k=1,resx
            call LocDen(lhsx(:,k),coefsx(:,k),deg,resx,
C#ifdef SIMPSCAL
C     *              intmat(1:(deg+1),1:res,k,1)*offset(1,k,1),
C     *                     Xmat(:,:,k,1),xlim(:,1),
C#else
     *              intmatx(1:(deg+1),1:resx,k)*offsetx,
     *                     Xmatx(:,:,k),
     *                     xlim(:,1),
C#endif
     *              maxiters2,tol,info)
            if(info .ne. 0) then
               print *,'Warning: Info =',info
               return
            endif
         enddo


C force sum of intercepts to be zero; otherwise, is not identifiable

         coefsx(1,:) = coefsx(1,:) - sum(coefsx(1,:))/dble(resx)


C The next line is the old way of finding fpr
C           fpr = coefs(1,:,1)
C Here is the new way
            do r=1,resx
               holdsum2 = dble(0.0)
               do g=1,resx

                  holdsum = dble(0.0)
                  do k=1,(deg+1)
c FIX HERE???? May need to adjust by (k-1)!
                     holdsum = holdsum + Xmatx(r,k,g)*coefsx(k,g)
                  enddo
                  holdsum2 = holdsum2 + intmatx(1,r,g)*
     *                      dexp(holdsum)
               enddo
               fpr(r) = dlog(holdsum2*(xlim(2,1)-xlim(1,1))/dble(resx)
c    *               *normconst(r,1)
     *               )
            enddo
C end of the new way
            
c The original scaling
c        fpr = dlog(dexp(fpr)/sum(dexp(fpr))/(xlim(2,1)-xlim(1,1))*
c    *           dble(res))

C May not need this check anymore
c        if(sum(fpr-pfpr) .eq. pdiff) then
c           exit
c        endif

         pfpr = fpr

C Fix X direction, estimate Y direction

         do j=1,resy
            cur(:,j) = fpr
         enddo
         cur = cur + hpr
         cur = dexp(cur)

         offsety(1,:)= sum(cur,1,mask)*(xlim(2,1)-xlim(1,1))/dble(resx)
         do k=2,(deg+1)
            offsety(k,:)=offsety(1,:)
         enddo

         do k=1,resy
            call LocDen(lhsy(:,k),coefsy(:,k),deg,resy,
C#ifdef SIMPSCAL
C     *              intmaty(1:(deg+1),1:resy,k)*offset(1,k,2),
C     *              Xmat(:,:,k,2),
C     *                   xlim(:,2),
C#else
     *              intmaty(1:(deg+1),1:resy,k)*offsety,
     *                   Xmaty(:,:,k),
     *                   xlim(:,2),
C#endif
     *              maxiters2,tol,info)
            if(info .ne. 0) then
               print *,'Warning: Info =',info
               return
            endif
         enddo

c The old way
c           gpr = coefs(1,:,2)
c The new way
            do r=1,resy
               holdsum2 = dble(0.0)
               do g=1,resy

                  holdsum = dble(0.0)
                  do k=1,(deg+1)
                     holdsum = holdsum + Xmaty(r,k,g)*coefsy(k,g)
                  enddo
                  holdsum2 = holdsum2 + intmaty(1,r,g)*
     *              dexp(holdsum)
               enddo
                
               gpr(r) = dlog(holdsum2*(xlim(2,2)-xlim(1,2))/dble(resy)
c    *              /normconst(r,2)
     *              )
            enddo


        
C estimate theta

            do j=1,resx
               do k=1,resy
                  cur(j,k) = fpr(j) + gpr(k)
               enddo
            enddo
     
 
            holdderiv = sumxy - 
     *         sum(sum(xymat*dexp(cur + theta*xymat),1,mask))*
     *         (xlim(2,2)-xlim(1,2))/dble(resy)*
     *         (xlim(2,1)-xlim(1,1))/dble(resx)
            if(holdderiv .lt. 0.0) then
               posder = .FALSE.
            else
               posder = .TRUE.
            endif
            stepsize = dble(1.0)

            do while(dabs(holdderiv) .gt. 0.00000000000001 
     *                .or. stepsize .gt. 0.01)
c           do while(dabs(holdderiv) .gt. 0.001 
c    *                .and. stepsize .gt. 0.01)
      
                
c              print *,holdderiv, theta, stepsize
               if(posder) then
                  theta = theta + stepsize
               else
                  theta = theta - stepsize
               endif
               holdderiv = sumxy - 
     *            sum(sum(xymat*dexp(cur + theta*xymat),1,mask))*
     *            (xlim(2,2)-xlim(1,2))/dble(resy)*
     *            (xlim(2,1)-xlim(1,1))/dble(resx)
               hpr = theta*xymat
               if(holdderiv .lt. 0.0 .and. posder) then
                  stepsize = stepsize / dble(2.0)
                  posder = .FALSE.
               endif
               if(holdderiv .gt. 0.0 .and. .not. posder) then
                  stepsize = stepsize / dble(2.0)
                  posder = .TRUE.
               endif
            enddo
c           print *,holdderiv,theta,stepsize
            if(dabs(theta-thetaprev) .lt. tol) then
c              exit
            endif
            cur = cur + theta*xymat

c           print *,dabs(theta-thetaprev),sum(dabs(pcur-cur))/
c    *            dble(resx*resy) 

            thetaprev = theta
       
c           print *,i,sum(dabs(pcur-cur))/dble(resx*resy) 
            if(sum(dabs(pcur-cur))/dble(resx*resy) .lt. tol) then
               exit
            endif
            pcur = cur


         if(i .eq. maxiters1) then
             print *,'Reach maxiters1'
         endif
      enddo

      do j=1,resx
         do k=1,resy
            cur(j,k) = fpr(j) + gpr(k)
         enddo
      enddo

      hpr = theta*xymat
      cur = cur + hpr      
      deallocate(pfpr) 
      return    
      end



C----------------------------------------------------------------------

      subroutine LocDen(lhs,coefs,deg,res,intmat,Xmat,
     *    xlim,
     *    maxiters,tol,info)

      implicit none

      integer res
      integer deg
      integer maxiters
      integer info

      double precision lhs(deg+1)
      double precision coefs(deg+1)
c     double precision xo
      double precision intmat((deg+1),res)
      double precision Xmat(res,(deg+1))
      double precision, allocatable :: rhs(:)
      double precision xlim(2)
      double precision tol

      double precision, allocatable :: hold(:)
      double precision, allocatable :: pcoefs(:)
c     double precision, allocatable :: derivs(:)
      double precision, allocatable :: derivs(:,:)
      double precision, allocatable :: dderivs(:,:)
      double precision, allocatable :: dmat(:,:,:)
      integer, allocatable :: ipiv(:)
      double precision, allocatable :: work(:)
      integer lwork

      double precision diff

      integer i,j

      allocate(rhs(deg+1))
c     allocate(derivs(deg+1))
      allocate(derivs((deg+1),(deg+1)))
      allocate(dderivs((deg+1),(deg+1)))
      allocate(hold(deg+1))
      allocate(pcoefs(deg+1))
      allocate(dmat((deg+1),res,(deg+1)))

      call FormProd(intmat(1:(deg+1),1:res),coefs,Xmat,xlim,rhs,res,deg)

      info = 0
      diff = dot_product((rhs-lhs),(rhs-lhs))
      diff = sum(dabs(coefs-pcoefs))

C Form dmat

      do i=1,(deg+1)
         do j=1,(deg+1)
            dmat(i,:,j) = Xmat(:,j)
         enddo
      enddo
      pcoefs = dble(-9999)

C Main iterations
      allocate(ipiv(deg+1))
      lwork=192
      allocate(work(lwork))

      if(sum(lhs) .eq. 0.0) then
         coefs = dble(0.0)
         coefs(1) = dble(-100.0)
      else

      tol = 0.000000000001
      tol = 0.0000001
      do i=1,maxiters
         if(diff .lt. tol) then
c        write(*,'(5F15.10,I6)') rhs(1),rhs(2),coefs(1),coefs(2),diff,i
            exit
         endif
         do j=1,(deg+1)
            call FormProd(intmat(1:(deg+1),1:res)*dmat(:,:,j),coefs,
     *               Xmat,xlim,hold,
     *               res,deg)
            derivs(:,j) = hold
         enddo
 
         call FormInv(derivs,dderivs,(deg+1),ipiv,work,lwork)
         coefs = coefs - matmul(dderivs,(rhs-lhs))

         call FormProd(intmat(1:(deg+1),1:res),coefs,Xmat,xlim,
     *        rhs,res,deg)

         diff = dot_product((rhs-lhs),(rhs-lhs))
         diff = sum(dabs(coefs-pcoefs))
         pcoefs = coefs
c        write(*,'(5F15.10,I6)') rhs(1),rhs(2),coefs(1),coefs(2),diff,i
         if(i .eq. maxiters) then
            info = 1
            exit
         endif
      enddo
      endif
       
      deallocate(rhs)
      deallocate(dmat)
      deallocate(hold)
      deallocate(derivs)
      deallocate(dderivs)
      deallocate(ipiv)
      deallocate(work)

      return
      end
  

 
C----------------------------------------------------------------------
 
      subroutine FormProd(intmat,coefs,Xmat,xlim,rhs,res,deg)

      implicit none

      integer res
      integer deg

      double precision rhs(deg+1)
      double precision coefs(deg+1)
      double precision intmat((deg+1),res)
      double precision Xmat(res,(deg+1))
      double precision xlim(2)

      double precision, allocatable :: hold1(:)

C Need the product intmat %*% exp(Xmat %*% coefs) / res * (xlim(2)-xlim(1)

      allocate(hold1(res))
      hold1 = matmul(Xmat,coefs)
      hold1 = dexp(hold1)
      rhs = matmul(intmat(1:(deg+1),1:res),hold1)*
     *      (xlim(2)-xlim(1))/dble(res)
      deallocate(hold1)

      return
      end

C----------------------------------------------------------------------
      double precision function Kernel(x)

      implicit none
      double precision x

C The Gaussian Kernel
C     Kernel = dexp(-(x**2.0)/2.0)*(0.3989423)

C The tri-cube Kernel

      if(dabs(x) < 1) then
         Kernel = (1.0-(dabs(x)**3))**3
      else
         Kernel = 0.0
      endif

      return
      end

C----------------------------------------------------------------------
      subroutine Avec(x,out,deg)

      implicit none

      integer deg
      double precision x
      double precision out(deg+1)
      integer i

      out(1) = 1.0
      do i=1,deg
         out((i+1)) = x**dble(i)
      enddo

      return
      end

C----------------------------------------------------------------------

      subroutine FormInv(A,B,n,ipiv,work,lwork)

      implicit none

      integer n      
      integer ipiv(n),info,lwork
      double precision A(n,n)
      double precision B(n,n)
      double precision work(lwork)

      if(n .gt. 2) then
         B = A
         call dgetrf(n,n,B,n,ipiv,info) 
         call dgetri(n,B,n,ipiv,work,lwork,info)
      else
         B(1,1) = A(2,2)
         B(2,2) = A(1,1)
         B(1,2) = -A(1,2)
         B(2,1) = -A(2,1)
         B = B / (A(1,1)*A(2,2)-A(2,1)*A(1,2))
      endif
 
      return
      end

C-----------------------------------------------------------------------
C yminorig <- -1.2
C ymaxorig <- 3.3

C trans <- function(x)
C {
C    -23.58 -1.215*x
C }

C ylimits <- function(x,ymin,ymax)
C {
C   hi <- pmin(19.894 - 2.303*16.08/2.5 + 2 *log(1+x - sqrt(1+x)) - log(1+x)/2,ymax)
C   lo <- pmax(19.894 - 2.303*18.934/2.5 + 2 *log(1+x - sqrt(1+x)) - log(1+x)/2,ymin)
C   hi <- pmin(19.894 - 2.303*16.5/2.5 + 2 *log(1+x - sqrt(1+x)) - log(1+x)/2,ymax)
C   lo <- pmax(19.894 - 2.303*19.2/2.5 + 2 *log(1+x - sqrt(1+x)) - log(1+x)/2,ymin)

C   hitmp <- hi
C   hi <- trans(lo)
C   lo <- trans(hitmp)

C   cbind(lo,hi)
C}
C yminorig <- -1.2
C ymaxorig <- 3.3

C ymax <-  trans(yminorig)
C ymin <- trans(ymaxorig)




      logical function maskfunc2(x,y)

      implicit none
      double precision x,y
c     double precision xlim(2,2)

c     if(((x-0.5)**2) + ((y-0.5)**2) .ge. 0.1 .and. x .ge. 0 .and.
c    *      x .le. 1 .and. y .ge. 0 .and. y .le. 1 .and. x .lt.
c    *      (y+0.1)) then
      if(x .ge. 0 .and. x .le. 1 .and. y .ge. 0 .and. y .le. 1) then
c     if(x .ge. 0 .and. x .le. 1 .and. y .ge. 0 .and. y .le. 1
c    *   .and. x .ge. (y-0.1)) then
         maskfunc2 = .TRUE.
      else
         maskfunc2 = .FALSE.
      endif

      return
      end



C----------------------------------------------------------------------

      logical function maskfunc(x,y,xlim)
     
      implicit none
      double precision x,y
      double precision xlim(2,2)
      double precision ylim(2)

      call getylim(x,ylim)
      if(x .le. xlim(2,1) .and. x .ge. xlim(1,1) .and. y .ge. xlim(1,2)
     *   .and. y .le. xlim(2,2) 
     *   .and. y .le. ylim(2) .and. y .ge. ylim(1)) then
         maskfunc = .TRUE. 
      else
         maskfunc = .FALSE.
      endif

      return
      end

      subroutine getylim(x,ylim)
      implicit none
      double precision ylim(2),hitmp,x

      ylim(2) = 19.894-2.303*16.5/2.5+2.0*dlog(1.0+x-sqrt(1.0+x))
     *    -dlog(1.0+x)/2.0
      ylim(1) = 19.894-2.303*19.2/2.5+2.0*dlog(1.0+x-sqrt(1.0+x))
     *    -dlog(1.0+x)/2.0

      hitmp = ylim(2)
      ylim(2) = -23.58 - 1.215*ylim(1)
      ylim(1) = -23.58 - 1.215*hitmp

      return
      end


C---------------------------------------------------------------------

      double precision function evallike(x,np,mask,res,cur,xlim)

      implicit none

      integer np,res
      double precision x(np,2)
      logical mask(res,res)
      double precision cur(res,res)
      double precision xlim(2,2)
      double precision outlike

      double precision, allocatable :: xg(:,:)
      double precision, allocatable :: wt1(:)
      double precision, allocatable :: wt2(:)
      double precision, allocatable :: wt3(:)
      double precision, allocatable :: wt4(:)
      integer i

      allocate(xg(np,2))

      allocate(wt1(np))
      allocate(wt2(np))
      allocate(wt3(np))
      allocate(wt4(np))

      xg(:,1) = (x(:,1)-xlim(1,1))/(xlim(2,1)-xlim(1,1))*
     *   dble(res-1)+dble(1.0)
      xg(:,2) = (x(:,2)-xlim(1,2))/(xlim(2,2)-xlim(1,2))*
     *   dble(res-1)+dble(1.0)

      wt1 = (ceiling(xg(:,1))-xg(:,1)+ceiling(xg(:,2))-xg(:,2))
     *        /dble(4.0)
      wt2 = (ceiling(xg(:,1))-xg(:,1)+xg(:,2)-floor(xg(:,2)))
     *        /dble(4.0)
      wt3 = (xg(:,1)-floor(xg(:,1))+ceiling(xg(:,2))-xg(:,2))
     *        /dble(4.0)
      wt4 = (xg(:,1)-floor(xg(:,1))+xg(:,2)-floor(xg(:,2)))
     *        /dble(4.0)
      outlike = 0.0
      do i=1,np
         outlike = outlike + cur(floor(xg(i,1)),floor(xg(i,2)))*wt1(i)
     *             + cur(floor(xg(i,1)),ceiling(xg(i,2)))*wt2(i)
     *             + cur(ceiling(xg(i,1)),floor(xg(i,2)))*wt3(i)
     *             + cur(ceiling(xg(i,1)),ceiling(xg(i,2)))*wt4(i)
      enddo

      outlike = outlike - dble(np)*dlog(sum(dexp(cur),MASK=mask))

      evallike = outlike
     
      deallocate(wt1)
      deallocate(wt2)
      deallocate(wt3)
      deallocate(wt4)
      deallocate(xg)
 
      return
      end


