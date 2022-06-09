#==========================================================================
#                WeldFlux 2.0-dev    Copyright (C) 2022 JIN Cheng                
# 	                                                                                          
#                       E-mail: i_welding@126.com                                   
#                                                                                                    
#==========================================================================
# Import modules 
# -*- coding: GBK -*-
from datetime import *
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
import mesh
#==========================================================================
#
#       A USER DEFINED SCRIPT CODE FOR ABAQUS TO GENERATE WELDING HEAT SOURCE 
#       SUBROUTINE 'DFLUX'. 
#
#                                 Version 2.0-dev
#
#                                 developed by
#
#
#                                  JIN CHENG
#                          DALIAN JIAOTONG UNIVERSITY
#
#===========================================================================
#	Notes:
#
#	This plug-in code can only be used in Abaqus.
#
#   Only Planar Gauss, Double-ellipsoid and Cone body heat source can be applied 
#       in this version.
#   Using mm-tonne-s units by default.
#===========================================================================
def kernel(current, vol,vel,eff,mtype,a,b,c,a2,ratio,wtype,point1,point2,point3,point4,\
        PreStepName,FirstAMstep,CurrentPass,Length,Space,Layers,EnAM,Eltype,BEle,Eles):
    if EnAM == True:
        if Eltype == 'Box':
            waste=ADDL(vel,point1,point2,PreStepName,FirstAMstep,CurrentPass,Space,\
                    Length,Layers)
        elif Eltype == 'Label':
            waste= ADDC(vel,PreStepName,FirstAMstep,CurrentPass,Length,Layers,\
                    BEle,Eles)
    else:
        waste = 0.

    if wtype == 'Line':
        T_Plain(current,vol,vel,eff,mtype,a,b,c,a2,ratio,point1,point2,point4,waste,EnAM)

    elif wtype == 'Arc':
        Circle(current, vol,vel,eff,mtype,a,b,c,a2,ratio,point1,point2,point3,point4,waste,EnAM)

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
                    getByBoundingCylinder(p1,pnf[i],5)
        else:
            ele=mdb.models[Model_name].rootAssembly.sets[CurrentPass].elements.\
                    getByBoundingCylinder(pnr[i-1],pnf[i],5)
        mdb.models[Model_name].ModelChange(activeInStep=True,createStepName=Name+str(number+i),\
                name='ADD'+str(number+i),region=Region(elements=ele),regionType=ELEMENTS)

    stepKeys = mdb.models[Model_name].steps.keys()
    stepValues = mdb.models[Model_name].steps.values()
    po = stepKeys.index(FirstAMstep)
    waste = 0.
    for i in range(1,po):
        waste = waste + stepValues[i].timePeriod

    return waste


