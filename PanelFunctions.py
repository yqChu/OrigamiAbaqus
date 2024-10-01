# 现在需要在abaqus里实验一下node_label,node_coordes等允许的格式
import numpy as np
from numpy.linalg import *


def PanelFromNodes(node1, node2, node3, hor_num, vert_num):
    '''
    Form rectangle panels(parts) in Abaqus
    Inputs are the 3D coordinates of vertices, and the amount of mesh points in edge 
    '''
    node_labels=np.arange(1,hor_num*vert_num+1).tolist()

    hor_vec = (node2-node1)/(hor_num-1)
    vert_vec = (node3-node1)/(vert_num-1) 
    node_narray = np.zeros((hor_num*vert_num, 3))
    for vert_id in range(0,vert_num):
        for hor_id in range(0,hor_num):
            node_narray[vert_id*hor_num+hor_id] = node1 + vert_id*vert_vec + hor_id*hor_vec
    node_coords = node_narray.tolist()
    return [node_labels, node_coords]

def S4ElementFromPanel(hor_num, vert_num):
    '''
    Form elements from 3 vertices(nodes) of a rectangle
    following the nodes sequence in function PanelFromNodes
    '''
    element_type = 'S4'
    element_labels = np.arange(1, ((hor_num-1)*(vert_num-1)+1)).tolist()
    element_narray = np.zeros(((hor_num-1)*(vert_num-1), 4))
    for vert_id in range(0, vert_num-1):
        for hor_id in range(0, hor_num-1):
            element_narray[vert_id*(hor_num-1)+hor_id] = [vert_id*hor_num+hor_id+1, vert_id*hor_num+hor_id+2, (vert_id+1)*hor_num+hor_id+2, (vert_id+1)*hor_num+hor_id+1]
    element_nodes = element_narray.astype(int).tolist()
    return [element_type, element_labels, element_nodes]

def CubePanelNoInterval(sqr_diag_len, theta):
    node = np.array([[[0.0, 0.0, 0.0],
                      [1/np.sqrt(2)*sqr_diag_len, 0.0, 0.0],
                      [np.sqrt(2)*np.cos(theta)**2*sqr_diag_len, np.sqrt(2)*np.sin(theta)*np.cos(theta)*sqr_diag_len, 0.0],
                      [np.cos(2*theta)*1/np.sqrt(2)*sqr_diag_len, np.sin(2*theta)*1/np.sqrt(2)*sqr_diag_len, 0.0]],
                      [[0.0, 0.0, 1/np.sqrt(2)*sqr_diag_len],
                      [1/np.sqrt(2)*sqr_diag_len, 0.0, 1/np.sqrt(2)*sqr_diag_len],
                      [np.sqrt(2)*np.cos(theta)**2*sqr_diag_len, np.sqrt(2)*np.sin(theta)*np.cos(theta)*sqr_diag_len, 1/np.sqrt(2)*sqr_diag_len],
                      [np.cos(2*theta)*1/np.sqrt(2)*sqr_diag_len, np.sin(2*theta)*1/np.sqrt(2)*sqr_diag_len, 1/np.sqrt(2)*sqr_diag_len]]])
    panels_no_interval = np.array([[node[0,0], node[0,1], node[1,0]],
                                   [node[0,1], node[0,2], node[1,1]],
                                   [node[0,2], node[0,3], node[1,2]],
                                   [node[0,3], node[0,0], node[1,3]],
                                   [node[1,0], node[1,3], node[1,1]]])
    return panels_no_interval


