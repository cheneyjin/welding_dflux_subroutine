#==========================================================================
#                AMFlux 1.0    Copyright (C) 2023 JIN Cheng                
# 	                                                                        
#                       E-mail: Cheneyjin@gmail.com                                   
#                                                                                        
#==========================================================================
# Import modules 
# -*- coding: GBK -*-
import datetime,time
from datetime import timedelta,datetime
from abaqus import *
import part
import assembly
from abaqusConstants import *
from symbolicConstants import *
import os
import numpy as np
from numpy.linalg import det
from step import *
from interaction import *
import re
#import mesh
#==========================================================================
#   Notes:
#
#   1. This plug-in can only be used in Abaqus6.14 or above.
#   2. Only Planar Gauss, Double-ellipsoid and Cone body heat source can be
#       applied in this version.
#   3. Using mm-tonne-s units by default.
#===========================================================================
def kernel(power,vel,eff,mtype,a,b,c,a2,ratio,wtype,point1,point2,point3,point4,\
        PreStepName,FirstAMstep,CurrentPass,Length,Space,Layers,Eltype,BEle,Eles):

    if wtype == 'Line':
        T_Plain(power,vel,eff,mtype,a,b,c,a2,ratio,point1,point2,point4,waste)

    elif wtype == 'Arc':
        reply=getWarningReply('   Only Line path type can be selected in \n\
    opensource version. Contact us for full features.\n\
    E-mail: Cheneyjin@gmail.com', (YES, NO))
        if reply==YES:
            print 'Contact us for full features!'
            print 'Email: Cheneyjin@gmail.com'
            return 
        elif reply==NO:
            print 'Process terminated! Try other features.'
            return 

    if Eltype == 'Box':
        waste=ADDL(vel,point1,point2,PreStepName,FirstAMstep,CurrentPass,Space,\
                    Length,Layers)
    elif Eltype == 'Label':
        reply=getWarningReply('   Only Box type can be selected in \n\
    opensource version. Contact us for full features. \n\
    E-mail: Cheneyjin@gmail.com', (YES, NO))
        if reply==YES:
            print 'Contact us for full features!'
            print 'Email: Cheneyjin@gmail.com'
            return
        elif reply==NO:
            print 'Process terminated! Try other features.'
            return

    return

