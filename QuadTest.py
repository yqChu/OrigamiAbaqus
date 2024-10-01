from abaqus import *
from abaqusConstants import *
from caeModules import *
from part import *
from PanelFunctions import *
import numpy as np
Mdb()

m = mdb.models['Model-1']

node1 = np.array([0, 0, 0])
node2 = np.array([1, 0, 0])
node3 = np.array([1, 1, 0])
hor_num=3
vert_num=3
node_labels, node_coords = PanelFromNodes(node1, node2, node3, hor_num, vert_num)

element_type, element_labels, element_nodes = S4ElementFromPanel(hor_num, vert_num)

nodeLabelsPart1=[1,2,3,4]
nodeLabelsPart2=[1,2,3,4]
nodeCoordsPart1=[[-9.9, 9.9, 0],
                 [-9.9, -9.9, 0],
                 [9.9, -9.9, 0],
                 [9.9, 9.9, 0]]
nodeCoordsPart2=[[10.0, 9.9, 0.1],
                [10.0, -9.9, 0.1],
                [10.0, -9.9, 20.0],
                [10.0, 9.9, 20.0]]

elementsArrayPart1=[
    ['S3', [1,2], [[1, 2, 3], [1, 2, 4]]]
]
elementsArrayPart2=[
    ['S4', [2], [[1, 2, 3, 4]]]
]

mdb.models['Model-1'].PartFromNodesAndElements(
    name='Part-1',
    dimensionality=THREE_D,
    type=DEFORMABLE_BODY,
    nodes=(node_labels, node_coords),
    elements=[[element_type, element_labels, element_nodes]]
)

node1 = np.array([])
