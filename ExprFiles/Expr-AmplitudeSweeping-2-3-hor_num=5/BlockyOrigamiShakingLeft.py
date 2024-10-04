# -*- coding: utf-8 -*-
import sys
sys.path.append('C:/Research/Nonreciprocity/OrigamiAbaqus')
from abaqus import *
from abaqusConstants import *
from caeModules import *
from part import *
from PanelFunctions import *
import numpy as np
import job
from CreaseFunctions import *
Mdb()

m = mdb.models['Model-1']

# mesh scale, hor_num and vert_num should be equal
hor_num = 5
vert_num = hor_num
# The whole origami's scale
x_num = 2
y_num = 3
[panels_no_interval_cyclic, panels_no_interval_cap] = PanelsNoInterval(theta=np.pi/16, sqr_diag_len=0.016, quad_diag_len=[0.016, 0.008], x_num=x_num, y_num=y_num)
panels_no_interval_cyclic = panels_no_interval_cyclic.reshape(x_num*y_num*20, 3, 3)
panels_no_interval_cap = panels_no_interval_cap.reshape(x_num*10, 3, 3)
panels_no_interval = np.concatenate((panels_no_interval_cyclic,panels_no_interval_cap), axis=0)
panels_interval = np.zeros(panels_no_interval.shape)
for panel_id in range(len(panels_no_interval[:,0,0])):
    panels_interval[panel_id] = SetInterval(panels_no_interval[panel_id], interval=0.05)
    node_labels, node_coords = PanelFromNodes(panels_interval[panel_id, 0], panels_interval[panel_id, 1], panels_interval[panel_id, 2], hor_num, vert_num)
    element_type, element_labels, element_nodes = S4ElementFromPanel(hor_num, vert_num)
    mdb.models['Model-1'].PartFromNodesAndElements(
        name='Part-{panel_id}'.format(panel_id=panel_id+1),
        dimensionality=THREE_D,
        type=DEFORMABLE_BODY,
        nodes=(node_labels, node_coords),
        elements=[[element_type, element_labels, element_nodes]]
    )

    mdb.models['Model-1'].parts['Part-{panel_id}'.format(panel_id=panel_id+1)].DatumCsysByThreePoints(name='Datum-csys-{panel_id}-A'.format(panel_id=panel_id+1), coordSysType=CARTESIAN, origin=panels_interval[panel_id,0],
    point1=panels_interval[panel_id,1], point2=panels_interval[panel_id,2])

    mdb.models['Model-1'].parts['Part-{panel_id}'.format(panel_id=panel_id+1)].DatumCsysByThreePoints(name='Datum-csys-{panel_id}-B'.format(panel_id=panel_id+1), coordSysType=CARTESIAN, origin=panels_interval[panel_id,0],
    point1=panels_interval[panel_id,2], point2=panels_interval[panel_id,1])

    mdb.models['Model-1'].parts['Part-{panel_id}'.format(panel_id=panel_id+1)].DatumCsysByThreePoints(name='Datum-csys-{panel_id}-C'.format(panel_id=panel_id+1), coordSysType=CARTESIAN, origin=panels_interval[panel_id,0],
    point1=2*panels_interval[panel_id,0]-panels_interval[panel_id,1], point2=panels_interval[panel_id,2])

    mdb.models['Model-1'].parts['Part-{panel_id}'.format(panel_id=panel_id+1)].DatumCsysByThreePoints(name='Datum-csys-{panel_id}-D'.format(panel_id=panel_id+1), coordSysType=CARTESIAN, origin=panels_interval[panel_id,0],
    point1=2*panels_interval[panel_id,0]-panels_interval[panel_id,2], point2=panels_interval[panel_id,1])

# Materials
mdb.models['Model-1'].Material(name='Material-1')
mdb.models['Model-1'].materials['Material-1'].Elastic(table=((400000000.0, 0.3),))
mdb.models['Model-1'].materials['Material-1'].Density(table=((2000.0, ), ))

# Section
mdb.models['Model-1'].HomogeneousShellSection(name='Section-1', 
    preIntegrate=OFF, material='Material-1', thicknessType=UNIFORM, 
    thickness=0.001, thicknessField='', nodalThicknessField='',
    idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT, 
    thicknessModulus=None, temperature=GRADIENT, useDensity=OFF, 
    integrationRule=SIMPSON, numIntPts=5)

# Section Assignment
for panel_id in range(len(panels_interval[:,0,0])):
    elements = mdb.models['Model-1'].parts['Part-{panel_id}'.format(panel_id=panel_id+1)].elements.getSequenceFromMask(mask=('[#ffffffff #f ]',),)
    region = mdb.models['Model-1'].parts['Part-{panel_id}'.format(panel_id=panel_id+1)].Set(elements=elements, name='Set-1')
    mdb.models['Model-1'].parts['Part-{panel_id}'.format(panel_id=panel_id+1)].SectionAssignment(region=region, sectionName='Section-1')