def PanelsNoInterval(theta, sqr_diag_len, quad_diag_len, x_num, y_num):
    '''
    Initialize
    cyclic--those rectangle+quad cyclic in x & y axis
    cap--those rectangle cyclic only in y axis, works as a cap of the whole structure
    '''
    panels_no_interval_cyclic = np.zeros((x_num*y_num, 20, 3, 3), dtype=float)
    panels_no_interval_cap = np.zeros((x_num, 10, 3, 3), dtype=float)

    A_node = np.array([[[0.0, 0.0, 0.0],
                        [1/np.sqrt(2)*sqr_diag_len*np.cos(theta+np.pi/4), 1/np.sqrt(2)*sqr_diag_len*np.sin(theta+np.pi/4), 0],
                        [sqr_diag_len*np.cos(theta), sqr_diag_len*np.sin(theta), 0],
                        [1/np.sqrt(2)*sqr_diag_len*np.cos(theta-np.pi/4), 1/np.sqrt(2)*sqr_diag_len*np.sin(theta-np.pi/4), 0]], # first layer
                       [[0.0, 0.0, 1/np.sqrt(2)*sqr_diag_len],
                        [1/np.sqrt(2)*sqr_diag_len*np.cos(theta+np.pi/4), 1/np.sqrt(2)*sqr_diag_len*np.sin(theta+np.pi/4), 1/np.sqrt(2)*sqr_diag_len],
                        [sqr_diag_len*np.cos(theta), sqr_diag_len*np.sin(theta), 1/np.sqrt(2)*sqr_diag_len],
                        [1/np.sqrt(2)*sqr_diag_len*np.cos(theta-np.pi/4), 1/np.sqrt(2)*sqr_diag_len*np.sin(theta-np.pi/4), 1/np.sqrt(2)*sqr_diag_len]]]) # second layer
    varphi = np.arctan(quad_diag_len[1]/quad_diag_len[0])
    quad_edge_len = 0.5*np.sqrt(quad_diag_len[0]**2+quad_diag_len[1]**2)
    C_node = np.array([[[quad_edge_len*np.cos(varphi+np.pi/2-theta), quad_edge_len*np.sin(varphi+np.pi/2-theta), 0],
                        [quad_diag_len[0]*np.cos(np.pi/2-theta), quad_diag_len[0]*np.sin(np.pi/2-theta), 0],
                        [quad_edge_len*np.cos(np.pi/2-theta-varphi), quad_edge_len*np.sin(np.pi/2-theta-varphi), 0],
                        [0, 0, 0]],
                       [[quad_edge_len*np.cos(varphi+np.pi/2-theta), quad_edge_len*np.sin(varphi+np.pi/2-theta), 1/np.sqrt(2)*sqr_diag_len],
                        [quad_diag_len[0]*np.cos(np.pi/2-theta), quad_diag_len[0]*np.sin(np.pi/2-theta), 1/np.sqrt(2)*sqr_diag_len],
                        [quad_edge_len*np.cos(np.pi/2-theta-varphi), quad_edge_len*np.sin(np.pi/2-theta-varphi), 1/np.sqrt(2)*sqr_diag_len],
                        [0, 0, 1/np.sqrt(2)*sqr_diag_len]]]) + A_node[0, 1]
    B_node = np.zeros((2, 4, 3))
    D_node = np.zeros((2, 4, 3))
    for i in range(2):
        for j in range(4):
            B_node[i, j, 0] = 2*A_node[0, 2, 0] - A_node[i, j, 0]
            B_node[i, j, 1] = A_node[i, j, 1]
            B_node[i, j, 2] = A_node[i, j ,2]
            D_node[i, j, 0] = 2*A_node[0, 2, 0] - C_node[i, j, 0]
            D_node[i, j, 1] = C_node[i, j, 1]
            D_node[i, j ,2] = C_node[i, j, 2]

    panels_no_interval_cyclic[0] = np.array([[A_node[0,0], A_node[0,1], A_node[1,0]],
                                             [A_node[0,1], A_node[0,2], A_node[1,1]],
                                             [A_node[0,2], A_node[0,3], A_node[1,2]],
                                             [A_node[0,3], A_node[0,0], A_node[1,3]],
                                             [A_node[1,0], A_node[1,3], A_node[1,1]],
                                             [B_node[0,0], B_node[0,1], B_node[1,0]],
                                             [B_node[0,1], B_node[0,2], B_node[1,1]],
                                             [B_node[0,2], B_node[0,3], B_node[1,2]],
                                             [B_node[0,3], B_node[0,0], B_node[1,3]],
                                             [B_node[1,0], B_node[1,3], B_node[1,1]],
                                             [C_node[0,0], C_node[0,1], C_node[1,0]],
                                             [C_node[0,1], C_node[0,2], C_node[1,1]],
                                             [C_node[0,2], C_node[0,3], C_node[1,2]],
                                             [C_node[0,3], C_node[0,0], C_node[1,3]],
                                             [C_node[1,0], C_node[1,3], C_node[1,1]],
                                             [D_node[0,0], D_node[0,1], D_node[1,0]],
                                             [D_node[0,1], D_node[0,2], D_node[1,1]],
                                             [D_node[0,2], D_node[0,3], D_node[1,2]],
                                             [D_node[0,3], D_node[0,0], D_node[1,3]],
                                             [D_node[1,0], D_node[1,3], D_node[1,1]]])
    translation_x = np.zeros((20,3,3))
    translation_y = np.zeros((20,3,3))
    translation_x[:,:,0] = np.ones((20,3))*2*A_node[0,2,0]
    translation_y[:,:,1] = np.ones((20,3))*(C_node[0,1,1]-A_node[0,3,1])
    for y_id in range(y_num):
        for x_id in range(x_num):
            panels_no_interval_cyclic[y_id*x_num+x_id] = panels_no_interval_cyclic[0] + translation_x*x_id + translation_y*y_id
    for x_id in range(x_num):
        panels_no_interval_cap[x_id] = panels_no_interval_cyclic[(y_num-1)*x_num+x_id, 0:10] + translation_y[0:10]
    return [panels_no_interval_cyclic, panels_no_interval_cap]
def SetInterval(panel_no_interval, interval):
    '''
        Args:
            interval(float): The ratio between interval length and diagonal length
    '''
    node_mid = (panel_no_interval[1] + panel_no_interval[2])/2
    vec = np.zeros((3,3))
    panel_interval = np.zeros((3,3))
    for i in range(3):
        vec[i] = panel_no_interval[i] - node_mid
        panel_interval[i] = node_mid + vec[i]*(1-interval)
    return panel_interval