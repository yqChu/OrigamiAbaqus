from abaqus import *
from abaqusConstants import *
from caeModules import *
from part import *
from PanelFunctions import *
Mdb()

m = mdb.models['Model-1']

node1 = np.array([0, 0.1, 0.1])
node2 = np.array([0, 0.9, 0.1])
node3 = np.array([0, 0.1, 0.9])
hor_num = 3
vert_num = 3

node_labels, node_coords = PanelFromNodes(node1, node2, node3, hor_num, vert_num)
element_type, element_labels, element_nodes = S4ElementFromPanel(hor_num, vert_num)

mdb.models['Model-1'].PartFromNodesAndElements(
    name='Part-1',
    dimensionality=THREE_D,
    type=DEFORMABLE_BODY,
    nodes=(node_labels, node_coords),
    elements=[[element_type, element_labels, element_nodes]]
)
mdb.models['Model-1'].parts['Part-1'].DatumCsysByThreePoints(name='Datum csys-1',
            coordSysType=CARTESIAN, origin=node1, point1=node3, point2=node2)
mdb.models['Model-1'].parts['Part-1'].DatumCsysByThreePoints(name='Datum csys-4',
            coordSysType=CARTESIAN, origin=node1, point1=node2, point2=node3)

node1 = np.array([0.1, 0, 0.1])
node2 = np.array([0.9, 0, 0.1])
node3 = np.array([0.1, 0, 0.9])
hor_num = 3
vert_num = 3

node_labels, node_coords = PanelFromNodes(node1, node2, node3, hor_num, vert_num)
element_type, element_labels, element_nodes = S4ElementFromPanel(hor_num, vert_num)

mdb.models['Model-1'].PartFromNodesAndElements(
    name='Part-2',
    dimensionality=THREE_D,
    type=DEFORMABLE_BODY,
    nodes=(node_labels, node_coords),
    elements=[[element_type, element_labels, element_nodes]]
)
mdb.models['Model-1'].parts['Part-2'].DatumCsysByThreePoints(name='Datum csys-2',
            coordSysType=CARTESIAN, origin=node1, point1=node3, point2=node2)
mdb.models['Model-1'].parts['Part-1'].DatumCsysByThreePoints(name='Datum csys-5',
            coordSysType=CARTESIAN, origin=node1, point1=node2, point2=node3)

# node1 = np.array([0, -0.1, 0.1])
# node2 = np.array([0, -1, 0.1])
# node3 = np.array([0, -0.1, 0.9])
node1 = np.array([0.1, 0.1, 0])
node2 = np.array([0.1, 0.9, 0])
node3 = np.array([0.9, 0.1, 0])
hor_num = 3
vert_num = 3

node_labels, node_coords = PanelFromNodes(node1, node2, node3, hor_num, vert_num)
element_type, element_labels, element_nodes = S4ElementFromPanel(hor_num, vert_num)

mdb.models['Model-1'].PartFromNodesAndElements(
    name='Part-3',
    dimensionality=THREE_D,
    type=DEFORMABLE_BODY,
    nodes=(node_labels, node_coords),
    elements=[[element_type, element_labels, element_nodes]]
)
mdb.models['Model-1'].parts['Part-3'].DatumCsysByThreePoints(name='Datum csys-3',
            coordSysType=CARTESIAN, origin=node1, point1=node3, point2=node2)
mdb.models['Model-1'].parts['Part-1'].DatumCsysByThreePoints(name='Datum csys-6',
            coordSysType=CARTESIAN, origin=node1, point1=node2, point2=node3)

a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
p = mdb.models['Model-1'].parts['Part-1']
a.Instance(name='Part-1-1', part=p, dependent=ON)
p = mdb.models['Model-1'].parts['Part-2']
a.Instance(name='Part-2-1', part=p, dependent=ON)
p = mdb.models['Model-1'].parts['Part-3']
a.Instance(name='Part-3-1', part=p, dependent=ON)

# Material
mdb.models['Model-1'].Material(name='Material-1')
mdb.models['Model-1'].materials['Material-1'].Elastic(table=((2100000.0, 0.3), 
    ))
mdb.models['Model-1'].materials['Material-1'].Density(table=((2000.0, ), ))

# Section
mdb.models['Model-1'].HomogeneousShellSection(name='Section-1', 
    preIntegrate=OFF, material='Material-1', thicknessType=UNIFORM, 
    thickness=0.01, thicknessField='', nodalThicknessField='', 
    idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT, 
    thicknessModulus=None, temperature=GRADIENT, useDensity=OFF, 
    integrationRule=SIMPSON, numIntPts=5)

# Section Assignment
elements = mdb.models['Model-1'].parts['Part-1'].elements.getSequenceFromMask(mask=('[#f ]',),)
region = mdb.models['Model-1'].parts['Part-1'].Set(elements=elements, name='Set-1')
mdb.models['Model-1'].parts['Part-1'].SectionAssignment(region=region, sectionName='Section-1', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='',thicknessAssignment=FROM_SECTION)

elements = mdb.models['Model-1'].parts['Part-2'].elements.getSequenceFromMask(mask=('[#f ]',),)
region = mdb.models['Model-1'].parts['Part-2'].Set(elements=elements, name='Set-1')
mdb.models['Model-1'].parts['Part-2'].SectionAssignment(region=region, sectionName='Section-1', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='',thicknessAssignment=FROM_SECTION)

# Define Connector
mdb.models['Model-1'].ConnectorSection(name='ConnSect-1', assembledType=HINGE)
elastic_0 = connectorBehavior.ConnectorElasticity(components=(4, ), table=((
    1.0, ), ))
mdb.models['Model-1'].sections['ConnSect-1'].setValues(behaviorOptions =(
    elastic_0, ) )
mdb.models['Model-1'].sections['ConnSect-1'].behaviorOptions[0].ConnectorOptions(
    )

# for i in range(vert_num):
#     a = mdb.models['Model-1'].rootAssembly
#     n1 = a.instances['Part-1-1'].nodes
#     n2 = a.instances['Part-2-1'].nodes
#     wire = a.WirePolyLine(points=((n1[i*hor_num], n2[(i+1)*hor_num-1]), ), mergeType=IMPRINT, 
#         meshable=False)
#     oldName = wire.name
#     a.features.changeKey(fromName=oldName, 
#         toName=f'Wire-{i+1}')
#     e1 = a.edges
#     edges1 = e1.getSequenceFromMask(mask=('[#1 ]', ), )
#     a.Set(edges=edges1, name=f'Wire-{i+1}-Set-1')
#     region = a.sets[f'Wire-{i+1}-Set-1']
#     csa = a.SectionAssignment(sectionName=f'ConnSect-1', region=region)
#     #: The section "ConnSect-1" has been assigned to 1 wire or attachment line.
#     dtmid1 = a.instances['Part-1-1'].datums[2]
#     dtmid2 = a.instances['Part-2-1'].datums[2]
#     a.ConnectorOrientation(region=csa.getSet(), localCsys1=dtmid1, 
#         orient2sameAs1=False, localCsys2=dtmid2)