# Define Instance
mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
for panel_id in range(len(panels_interval[:,0,0])):
    mdb.models['Model-1'].rootAssembly.Instance(name='Part-{panel_id}-1'.format(panel_id=panel_id+1),
                                                part=mdb.models['Model-1'].parts['Part-{panel_id}'.format(panel_id=panel_id+1)],
                                                dependent=ON)

# Define ConnectorSection
mdb.models['Model-1'].ConnectorSection(name='ConnSect-1', assembledType=HINGE)
elastic_0 = connectorBehavior.ConnectorElasticity(components=(4, ), table=((
    3/(hor_num-2), ), ))
mdb.models['Model-1'].sections['ConnSect-1'].setValues(behaviorOptions =(
    elastic_0, ) )
mdb.models['Model-1'].sections['ConnSect-1'].behaviorOptions[0].ConnectorOptions(
    )

## Connector Assignment
# node 1-4 for each panel group
for panel_id in range(len(panels_interval[:,0,0])):
    if np.mod(panel_id+1,5) == 1:
        CreateVertCrease(panel_id1=panel_id, panel_id2=panel_id+3, hor_num=hor_num, vert_num=vert_num, crease_type=0)
    elif np.mod(panel_id+1,5) in (2,3,4):
        CreateVertCrease(panel_id1=panel_id, panel_id2=panel_id-1, hor_num=hor_num, vert_num=vert_num, crease_type=0)
    if panel_id<x_num*y_num*20:
        if np.mod(panel_id+1,20) in (1,6):
            CreateVertCrease(panel_id1=panel_id+13, panel_id2=panel_id, hor_num=hor_num, vert_num=vert_num, crease_type=0)
        elif np.mod(panel_id+1,20) == 2:
            CreateVertCrease(panel_id1=panel_id, panel_id2=panel_id+11, hor_num=hor_num, vert_num=vert_num, crease_type=0)
            CreateVertCrease(panel_id1=panel_id, panel_id2=panel_id+5, hor_num=hor_num, vert_num=vert_num, crease_type=1)
        elif np.mod(panel_id+1,20) == 3:
            CreateVertCrease(panel_id1=panel_id, panel_id2=panel_id+5, hor_num=hor_num, vert_num=vert_num, crease_type=2)
        elif np.mod(panel_id+1,20) == 7:
            CreateVertCrease(panel_id1=panel_id, panel_id2=panel_id+11, hor_num=hor_num, vert_num=vert_num, crease_type=0)
        elif np.mod(panel_id+1,20) in (11,16):
            if panel_id<x_num*(y_num-1)*20:
                CreateVertCrease(panel_id1=panel_id+20*x_num-7, panel_id2=panel_id, hor_num=hor_num, vert_num=vert_num, crease_type=0)
            else:
                CreateVertCrease(panel_id1=panel_id+20*x_num-10*(np.mod(panel_id, 20*x_num)//20)-7, panel_id2=panel_id, hor_num=hor_num, vert_num=vert_num, crease_type=0)
        elif np.mod(panel_id+1,20) in (12,17):
            if panel_id<x_num*(y_num-1)*20:
                CreateVertCrease(panel_id1=panel_id, panel_id2=panel_id+20*x_num-9, hor_num=hor_num, vert_num=vert_num, crease_type=0)
            else:
                CreateVertCrease(panel_id1=panel_id, panel_id2=panel_id+20*x_num-10*(np.mod(panel_id, 20*x_num)//20)-9, hor_num=hor_num, vert_num=vert_num, crease_type=0)
    if panel_id>19 and panel_id < x_num*y_num*20:
        if np.mod(panel_id+1, 20) == 1 and np.mod(panel_id//20,x_num)!=0:
            CreateVertCrease(panel_id1=panel_id, panel_id2=panel_id-15, hor_num=hor_num, vert_num=vert_num, crease_type=2)
        elif np.mod(panel_id+1, 20) == 4 and np.mod(panel_id//20,x_num)!=0:
            CreateVertCrease(panel_id1=panel_id, panel_id2=panel_id-15, hor_num=hor_num, vert_num=vert_num, crease_type=1)
    if panel_id >= x_num*y_num*20+5:
        if np.mod(panel_id+1,10) in (4,7):
            CreateVertCrease(panel_id1=panel_id, panel_id2=panel_id-5, hor_num=hor_num, vert_num=vert_num, crease_type=1)
        elif np.mod(panel_id+1,10) in (1,8):
            CreateVertCrease(panel_id1=panel_id, panel_id2=panel_id-5, hor_num=hor_num, vert_num=vert_num, crease_type=2)

for panel_id in range(len(panels_interval[:,0,0])):
    if np.mod(panel_id+1,5)==0:
        CreateHorCrease(panel_id1=panel_id, panel_id2=panel_id-4, hor_num=hor_num, vert_num=vert_num)
        CreateHorCrease(panel_id1=panel_id, panel_id2=panel_id-3, hor_num=hor_num, vert_num=vert_num)
        CreateHorCrease(panel_id1=panel_id, panel_id2=panel_id-2, hor_num=hor_num, vert_num=vert_num)
        CreateHorCrease(panel_id1=panel_id, panel_id2=panel_id-1, hor_num=hor_num, vert_num=vert_num)

# Define Step
mdb.models['Model-1'].ExplicitDynamicsStep(name='Step-1', previous='Initial', improvedDtMethod=ON)

# Define Bottom Boundary Condition
a = mdb.models['Model-1'].rootAssembly
flag = 0
for part_id in range(x_num*y_num*20+x_num*10):
    if np.mod(part_id+1, 5)!=0:
        exec("n = a.instances['Part-{part_id}-1'].nodes".format(part_id=part_id+1))
        exec("nodes{flag} = n.getSequenceFromMask(mask=('[#f]', ), )".format(flag=flag+1))
        flag += 1
region = a.Set(nodes=nodes1+nodes2+nodes3+nodes4+nodes5+nodes6+nodes7+nodes8+nodes9+\
    nodes10+nodes11+nodes12+nodes13+nodes14+nodes15+nodes16+nodes17+nodes18+\
    nodes19+nodes20+nodes21+nodes22+nodes23+nodes24+nodes25+nodes26+nodes27+\
    nodes28+nodes29+nodes30+nodes31+nodes32+nodes33+nodes34+nodes35+nodes36+\
    nodes37+nodes38+nodes39+nodes40+nodes41+nodes42+nodes43+nodes44+nodes45+\
    nodes46+nodes47+nodes48+nodes49+nodes50+nodes51+nodes52+nodes53+nodes54+\
    nodes55+nodes56+nodes57+nodes58+nodes59+nodes60+nodes61+nodes62+nodes63+\
    nodes64+nodes65+nodes66+nodes67+nodes68+nodes69+nodes70+nodes71+nodes72+\
    nodes73+nodes74+nodes75+nodes76+nodes77+nodes78+nodes79+nodes80+nodes81+\
    nodes82+nodes83+nodes84+nodes85+nodes86+nodes87+nodes88+nodes89+nodes90+\
    nodes91+nodes92+nodes93+nodes94+nodes95+nodes96+nodes97+nodes98+nodes99+\
    nodes100+nodes101+nodes102+nodes103+nodes104+nodes105+nodes106+nodes107+\
    nodes108+nodes109+nodes110+nodes111+nodes112, name='BottomNodes')
mdb.models['Model-1'].ZsymmBC(name='BottomBC', createStepName='Step-1', region=region, localCsys=None)

# Define Side Boundary Condition
## You need to change the following lines if you change x_num or y_num
if hor_num==4:
    a = mdb.models['Model-1'].rootAssembly
    n1 = a.instances['Part-4-1'].nodes
    nodes1 = n1.getSequenceFromMask(mask=('[#888888 ]', ), )
    n2 = a.instances['Part-44-1'].nodes
    nodes2 = n2.getSequenceFromMask(mask=('[#888888 ]', ), )
    n3 = a.instances['Part-84-1'].nodes
    nodes3 = n3.getSequenceFromMask(mask=('[#888888 ]', ), )
    n4 = a.instances['Part-124-1'].nodes
    nodes4 = n4.getSequenceFromMask(mask=('[#888888 ]', ), )
    n5 = a.instances['Part-29-1'].nodes
    nodes5 = n5.getSequenceFromMask(mask=('[#888888 ]', ), )
    n6 = a.instances['Part-69-1'].nodes
    nodes6 = n6.getSequenceFromMask(mask=('[#888888 ]', ), )
    n7 = a.instances['Part-109-1'].nodes
    nodes7 = n7.getSequenceFromMask(mask=('[#888888 ]', ), )
    n8 = a.instances['Part-139-1'].nodes
    nodes8 = n8.getSequenceFromMask(mask=('[#888888 ]', ), )
    region = a.Set(nodes=nodes1+nodes2+nodes3+nodes4+nodes5+nodes6+nodes7+nodes8, 
        name='SideNodes')
    mdb.models['Model-1'].PinnedBC(name='SideBC', createStepName='Step-1', region=region, localCsys=None)
elif hor_num==5:
    a = mdb.models['Model-1'].rootAssembly
    n1 = a.instances['Part-4-1'].nodes
    nodes1 = n1.getSequenceFromMask(mask=('[#1084210 ]', ), )
    n2 = a.instances['Part-44-1'].nodes
    nodes2 = n2.getSequenceFromMask(mask=('[#1084210 ]', ), )
    n3 = a.instances['Part-84-1'].nodes
    nodes3 = n3.getSequenceFromMask(mask=('[#1084210 ]', ), )
    n4 = a.instances['Part-124-1'].nodes
    nodes4 = n4.getSequenceFromMask(mask=('[#1084210 ]', ), )
    n5 = a.instances['Part-29-1'].nodes
    nodes5 = n5.getSequenceFromMask(mask=('[#1084210 ]', ), )
    n6 = a.instances['Part-69-1'].nodes
    nodes6 = n6.getSequenceFromMask(mask=('[#1084210 ]', ), )
    n7 = a.instances['Part-109-1'].nodes
    nodes7 = n7.getSequenceFromMask(mask=('[#1084210 ]', ), )
    n8 = a.instances['Part-139-1'].nodes
    nodes8 = n8.getSequenceFromMask(mask=('[#1084210 ]', ), )
    region = a.Set(nodes=nodes1+nodes2+nodes3+nodes4+nodes5+nodes6+nodes7+nodes8, 
        name='SideNodes')
    mdb.models['Model-1'].PinnedBC(name='SideBC', createStepName='Step-1', region=region, localCsys=None)

# Define periodic function
mdb.models['Model-1'].PeriodicAmplitude(name='Amp-1', timeSpan=STEP, frequency=200.0, start=0.0, a_0=0.0, data=((1.0, 0.0), ))

# Define Shaking Force
# You need to change the following lines if you change x_num or y_num
a = mdb.models['Model-1'].rootAssembly
n1 = a.instances['Part-24-1'].nodes
n2 = a.instances['Part-9-1'].nodes
if hor_num==4:
    nodes1 = n1.getSequenceFromMask(mask=('[#888888 ]', ), )
    nodes2 = n2.getSequenceFromMask(mask=('[#888888 ]', ), )
elif hor_num==5:
    nodes1 = n1.getSequenceFromMask(mask=('[#1084210 ]', ), )
    nodes2 = n2.getSequenceFromMask(mask=('[#1084210 ]', ), )
load_region = a.Set(nodes=nodes1+nodes2, name='LeftNodes')

# Define RightNodes Set
# You need to change the following lines if you change x_num or y_num
a = mdb.models['Model-1'].rootAssembly
n1 = a.instances['Part-126-1'].nodes
n2 = a.instances['Part-131-1'].nodes
if hor_num==4:
    node1 = n1.getSequenceFromMask(mask=('[#111111 ]', ), )
    nodes2 = n2.getSequenceFromMask(mask=('[#111111 ]', ), )
elif hor_num==5:
    nodes1 = n1.getSequenceFromMask(mask=('[#108421 ]', ), )
    nodes2 = n2.getSequenceFromMask(mask=('[#108421 ]', ), )
a.Set(nodes=nodes1+nodes2, name='RightNodes')

# History Output LeftNodes
mdb.models['Model-1'].historyOutputRequests.changeKey(fromName='H-Output-1', 
    toName='LeftNodes')
regionDef=mdb.models['Model-1'].rootAssembly.sets['LeftNodes']
mdb.models['Model-1'].historyOutputRequests['LeftNodes'].setValues(variables=(
    'CF2', ), numIntervals=10000, region=regionDef, sectionPoints=DEFAULT, 
    rebar=EXCLUDE)

# History Output RightNodes
regionDef=mdb.models['Model-1'].rootAssembly.sets['RightNodes']
mdb.models['Model-1'].HistoryOutputRequest(name='RightNodes', 
    createStepName='Step-1', variables=('U2', 'V2'), numIntervals=10000, 
    region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

# Use for loop to submit 10 jobs with different Amplitude
for force_id in range(10):
# Define Force
    mdb.models['Model-1'].ConcentratedForce(name='Load-1', createStepName='Step-1', region=load_region, cf2=force_id+1, amplitude='Amp-1', distributionType=UNIFORM, field='', localCsys=None)
# Define Job
    job = mdb.Job(name='LeftLoadFreq=200Amp={force_id}hor_num={hor_num}'.format(force_id=force_id+1, hor_num=hor_num), model='Model-1', description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, explicitPrecision=SINGLE, 
        nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, 
        contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', 
        resultsFormat=ODB, numDomains=1, activateLoadBalancing=False, 
        numThreadsPerMpiProcess=1, multiprocessingMode=DEFAULT, numCpus=1)
# Submit Job
    # job.submit()