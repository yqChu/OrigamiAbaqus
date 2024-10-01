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

# mesh scale, hor_num and vert_num should be equal
hor_num = 3
vert_num = hor_num
panels_no_interval = CubePanelNoInterval(sqr_diag_len=0.016, theta=np.pi/4)
panels_interval = np.zeros(panels_no_interval.shape)
for panel_id in range(len(panels_no_interval[:, 0, 0])):
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