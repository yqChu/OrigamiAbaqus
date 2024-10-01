import sys
sys.path.append('C:/Research/Nonreciprocity/OrigamiAbaqus')
from abaqus import *
from abaqusConstants import *
from caeModules import *
from part import *
from PanelFunctions import *
import numpy as np
from CreaseFunctions import *
Mdb()

m = mdb.models['Model-1']

# hor_num and vert_num should be equal
hor_num = 3
vert_num = hor_num
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
        name=f'Part-{panel_id+1}',
        dimensionality=THREE_D,
        type=DEFORMABLE_BODY,
        nodes=(node_labels, node_coords),
        elements=[[element_type, element_labels, element_nodes]]
    )

    mdb.models['Model-1'].parts[f'Part-{panel_id+1}'].DatumCsysByThreePoints(name=f'Datum-csys-{panel_id+1}-A', coordSysType=CARTESIAN, origin=panels_interval[panel_id,0],
    point1=panels_interval[panel_id,1], point2=panels_interval[panel_id,2])

    mdb.models['Model-1'].parts[f'Part-{panel_id+1}'].DatumCsysByThreePoints(name=f'Datum-csys-{panel_id+1}-B', coordSysType=CARTESIAN, origin=panels_interval[panel_id,0],
    point1=panels_interval[panel_id,2], point2=panels_interval[panel_id,1])

# Materials
mdb.models['Model-1'].Material(name='Material-1')
mdb.models['Model-1'].materials['Material-1'].Elastic(table=((210000000.0, 0.3),))
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
    elements = mdb.models['Model-1'].parts[f'Part-{panel_id+1}'].elements.getSequenceFromMask(mask=('[#1ffffff]',),)
    region = mdb.models['Model-1'].parts[f'Part-{panel_id+1}'].Set(elements=elements, name='Set-1')
    mdb.models['Model-1'].parts[f'Part-{panel_id+1}'].SectionAssignment(region=region, sectionName='Section-1')

# Define Instance
mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
for panel_id in range(len(panels_interval[:,0,0])):
    mdb.models['Model-1'].rootAssembly.Instance(name=f'Part-{panel_id+1}-1',
                                                part=mdb.models['Model-1'].parts[f'Part-{panel_id+1}'],
                                                dependent=ON)

# Define ConnectorSection
mdb.models['Model-1'].ConnectorSection(name='ConnSect-1', assembledType=HINGE)
elastic_0 = connectorBehavior.ConnectorElasticity(components=(4, ), table=((
    0.001, ), ))
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