def ADDL(vel,point1,point2,PreStepName,FirstAMstep,CurrentPass,Space,Length,Layers):
    Tol=0.001
    Nsegment=int(Length//(Space*Layers))
    left = Length%(Space*Layers)
    period=Space*Layers/float(vel)
    period_left = left/float(vel)
    number = re.findall("\d+",FirstAMstep)
    Name = re.findall("\D+",FirstAMstep)
    number = int(number[0])
    Name = Name[0]
    big = 0.1
    big_left = 0.1
    if period < 0.1:
        big = period
    if period_left < 0.1:
        big_left = period_left
    ini=0.001
    ini_left=0.001
    if period < 0.001:
        ini= 0.2*period
    if period_left < 0.001:
        ini_left=0.2*period_left

    ## Add AM Steps
    vps = session.viewports[session.currentViewportName]
    Model_name = vps.displayedObject.modelName
    for i in range (Nsegment):
        if i==0:
            mdb.models[Model_name].HeatTransferStep(timePeriod=period,deltmx=1500,\
                initialInc=ini,maxInc=big,maxNumInc=1000,minInc=1e-6,\
                name=FirstAMstep,previous=PreStepName)
        else:
            mdb.models[Model_name].HeatTransferStep(timePeriod=period,deltmx=1500,\
                initialInc=ini,maxInc=big,maxNumInc=1000,minInc=1e-6,\
                name=Name+str(number+i),previous=Name+str(number+i-1))
    if left != 0.0 :
        mdb.models[Model_name].HeatTransferStep(timePeriod=period_left,deltmx=1500,\
                initialInc=ini_left,maxInc=big_left,maxNumInc=1000,minInc=1e-6,\
                name=Name+str(number+i+1),previous=Name+str(number+i))
        print str(number+i+1)+" steps have been created after step "+PreStepName+"."
    else:
        print str(number+i)+" steps have been created after step "+PreStepName+"."


    t1 = type(point1)
    t2 = type(point2)
    if t1 == tuple:
        p1=point1
    else:
        try:
            p1=point1.coordinates
        except:
            try:
                p1=point1.pointOn
            except:
                print "Type of StartPoint is:", t1
                getWarningReply(' The StartPoint is invalid!\nTry a Node or DatumPoint.',\
                        (YES,CANCEL))
                return

    if t2 == tuple:
        p2=point2
    else:
        try:
            p2=point2.coordinates
        except:
            try:
                p2=point2.pointOn
            except:
                print "Type of AlongPoint is:", t2
                getWarningReply(' The AlongPoint is invalid!\nTry a Node or DatumPoint.',\
                        (YES,CANCEL))
                return

    l12=sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2+(p2[2]-p1[2])**2)
    if left != 0.0:
        Nsegment = Nsegment +1
    pn=[[0]*3 for _ in range(Nsegment)]
    pnf=[[0]*3 for _ in range(Nsegment)]
    pnr=[[0]*3 for _ in range(Nsegment)]
    for N in range (Nsegment):
        for i in range (3):
            pn[N][i]=p1[i]+(p2[i]-p1[i])*(N+1)*Space*Layers/l12
            pnf[N][i]=p1[i]+(p2[i]-p1[i])*(N+1)*(Space*Layers+Tol)/l12
            pnr[N][i]=p1[i]+(p2[i]-p1[i])*(N+1)*(Space*Layers-Tol)/l12

    ## activation

    for i in range (Nsegment):
        pn[i]=tuple(pn[i])
        if i==0:
            ele=mdb.models[Model_name].rootAssembly.sets[CurrentPass].elements.\
                    getByBoundingCylinder(p1,pnf[i],15)
        else:
            ele=mdb.models[Model_name].rootAssembly.sets[CurrentPass].elements.\
                    getByBoundingCylinder(pnr[i-1],pnf[i],15)
        mdb.models[Model_name].ModelChange(activeInStep=True,createStepName=Name+str(number+i),\
                name='ADD'+str(number+i),region=Region(elements=ele),regionType=ELEMENTS)

    stepKeys = mdb.models[Model_name].steps.keys()
    stepValues = mdb.models[Model_name].steps.values()
    po = stepKeys.index(FirstAMstep)
    waste = 0.
    for i in range(1,po):
        waste = waste + stepValues[i].timePeriod

    return waste

