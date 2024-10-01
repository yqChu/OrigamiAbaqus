from abaqus import *
from abaqusConstants import *
from caeModules import *
from part import *
from PanelFunctions import *

def CreateVertCrease(panel_id1, panel_id2, hor_num, vert_num, crease_type):
    for conncetor_id in range(1, vert_num-1):
        a = mdb.models['Model-1'].rootAssembly
        n1 = a.instances[f'Part-{panel_id1+1}-1'].nodes
        n2 = a.instances[f'Part-{panel_id2+1}-1'].nodes
        if crease_type==0:
            wire = a.WirePolyLine(points=((n1[conncetor_id*hor_num], n2[(conncetor_id+1)*hor_num-1]), ), mergeType=IMPRINT, meshable=False)
        elif crease_type==1:
            wire = a.WirePolyLine(points=((n1[(conncetor_id+1)*hor_num-1], n2[(conncetor_id+1)*hor_num-1]), ), mergeType=IMPRINT, meshable=False)
        elif crease_type==2:
            wire = a.WirePolyLine(points=((n1[conncetor_id*hor_num], n2[conncetor_id*hor_num]), ), mergeType=IMPRINT, meshable=False)
        oldName = wire.name
        a.features.changeKey(fromName=oldName, toName=f'Wire-{panel_id1+1}-{panel_id2+1}-{conncetor_id+1}')
        e1 = a.edges
        edges1 = e1.getSequenceFromMask(mask=('[#1 ]', ), )
        a.Set(edges=edges1, name=f'Wire-{panel_id1+1}-{panel_id2+1}-{conncetor_id+1}-Set-1')
        region = a.sets[f'Wire-{panel_id1+1}-{panel_id2+1}-{conncetor_id+1}-Set-1']
        csa = a.SectionAssignment(sectionName=f'ConnSect-1', region=region)
        dtmid1 = a.instances[f'Part-{panel_id1+1}-1'].datums[3]
        dtmid2 = a.instances[f'Part-{panel_id2+1}-1'].datums[3]
        a.ConnectorOrientation(region=csa.getSet(), localCsys1=dtmid1,orient2sameAs1=False, localCsys2=dtmid2)

def CreateHorCrease(panel_id1, panel_id2, hor_num, vert_num):
    for conncetor_id in range(1, vert_num-1):
        a = mdb.models['Model-1'].rootAssembly
        n1 = a.instances[f'Part-{panel_id1+1}-1'].nodes
        n2 = a.instances[f'Part-{panel_id2+1}-1'].nodes
        if np.mod(panel_id2+1,5)==1:
            wire = a.WirePolyLine(points=((n1[conncetor_id*hor_num], n2[(vert_num-1)*hor_num+conncetor_id]), ), mergeType=IMPRINT, meshable=False)
        elif np.mod(panel_id2+1,5)==2:
            wire = a.WirePolyLine(points=((n1[(vert_num-1)*hor_num+conncetor_id], n2[(vert_num-1)*hor_num+conncetor_id]), ), mergeType=IMPRINT, meshable=False)
        elif np.mod(panel_id2+1,5)==3:
            wire = a.WirePolyLine(points=((n1[(conncetor_id+1)*hor_num-1], n2[vert_num*hor_num-1-conncetor_id]), ), mergeType=IMPRINT, meshable=False)
        elif np.mod(panel_id2+1,5)==4:
            wire = a.WirePolyLine(points=((n1[conncetor_id], n2[vert_num*hor_num-1-conncetor_id]), ), mergeType=IMPRINT, meshable=False)
        oldName = wire.name
        a.features.changeKey(fromName=oldName, toName=f'Wire-{panel_id1+1}-{panel_id2+1}-{conncetor_id+1}')
        e1 = a.edges
        edges1 = e1.getSequenceFromMask(mask=('[#1 ]', ), )
        a.Set(edges=edges1, name=f'Wire-{panel_id1+1}-{panel_id2+1}-{conncetor_id+1}-Set-1')
        region = a.sets[f'Wire-{panel_id1+1}-{panel_id2+1}-{conncetor_id+1}-Set-1']
        csa = a.SectionAssignment(sectionName=f'ConnSect-1', region=region)
        if np.mod(panel_id2+1,5)==1:
            dtmid1 = a.instances[f'Part-{panel_id1+1}-1'].datums[3]
        elif np.mod(panel_id2+1,5)==2:
            dtmid1 = a.instances[f'Part-{panel_id1+1}-1'].datums[2]
        elif np.mod(panel_id2+1,5)==3:
            dtmid1 = a.instances[f'Part-{panel_id1+1}-1'].datums[5]
        elif np.mod(panel_id2+1,5)==4:
            dtmid1 = a.instances[f'Part-{panel_id1+1}-1'].datums[4]
        dtmid2 = a.instances[f'Part-{panel_id2+1}-1'].datums[2]
        a.ConnectorOrientation(region=csa.getSet(), localCsys1=dtmid1,orient2sameAs1=False, localCsys2=dtmid2)