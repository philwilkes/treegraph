import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

def node_angle_f(a, b, c):
    
    # normalise distance between coordinate pairs where b is the central coordinate
    ba = a - b
    bc = c - b
  
    # calculate angle between and length of each vector pair 
    angle_pair = lambda ba, bc: np.arccos(np.dot(bc, ba) / (np.linalg.norm(ba) * np.linalg.norm(bc)))

    return angle_pair(bc.T, ba)#[0][0]


def nn(arr, N):
    
    nbrs = NearestNeighbors(n_neighbors=N+1, algorithm='kd_tree').fit(arr)
    distances, indices = nbrs.kneighbors(arr)
    
    return distances[:, 1]


def update_slice_id(self, node_id, X):
    
    node = self.centres.loc[self.centres.node_id == node_id]
    nbranch = node.nbranch.values[0]
    ncyl = node.ncyl.values[0]
    
    # update slices of same branch above ncyls
    self.centres.loc[(self.centres.nbranch == nbranch) & (self.centres.ncyl >= ncyl), 'slice_id'] += X
    
    # update branches above nbranch
    self.centres.loc[self.centres.nbranch.isin(self.branch_hierarchy[nbranch]['above']), 'slice_id'] += X

    
class treegraph:
    
    def __init__(self, pc, slice_interval=.05, min_pts=10, base_location=None, verbose=False):

        self.pc = pc.copy()        
        self.slice_interval=slice_interval
        self.min_pts = min_pts
        
        if base_location == None:
            self.base_location = self.pc.z.idxmin()
        else:
            self.base_location = base_location
            
        self.verbose = verbose
            