def ADDC(vel,PreStepName,FirstAMstep,CurrentPass,Length,Layers,BEle,Eles):
    vps = session.viewports[session.currentViewportName]
    Model_name = vps.displayedObject.modelName
    root = mdb.models[Model_name].rootAssembly
    Allel = root.sets[CurrentPass].elements
    Nele=len(Allel)
    AddEls=Eles*Layers
    Nsegment=int(Nele//AddEls)
    Nlayers=Nele/Eles
    left = Nele%AddEls/Eles
    period = Length/float(vel)/Nlayers*Layers
    period_left = Length/float(vel)/Nlayers*left
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
    for i in range (Nsegment):
        if i==0:
            mdb.models[Model_name].HeatTransferStep(timePeriod=period,deltmx=1500,\
                initialInc=ini,maxInc=big,maxNumInc=1000,minInc=1e-6,\
                name=FirstAMstep,previous=PreStepName)
        else:
            mdb.models[Model_name].HeatTransferStep(timePeriod=period,deltmx=1500,\
                initialInc=ini,maxInc=big,maxNumInc=1000,minInc=1e-6,\
                name=Name+str(number+i),previous=Name+str(number+i-1))
    if left != 0 :
        mdb.models[Model_name].HeatTransferStep(timePeriod=period_left,deltmx=1500,\
                initialInc=ini_left,maxInc=big_left,maxNumInc=1000,minInc=1e-6,\
                name=Name+str(number+i+1),previous=Name+str(number+i))
        print str(number+i+1)+" steps have been created after step "+PreStepName+"."
    else:
        print str(number+i)+" steps have been created after step "+PreStepName+"."

    ## activation
    E0 = Allel.getFromLabel(BEle)
    index = Allel.index(E0)
    
    for i in range (Nsegment):
        if index >= Eles:
            ele = Allel[Nele-AddEls*(i+1):Nele-AddEls*i]
        else:
            ele = Allel[i*AddEls:(i+1)*AddEls]
        mdb.models[Model_name].ModelChange(activeInStep=True,createStepName=\
                Name+str(number+i),name='ADD'+str(number+i),region=Region(elements=ele),\
                regionType=ELEMENTS)
        
    if left != 0:
        if index >= Eles:
            ele = Allel[0:Nele-AddEls*(i+1)] 
        else:
            ele = Allel[(i+1)*AddEls:Nele]
        mdb.models[Model_name].ModelChange(activeInStep=True,createStepName=\
                Name+str(number+i+1),name='ADD'+str(number+i+1),region=\
                Region(elements=ele),regionType=ELEMENTS)

    stepKeys = mdb.models[Model_name].steps.keys()
    stepValues = mdb.models[Model_name].steps.values()
    po = stepKeys.index(FirstAMstep)
    waste = 0.
    for i in range(1,po):
        waste = waste + stepValues[i].timePeriod

    return waste
    

def T_Plain(current,vol,vel,eff,mtype,a,b,c,a2,ratio,point1,point2,point3,waste,EnAM):
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
    dt = datetime.now()
    ontime = dt.strftime('%Y-%m-%d %H:%M:%S')
    if os.path.exists('./dflux.for')==True:
            reply=getWarningReply('The subroutine file exists!\nOverwrite?', (YES, NO))
            if reply==YES:
                f=open('./dflux.for', 'w')
            elif reply==NO:
                return

    else:
            f=open('./dflux.for', 'w')
    pwd=os.getcwd()
    f.writelines("c=====================================================================\n\n")
    f.writelines("c        This subrotine is generated by WeldFlux v2.0-dev              c\n")      
    f.writelines("c                 on "+str(ontime)+"                             c\n\n")
    f.writelines("c=====================================================================\n\n")
    f.writelines("      SUBROUTINE DFLUX(FLUX,SOL,KSTEP,KINC,TIME,NOEL,NPT,COORDS,JLTYP,\n")
    f.writelines("     1     TEMP,PRESS,SNAME)\n")
    f.writelines("      INCLUDE 'ABA_PARAM.INC'\n")
    f.writelines("      DIMENSION COORDS(3),FLUX(2),TIME(2)\n")
    f.writelines("      CHARACTER*80 SNAME\n\n")
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

    f.writelines("          CI = "+str(current)+'\n')
    f.writelines("          U = "+str(vol)+'\n')
    f.writelines("          vel = "+str(vel)+'\n')
    f.writelines("          yita= "+str(eff)+'\n')
    f.writelines("          power = 1000.*yita*U*CI\n")
    f.writelines("          yy = (" +str(Am)+ "*coords(1)+\n")
    f.writelines("     &     "+str(Bm)+"*coords(2)+" + str(Cm)+'\n')
    f.writelines("     &     *coords(3)+"+str(Dm)+")**2/"+str(dmm)+'\n')
    
    f.writelines("          xn = "+str(An)+ "*coords(1)+" + str(Bn)+"*coords(2)+\n")
    f.writelines("     $     "+ str(Cn)+"*coords(3)+"+str(Dn)+"\n")
    f.writelines("          disx = xn/"+str(dn)+'\n')
    if EnAM == True:
        f.writelines("          vt = vel*(time(2)-"+str(waste)+")\n")
    else:
        f.writelines("          vt = vel*time(1)\n")

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
    

    f.writelines("      return\n")
    f.writelines("      end\n")
    
    f.close()
    print "The welding subroutine has been saved in '"+pwd+"\dflux.for' successfully!"

    # Highlight points 
    highlight(point1)
    highlight(point2)
    highlight(point3)

    # Plot annotations in viewpoint
    vps = session.viewports[session.currentViewportName]
    Model_name = vps.displayedObject.modelName
    mo=mdb.models
    ass = mdb.models[Model_name].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=ass)
    session.viewports['Viewport: 1'].maximize()
    try:
        del session.viewports['Viewport: 2']
    except:
        pass

    ar = (mdb.Arrow(name='StartArrow', startPoint=(35., 30.), startAnchor=(p1[0], 
	    p1[1], p1[2]), endAnchor=(p1[0], p1[1], p1[2]), color='#FFFFFF', 
	    lineThickness=MEDIUM))
    session.viewports['Viewport: 1'].plotAnnotation(annotation=ar)
    t = (mdb.Text(name='StartPoint', text='StartPoint', offset=(35, 30.), 
	 anchor=(p1[0], p1[1], p1[2]), font='-*-arial-bold-r-normal-*-*-120-*-*-p-*-*-*', 
	 backgroundStyle=OTHER, backgroundColor='#FF0000', box=ON))
    session.viewports['Viewport: 1'].plotAnnotation(annotation=t)
    ar = (mdb.Arrow(name='AlongArrow', startPoint=(-25., 40.), startAnchor=(p2[0], p2[1], p2[2]), 
	    endAnchor=(p2[0], p2[1], p2[2]), color='#FFFFFF', lineThickness=MEDIUM))
    session.viewports['Viewport: 1'].plotAnnotation(annotation=ar)
    t = (mdb.Text(name='AlongPoint', text='AlongPoint', offset=(-25., 40.), anchor=(p2[0], p2[1], p2[2]), 
	    referencePoint=BOTTOM_CENTER, font='-*-arial-bold-r-normal-*-*-120-*-*-p-*-*-*', 
	    backgroundStyle=OTHER, backgroundColor='#0000FF', box=ON))
    session.viewports['Viewport: 1'].plotAnnotation(annotation=t)
    ar = (mdb.Arrow(name='VerticalArrow', startPoint=(18., 43.), startAnchor=(p3[0], p3[1], p3[2]), 
		    endAnchor=(p3[0], p3[1], p3[2]), color='#FFFFFF', lineThickness=MEDIUM))
    session.viewports['Viewport: 1'].plotAnnotation(annotation=ar)
    t = (mdb.Text(name='ToePoint', text='ToePoint', offset=(18., 43.), anchor=(p3[0], p3[1], p3[2]), 
		    referencePoint=BOTTOM_CENTER, font='-*-arial-bold-r-normal-*-*-120-*-*-p-*-*-*', 
		    backgroundStyle=OTHER, backgroundColor='#FF7F00', box=ON))
    session.viewports['Viewport: 1'].plotAnnotation(annotation=t)
    ar = (mdb.Arrow(name='EndArrow', startPoint=(0., 0.), endPoint=(0.,0.),startAnchor=(p1[0], p1[1], p1[2]), 
	    endAnchor=(p2[0], p2[1], p2[2]), color='#FF0000', startHeadStyle=HOLLOW_CIRCLE,
	    lineStyle=DASHED,lineThickness=THICK))
    session.viewports['Viewport: 1'].plotAnnotation(annotation=ar)
    return

