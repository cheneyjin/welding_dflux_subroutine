from abaqus import *
from abaqusConstants import *
import visualization
import numpy as np

def geom(SideEdge1,SideEdge2,Leg1,Leg2,Rein,HaveBot,
        AlongPath,SetName,color,BotEdge=None):

    # check inputs

    vps = session.viewports[session.currentViewportName]
    obj = vps.displayedObject
    if type(obj)!=visualization.PartType:
        raise TypeError,'This function is only valid on unmeshed Part'

    cAll = obj.cells
    sAll = obj.allSets
    if sAll.has_key('AllBaseMat')==0:
        obj.Set(cells=cAll,name='AllBaseMat')
    if sAll.has_key(SetName):
        reply = getWarningReply("Set '"+SetName+"' already exist!\nMake sure to overwrite?", (YES,CANCEL))
        if reply == CANCEL:
            return
        
    eAll = obj.edges
    vAll =obj.vertices
    e1 = SideEdge1
    e2 = SideEdge2
    v1 = e1.getVertices()
    v2 = e2.getVertices()
    path_coo = AlongPath.pointsOn

    if HaveBot=='Yes':
        bottoms_coo = BotEdge.pointsOn
        p0_coo = bottoms_coo[0]

        for e in BotEdge:
            botv = e.getVertices()
            if list(set(v1)&set(botv))!=[]:
                comL=list(set(v1)&set(botv))[0]
            if list(set(v2)&set(botv))!=[]:
                comR=list(set(v2)&set(botv))[0]


        p0L = vAll[comL] 
        p0R = vAll[comR] 
        p0L_coo = p0L.pointOn
        p0R_coo = p0R.pointOn
        p0L_array = np.array(p0L_coo)
        p0R_array = np.array(p0R_coo)
        p0Lx,p0Ly,p0Lz = p0L_coo[0]
        p0Rx,p0Ry,p0Rz = p0R_coo[0]
    else:
        comm = list(set(v1)&set(v2))[0]
        p0 = vAll[comm]    
        p0_coo = p0.pointOn

    p0x,p0y,p0z = p0_coo[0]
    p0_array = np.array(p0_coo)

    e1Len = e1.getSize(False)
    e2Len = e2.getSize(False)
    r1 = float(Leg1)/e1Len
    r2 = float(Leg2)/e2Len
    if r1 > 1.:
        raise ValueError, 'Input error:\nLeglength1 is greater than SideEdge1.'
    if r2 > 1.:
        raise ValueError, 'Input error:\nLeglength2 is greater than SideEdge2.'
    
    # Model chang from here
    f1 = obj.DatumPointByEdgeParam(e1,parameter=r1)
    p1 = obj.datums[f1.id]
    p1_array=np.array(p1.pointOn)

    if HaveBot=='Yes':
        dis1 = np.linalg.norm(p0L_array-p1_array)
    else:
        dis1 = np.linalg.norm(p0_array-p1_array)

    if abs(dis1-Leg1) > 0.01:
        del obj.features[f1.name]
        f1 = obj.DatumPointByEdgeParam(e1,parameter=(1-r1))
        p1 = obj.datums[f1.id]

    p1_coo = p1.pointOn
    p1x,p1y,p1z = p1_coo
    
    f2 = obj.DatumPointByEdgeParam(e2,parameter=r2)
    p2 = obj.datums[f2.id]
    p2_array = np.array(p2.pointOn)
    
    if HaveBot=='Yes':
        dis2 = np.linalg.norm(p0R_array-p2_array)
    else:
        dis2 = np.linalg.norm(p0_array-p2_array)

    if abs(dis2-Leg2) > 0.01:
        del obj.features[f2.name]
        f2 = obj.DatumPointByEdgeParam(e2,parameter=(1-r2))
        p2 = obj.datums[f2.id]
    
    p2_coo = p2.pointOn
    p2x,p2y,p2z = p2_coo
    # plot top wire

    f12=obj.WirePolyLine(points=(p1,p2), mergeType=IMPRINT, meshable=ON)
    p1p2 = obj.getFeatureEdges(f12.name)
    eAll = obj.edges
    if HaveBot=='Yes':
        midL = ((0.5*(p0Lx+p1x),0.5*(p0Ly+p1y),0.5*(p0Lz+p1z)),)
        midR = ((0.5*(p0Rx+p2x),0.5*(p0Ry+p2y),0.5*(p0Rz+p2z)),)
        left_coo = eAll.getClosest(coordinates=midL)[0][0].pointOn
        right_coo = eAll.getClosest(coordinates=midR)[0][0].pointOn
        left = eAll.findAt(left_coo)
        right = eAll.findAt(right_coo)
        bots = eAll.findAt(*bottoms_coo)
        fface = obj.CoverEdges(edgeList = left+p1p2+right+bots, tryAnalytical=True)
    else:
        midL = ((0.5*(p0x+p1x),0.5*(p0y+p1y),0.5*(p0z+p1z)),)
        midR = ((0.5*(p0x+p2x),0.5*(p0y+p2y),0.5*(p0z+p2z)),)
        left_coo = eAll.getClosest(coordinates=midL)[0][0].pointOn
        right_coo = eAll.getClosest(coordinates=midR)[0][0].pointOn
        left = eAll.findAt(left_coo)
        right = eAll.findAt(right_coo)
        fface = obj.CoverEdges(edgeList = left+p1p2+right, tryAnalytical=True)
        
    face_c = ((p0x+p1x+p2x)/3.,(p0y+p1y+p2y)/3.,(p0z+p1z+p2z)/3.)
    
    eAll = obj.edges
    edges =eAll.findAt(*path_coo)
    pathEdges=edges
    
    f=obj.faces
    fweld=obj.SolidSweep(path=pathEdges, profile=f.findAt(coordinates=face_c),
            keepInternalBoundaries=ON)

    cAll = obj.cells
    cell = obj.getFeatureCells(fweld.name)
    obj.Set(cells=cell,name=SetName)

    vps.enableMultipleColors()
    vps.setColor(initialColor='#FFFFFF')
    cmap = vps.colorMappings['Set']
    cmap.updateOverrides(defaultOverrides={'AllBaseMat':(1,'#FFFFFF', 'Default','#FFFFFF'),
        SetName:(1,color,'Default',color)})
    vps.setColor(colorMapping=cmap)
    vps.disableMultipleColors()
    vps.partDisplay.geometryOptions.setValues(datumPoints=OFF)
    print "** %s has been created successfully!"%SetName

    return

