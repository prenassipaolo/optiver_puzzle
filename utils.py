import numpy as np
import yaml


def neighbors(x, y):
    """
    Returns the adjacent points to the given coordinates of the grid
    """
    return {(x+1, y), (x-1, y), (x, y+1), (x, y-1)}


def points_distance(p1:tuple, p2:tuple):
    """
    Returns the distance in steps from point p1 to point p2
    """
    assert len(p1)==len(p2)
    return np.abs((np.array(p1)-np.array(p2)).sum())


def dict2keys_values(d:dict):
    """
    Returns a list containing the keys and the values
    """
    
    l = []
    
    if len(d)!=0:
        for i in d:
            l.append(i)
            l.append(d[i])
    
    return l

def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.load(f, yaml.Loader)