def Circle(current, vol,vel,eff,mtype,a,b,c,a2,ratio,point1,point2,point3,point4,waste,EnAM):
    t1 = type(point1)
    t2 = type(point2)
    t3 = type(point3)
    t4 = type(point4)
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
                getWarningReply(' The StartPoint is invalid!\nTry a Node or DatumPoint.', (YES,CANCEL))
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
                print "Type of AlongPoint1 is:", t2
                getWarningReply(' The AlongPoint1 is invalid!\nTry a Node or DatumPoint.', (YES,CANCEL))
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
                print "Type of AlongPoint2 is:", t3
                getWarningReply(' The AlongPoint2 is invalid!\nTry a Node or DatumPoint.', (YES,CANCEL))
                return

    if t4 == tuple:
        p4=point4
    else:
        try:
            p4=point4.coordinates
        except:
            try:
                p4=point4.pointOn
            except:
                print "Type of ToePoint is:", t4
                getWarningReply(' The ToePoint is invalid!\nTry a Node or DatumPoint.', (YES,CANCEL))
                return
            
    print "The weld Startpoint is: ", p1
    print "The First point on weld arc is: ",p2
    print "The Second point on weld arc is ",p3
    print "The weld Toe point is: ",p4

    o,r,normal=points2circle(p1,p2,p3)
    r = round(r,4)

    op1 = p1 - o
    op2 = p2 - o
    op3 = p3 - o
    angle = getAngle(normal,op1,op2)
                
    bv = np.cross(normal, op1)  
    av = op1 / np.linalg.norm(op1) 
    bv = bv / np.linalg.norm(bv)
    o = np.round(o,8)
    av = np.round(av,4)
    bv = np.round(bv,4)

    p1x = str(o[0])+'+'+str(r*av[0])+'*cos(theta)+'+str(r*bv[0])+'*sin(theta)'
    p1y = str(o[1])+'+'+str(r*av[1])+'*cos(theta)+'+str(r*bv[1])+'*sin(theta)'
    p1z = str(o[2])+'+'+str(r*av[2])+'*cos(theta)+'+str(r*bv[2])+'*sin(theta)'

    p2x = str(o[0])+'+'+str(2*r*av[0])+'*cos(theta2)+'+str(2*r*bv[0])+'*sin(theta2)'
    p2y = str(o[1])+'+'+str(2*r*av[1])+'*cos(theta2)+'+str(2*r*bv[1])+'*sin(theta2)'
    p2z = str(o[2])+'+'+str(2*r*av[2])+'*cos(theta2)+'+str(2*r*bv[2])+'*sin(theta2)'


    d = point2area(p1,p2,p3,p4)
    n = np.linalg.norm(normal)
    o1=np.array([o[0]+d*normal[0]/n,o[1]+d*normal[1]/n,o[2]+d*normal[2]/n])
    o1p4= p4 - o1
    r1 = np.linalg.norm(o1-p4) 

    b1 = np.cross(normal, o1p4)  
    a1 = o1p4 / np.linalg.norm(o1p4) 
    b1 = b1 / np.linalg.norm(b1) 
    o1 = np.round(o1,8)
    a1 = np.round(a1,4)
    r1 = np.round(r1,4)
    b1 = np.round(b1,4)

    p3x = str(o1[0])+'+'+str(r1*a1[0])+'*cos(theta)+'+str(r1*b1[0])+'*sin(theta)'
    p3y = str(o1[1])+'+'+str(r1*a1[1])+'*cos(theta)+'+str(r1*b1[1])+'*sin(theta)'
    p3z = str(o1[2])+'+'+str(r1*a1[2])+'*cos(theta)+'+str(r1*b1[2])+'*sin(theta)'

    # Write Dflux Subroutine
    dt = datetime.now()
    ontime = dt.strftime('%Y-%m-%d %H:%M:%S')
    if os.path.exists('./dflux.for')==True:
            reply=getWarningReply('The subroutine file exists!\nOverwrite?', (YES, NO))
            if reply==YES:
                f=open('./dflux.for', 'w')
            elif reply==NO:
                return

    else:
            f=open('./dflux.for', 'w')
    f.writelines("c=====================================================================\n\n")
    f.writelines("c        This subrotine is generated by WeldFlux v2.0-dev              c\n")      
    f.writelines("c                 on "+str(ontime)+"                             c\n\n")
    f.writelines("c=====================================================================\n\n")
    f.writelines("      INCLUDE 'dis.inc'\n")
    f.writelines("      SUBROUTINE DFLUX(FLUX,SOL,KSTEP,KINC,TIME,NOEL,NPT,COORDS,JLTYP,\n")
    f.writelines("     1     TEMP,PRESS,SNAME)\n")
    f.writelines("      use dis\n")
    f.writelines("      INCLUDE 'ABA_PARAM.INC'\n")
    f.writelines("      DIMENSION COORDS(3),FLUX(2),TIME(2)\n")
    f.writelines("      CHARACTER*80 SNAME\n\n")
    f.writelines("      a = "+str(a)+'\n')
    f.writelines("      b = "+str(b)+'\n')

    if mtype=='Double Ellipsoid':
            f.writelines("      c = "+str(c)+'\n')
            f.writelines("      a2= "+str(a2)+'\n')
            f.writelines("      ratio= "+str(ratio)+'\n')
            fr=round(2./(1+float(ratio)),8)
            ff=2.-fr
            f.writelines("      ff= "+str(ff)+'\n')
            f.writelines("      fr= "+str(fr)+'\n')
            
    if mtype=='Cone Body':
            f.writelines("      c = "+str(c)+'\n\n')

    f.writelines("      CI = "+str(current)+'\n')
    f.writelines("      U = "+str(vol)+'\n')
    f.writelines("      vel = "+str(vel)+'\n')
        
    if angle < 0:
            f.writelines("      w = -vel/"+str(r)+'\n')
            if EnAM == True:
                f.writelines("      theta = w*(time(2)-"+str(waste)+')\n')
                f.writelines("      theta2 = w*(time(2)-"+str(waste)+")-3.1416/3"+'\n')
            else:
                f.writelines("      theta = w*time(1)"+'\n')
                f.writelines("      theta2 = w*time(1)-3.1416/3"+'\n')
    else:
            f.writelines("      w = vel/"+str(r)+'\n')
            if EnAM == True:
                f.writelines("      theta = w*(time(2)-"+str(waste)+')\n')
                f.writelines("      theta2 = w*(time(2)-"+str(waste)+")+3.1416/3"+'\n')
            else:
                f.writelines("      theta = w*time(1)"+'\n')
                f.writelines("      theta2 = w*time(1)+3.1416/3"+'\n')
        
        
    f.writelines("      yita= "+str(eff)+'\n')
    f.writelines("      power = 1000.*yita*U*CI\n")

    f.writelines("      p1x="+p1x+'\n')
    f.writelines("      p1y="+p1y+'\n')
    f.writelines("      p1z="+p1z+'\n')
    f.writelines("      p2x="+p2x+'\n')
    f.writelines("      p2y="+p2y+'\n')
    f.writelines("      p2z="+p2z+'\n')
    f.writelines("      p3x="+p3x+'\n')
    f.writelines("      p3y="+p3y+'\n')
    f.writelines("      p3z="+p3z+'\n\n')

    f.writelines("      CALL DISTANCE (p1x,p1y,p1z,p2x,p2y,p2z,p3x,p3y,p3z,\n")
    f.writelines("     &  Am,Bm,Cm,Dm,dmm,An,Bn,Cn,Dn,disn,Aw,Bw,Cw,Dw,dww)\n\n")
        
    f.writelines("      yy = (Am*coords(1)+Bm*coords(2)+Cm*coords(3)+Dm)**2/dmm\n")
        
    f.writelines("          xn = An*coords(1)+Bn*coords(2)+Cn*coords(3)+Dn\n")
    f.writelines("          disx = xn/disn\n")
    f.writelines("          xx = disx*disx\n")

    # Write DFLUX for Planar Gauss
    if mtype=='Planar Gauss':
            f.writelines("          qm=3*power/3.1416/a/b\n")
            f.writelines("          FLUX(1)= qm*EXP(-3*(xx/a/a+yy/b/b))\n")
        
    # Write DFLUX for Double Ellipsoid
    if mtype=='Double Ellipsoid':
            f.writelines("          qm1=1.8663*ff*power/a/b/c\n")
            f.writelines("          qm2=1.8663*fr*power/a2/b/c\n")
            f.writelines("       zz = (Aw*coords(1)+\n")
            f.writelines("     &  Bw*coords(2)+Cw*coords(3)+\n")
            f.writelines("     &  Dw)**2/dww\n")
            f.writelines("       if (disx.GE.0.0) THEN\n")
            f.writelines("        FLUX(1)=qm1*EXP(-3*(xx/a/a+yy/b/b+zz/c/c))\n")
            f.writelines("       else\n")
            f.writelines("        FLUX(1)=qm2*EXP(-3*(xx/a2/a2+yy/b/b+zz/c/c))\n")
            f.writelines("       end if\n")

    # Write DFLUX for Cone
    if mtype=='Cone Body':
            f.writelines("       qm=9.*power*20.085537/3.1416/19.085537\n")
            f.writelines("       zz = (Aw*coords(1)+\n")
            f.writelines("     &  Bw*coords(2)+Cw*coords(3)+\n")
            f.writelines("     &  Dw**2/dww\n")
            f.writelines("       if (zz > c*c) then\n")
            f.writelines("          FLUX(1)=0.0\n")
            f.writelines("       else\n")
            f.writelines("          r0 = a-(a-b)*zz**0.5/c\n")
            f.writelines("          FLUX(1)=qm*EXP(-3*(xx+yy)/r0/r0)/c/(a*a+a*b+b*b)\n")
            f.writelines("       end if\n")
    f.writelines("      return\n")
    f.writelines("      end\n\n")
    f.close()
    pwd=os.getcwd()
    print ("The welding subroutine has been saved in '"+pwd+"\dflux.for' successfully!")

    f=open('./dis.inc', 'w')
    f.writelines("      Module dis\n")
    f.writelines("        real:: Am,Bm,Cm,Dm,dmm,An,Bn,Cn,Dn,disn,Aw,Bw,Cw,Dw,dww\n")
    f.writelines("        real:: p1x,p1y,p1z,p2x,p2y,p2z,p3x,p3y,p3z\n")
    f.writelines("      contains\n")
    f.writelines("      SUBROUTINE DISTANCE (p1x,p1y,p1z,p2x,p2y,p2z,p3x,p3y,p3z,\n")
    f.writelines("     &  Am,Bm,Cm,Dm,dmm,An,Bn,Cn,Dn,disn,Aw,Bw,Cw,Dw,dww)\n\n")
    f.writelines('      Aw = (p2y-p1y)*(p3z-p1z)-(p2z-p1z)*(p3y-p1y)\n')
    f.writelines('      Bw = (p2z-p1z)*(p3x-p1x)-(p2x-p1x)*(p3z-p1z)\n')
    f.writelines('      Cw = (p2x-p1x)*(p3y-p1y)-(p2y-p1y)*(p3x-p1x)\n')
    f.writelines('      Dw = -(Aw*p1x+Bw*p1y+Cw*p1z)\n')
    f.writelines('      dww = Aw*Aw+Bw*Bw+Cw*Cw\n\n')

    f.writelines('      Am = (p2y-p1y)*Cw-(p2z-p1z)*Bw\n')
    f.writelines('      Bm = (p2z-p1z)*Aw-(p2x-p1x)*Cw\n')
    f.writelines('      Cm = (p2x-p1x)*Bw-(p2y-p1y)*Aw\n')
    f.writelines('      Dm = -(Am*p1x+Bm*p1y+Cm*p1z)\n')
    f.writelines('      dmm = Am*Am+Bm*Bm+Cm*Cm\n\n')

    f.writelines('      An = p2x-p1x\n')
    f.writelines('      Bn = p2y-p1y\n')
    f.writelines('      Cn = p2z-p1z\n')
    f.writelines('      Dn = -(An*p1x+Bn*p1y+Cn*p1z)\n')
    f.writelines('      dnn= An*An+Bn*Bn+Cn*Cn\n')
    f.writelines('      disn = sqrt(dnn)\n\n')
    f.writelines('      END subroutine DISTANCE\n')
    f.writelines('      END Module dis\n')
        
    f.close()

    # Highlight points 
    highlight(point1)
    highlight(point2)
    highlight(point3)
    highlight(point4)    

    
    return