def T_Plain(power,vel,eff,mtype,a,b,c,a2,ratio,point1,point2,point3,waste):
    # Obtain the coordinates of the three point
    t1 = type(point1)
    t2 = type(point2)
    t3 = type(point3)
    if t1 == tuple:
        p1=point1
    else:
        try:
            p1=point1.coordinates
        except:
            try:
                p1=point1.pointOn
            except:
                print "Type of StartPoint is:", t1
                getWarningReply(' The StartPoint is invalid!\nTry a Node or DatumPoint.'\
                        , (YES,CANCEL))
                return

    if t2 == tuple:
        p2=point2
    else:
        try:
            p2=point2.coordinates
        except:
            try:
                p2=point2.pointOn
            except:
                print "Type of AlongPoint is:", t2
                getWarningReply(' The AlongPoint is invalid!\nTry a Node or DatumPoint.'\
                        , (YES,CANCEL))
                return

    if t3 == tuple:
        p3=point3
    else:
        try:
            p3=point3.coordinates
        except:
            try:
                p3=point3.pointOn
            except:
                print "Type of ToePoint is:", t3
                getWarningReply(' The ToePoint is invalid!\nTry a Node or DatumPoint.',\
                        (YES,CANCEL))
                return
            
    print "The weld startpoint is: ", p1
    print "The weld direction is towards: ",p2
    print "The toe point(p3) is: ",p3

    Aw = (p2[1]-p1[1])*(p3[2]-p1[2])-(p2[2]-p1[2])*(p3[1]-p1[1])
    Bw = (p2[2]-p1[2])*(p3[0]-p1[0])-(p2[0]-p1[0])*(p3[2]-p1[2])
    Cw = (p2[0]-p1[0])*(p3[1]-p1[1])-(p2[1]-p1[1])*(p3[0]-p1[0])
    Dw = -(Aw*p1[0]+Bw*p1[1]+Cw*p1[2])
    dww = Aw*Aw+Bw*Bw+Cw*Cw

    Am = (p2[1]-p1[1])*Cw-(p2[2]-p1[2])*Bw
    Bm = (p2[2]-p1[2])*Aw-(p2[0]-p1[0])*Cw
    Cm = (p2[0]-p1[0])*Bw-(p2[1]-p1[1])*Aw
    Dm = -(Am*p1[0]+Bm*p1[1]+Cm*p1[2])
    dmm = Am*Am+Bm*Bm+Cm*Cm

    An = p2[0]-p1[0]
    Bn = p2[1]-p1[1]
    Cn = p2[2]-p1[2]
    Dn = -(An*p1[0]+Bn*p1[1]+Cn*p1[2])
    dnn= An*An+Bn*Bn+Cn*Cn
    dn = sqrt(dnn)

    # Write Dflux Subroutine
    vps = session.viewports[session.currentViewportName]
    Model_name = vps.displayedObject.modelName
    step = mdb.models[Model_name].steps
    stepnum = len(step)-1
    dt = datetime.now()
    ontime = dt.strftime('%Y-%m-%d %H:%M:%S')

    if os.path.exists('./amflux.for'):
        filemt1=time.localtime(os.stat('./amflux.for').st_mtime)
        t1=time.mktime(filemt1)
        filemt2=time.localtime()
        t2=time.mktime(filemt2)
        intval = timedelta(seconds=t2-t1).seconds

        if intval<=300.:
            f_old = open('./amflux.for','r+')
            lines = f_old.readlines()
            del lines[-3:]
            f_old.close()
            f_new=open('./amflux.for','w')
            f_new.write(''.join(lines))
            f_new.close()
            f=open('./amflux.for', 'a')
            f.writelines("\n      else if(kstep<= "+str(stepnum)+") then\n")
        else:
            reply=getWarningReply('The subroutine file amflux.for exists!\nOverwrite?', (YES, NO))
            if reply==YES:
                f=open('./amflux.for', 'w')
                f.writelines("c=====================================================================\n\n")
                f.writelines("c        This subroutine is generated by AMFlux v1.0                  c\n")      
                f.writelines("c                 on "+str(ontime)+"                             c\n\n")
                f.writelines("c=====================================================================\n\n")
                f.writelines("      SUBROUTINE DFLUX(FLUX,SOL,KSTEP,KINC,TIME,NOEL,NPT,COORDS,JLTYP,\n")
                f.writelines("     1     TEMP,PRESS,SNAME)\n")
                f.writelines("      INCLUDE 'ABA_PARAM.INC'\n")
                f.writelines("      DIMENSION COORDS(3),FLUX(2),TIME(2)\n")
                f.writelines("      CHARACTER*80 SNAME\n\n")
                f.writelines("      if (kstep<= "+str(stepnum)+") then\n")
            elif reply==NO:
                return
    else:
        f=open('./amflux.for', 'w')
        f.writelines("c=====================================================================\n\n")
        f.writelines("c        This subroutine is generated by AMFlux v1.0                  c\n")      
        f.writelines("c                 on "+str(ontime)+"                             c\n\n")
        f.writelines("c=====================================================================\n\n")
        f.writelines("      SUBROUTINE DFLUX(FLUX,SOL,KSTEP,KINC,TIME,NOEL,NPT,COORDS,JLTYP,\n")
        f.writelines("     1     TEMP,PRESS,SNAME)\n")
        f.writelines("      INCLUDE 'ABA_PARAM.INC'\n")
        f.writelines("      DIMENSION COORDS(3),FLUX(2),TIME(2)\n")
        f.writelines("      CHARACTER*80 SNAME\n\n")
        f.writelines("      if (kstep<= "+str(stepnum)+") then\n")

    f.writelines("          a = "+str(a)+'\n')
    f.writelines("          b = "+str(b)+'\n')

    if mtype=='Double Ellipsoid':
        f.writelines("          c = "+str(c)+'\n')
        f.writelines("          a2= "+str(a2)+'\n')
        f.writelines("          ratio= "+str(ratio)+'\n')
        fr=round(2./(1+float(ratio)),8)
        ff=2.-fr
        f.writelines("          ff= "+str(ff)+'\n')
        f.writelines("          fr= "+str(fr)+'\n')
        
    if mtype=='Cone Body':
	    f.writelines("          c = "+str(c)+'\n')

    f.writelines("          vel = "+str(vel)+'\n')
    f.writelines("          yita= "+str(eff)+'\n')
    f.writelines("          power = 1000.*yita*"+str(power)+'\n')
    f.writelines("          yy = (" +str(Am)+ "*coords(1)+\n")
    f.writelines("     &     "+str(Bm)+"*coords(2)+" + str(Cm)+'\n')
    f.writelines("     &     *coords(3)+"+str(Dm)+")**2/"+str(dmm)+'\n')
    
    f.writelines("          xn = "+str(An)+ "*coords(1)+" + str(Bn)+"*coords(2)+\n")
    f.writelines("     $     "+ str(Cn)+"*coords(3)+"+str(Dn)+"\n")
    f.writelines("          disx = xn/"+str(dn)+'\n')

    f.writelines("          vt = vel*(time(2)-"+str(waste)+")\n")
    f.writelines("          x = vt - disx\n")
    f.writelines("          xx = x*x\n")

    # Write DFLUX for Planar Gauss
    if mtype=='Planar Gauss':
        f.writelines("          qm=3*power/3.1416/a/b\n")
        f.writelines("          FLUX(1)= qm*EXP(-3*(xx/a/a+yy/b/b))\n")
    
    # Write DFLUX for Double Ellipsoid
    elif mtype=='Double Ellipsoid':
        f.writelines("          qm1=1.8663*ff*power/a/b/c\n")
        f.writelines("          qm2=1.8663*fr*power/a2/b/c\n")
        f.writelines("       zz = (" +str(Aw)+ "*coords(1)+\n")
        f.writelines("     &  "+str(Bw)+"*coords(2)+" + str(Cw)+ "*coords(3)+\n")
        f.writelines("     &  "+str(Dw)+")**2/"+str(dww)+'\n')
        f.writelines("       if (disx.GE.vt) THEN\n")
        f.writelines("        FLUX(1)=qm1*EXP(-3*(xx/a/a+yy/b/b+zz/c/c))\n")
        f.writelines("       else\n")
        f.writelines("        FLUX(1)=qm2*EXP(-3*(xx/a2/a2+yy/b/b+zz/c/c))\n")
        f.writelines("       end if\n")

    # Write DFLUX for Cone
    elif mtype=='Cone Body':
        f.writelines("       qm=9.*power*20.085537/3.1416/19.085537\n")
        f.writelines("       zz = (" +str(Aw)+ "*coords(1)+\n")
        f.writelines("     &  "+str(Bw)+"*coords(2)+" + str(Cw)+ "*coords(3)+\n")
        f.writelines("     &  "+str(Dw)+")**2/"+str(dww)+'\n')
        f.writelines("       if (zz > c*c) then\n")
        f.writelines("          FLUX(1)=0.0\n")
        f.writelines("       else\n")
        f.writelines("          r0 = a-(a-b)*zz**0.5/c\n")
        f.writelines("          FLUX(1)=qm*EXP(-3*(xx+yy)/r0/r0)/c/(a*a+a*b+b*b)\n")
        f.writelines("       end if\n")
    
    f.writelines("      end if\n")
    f.writelines("      return\n")
    f.writelines("      end\n")
    
    f.close()
    pwd=os.getcwd()
    print "The welding subroutine has been saved in '"+pwd+"\\amflux.for' successfully!"

    # Highlight points 
    highlight(point1)
    highlight(point2)
    highlight(point3)

    # Plot annotations in viewpoint
    vps = session.viewports[session.currentViewportName]
    Model_name = vps.displayedObject.modelName
    
    ar = (mdb.Arrow(name='EndArrow', startPoint=(0., 0.), endPoint=(0.,0.),startAnchor=(p1[0], p1[1], p1[2]), 
	    endAnchor=(p2[0], p2[1], p2[2]), color='#FF0000', startHeadStyle=HOLLOW_CIRCLE,
	    lineStyle=DASHED,lineThickness=THICK))
    vps.plotAnnotation(annotation=ar)
    return