def points2circle(p1, p2, p3):
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    num1 = len(p1)
    num2 = len(p2)
    num3 = len(p3)

    # Check inputs
    if (num1 == num2) and (num2 == num3):
        if num1 == 2:
            p1 = np.append(p1, 0)
            p2 = np.append(p2, 0)
            p3 = np.append(p3, 0)
        elif num1 != 3:
            print('Only 2D or 3D coordinate is allowed.')
            return
    else:
        print('Inconsistent dimensions of the coordinates')
        return

    # Check Collinear
    temp01 = p1 - p2
    temp02 = p3 - p2
    temp03 = np.cross(temp01, temp02)
    temp = np.dot(temp03, temp03) / np.dot(temp01, temp01) / np.dot(temp02, temp02)
    if temp < 10 ** -6:
        print('The three points are collinear!')
        return

    temp1 = np.vstack((p1, p2, p3))
    temp2 = np.ones(3).reshape(3, 1)
    mat1 = np.hstack((temp1, temp2))  

    m = +det(mat1[:, 1:])
    n = -det(np.delete(mat1, 1, axis=1))
    p = +det(np.delete(mat1, 2, axis=1))
    q = -det(temp1)
    normal = [m, n, p]

    temp3 = np.array([np.dot(p1, p1), np.dot(p2, p2), np.dot(p3, p3)]).reshape(3, 1)
    temp4 = np.hstack((temp3, mat1))
    temp5 = np.array([2 * q, -m, -n, -p, 0])
    mat2 = np.vstack((temp4, temp5))  

    A = +det(mat2[:, 1:])
    B = -det(np.delete(mat2, 1, axis=1))
    C = +det(np.delete(mat2, 2, axis=1))
    D = -det(np.delete(mat2, 3, axis=1))
    E = +det(mat2[:, :-1])

    o = -np.array([B, C, D]) / 2 / A
    r = np.sqrt(B * B + C * C + D * D - 4 * A * E) / 2 / abs(A)

    return o, r, normal

def define_area(point1, point2, point3):
    point1 = np.asarray(point1)
    point2 = np.asarray(point2)
    point3 = np.asarray(point3)
    AB = np.asmatrix(point2 - point1)
    AC = np.asmatrix(point3 - point1)
    N = np.cross(AB, AC) 
    Ax = N[0, 0]
    By = N[0, 1]
    Cz = N[0, 2]
    D = -(Ax * point1[0] + By * point1[1] + Cz * point1[2])
    return Ax, By, Cz, D

def point2area(point1, point2, point3, point4):
    Ax, By, Cz, D = define_area(point1, point2, point3)
    mod_d = Ax * point4[0] + By * point4[1] + Cz * point4[2] + D
    mod_area = np.sqrt(np.sum(np.square([Ax, By, Cz])))
    d = mod_d / mod_area
    return d

def getAngle(normal, v1,v2):
    cosangle= v1.dot(v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))
    angle = np.arccos(cosangle)
    n = np.cross(v1,v2)
    d = np.dot(n,normal)
    if d < 0:
        angle = -angle
    return angle
