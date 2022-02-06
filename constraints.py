from copy import copy
from utils import neighbors as find_neighbors
from utils import points_distance

class Constraint():
    """
    A class used to represent the constraints
    ...

    Attributes
    ----------
    function : function
        function describing the boundaries. Given the coordinates of a point 
        the function returns a True value if the point respect the bouddaries, 
        False otherwise
    inside_points : set
        dictionary with the coordinates of the points that respects the boundaries
    boundary_points : set
        dictionary with the coordinates of the points that do not respects the
        boundaries and are at a distance of 1 step form the closest inside point
    closest_boundary : dict
        dictionary with inside points coordinates as keys and their closest 
        boundary point coordinates and the relative distance as values


    Methods
    -------
    __call__(*args, **kwds)
        Calls the function describing the boundaries
    evaluate_points(start_points:set={(0,0)}, max_iter:int=1000, print_iter:int=None)
        Finds, updates and returns the inside and boundary points
    find_closest_boundary()
        Finds the closest boundary point and its distance per each inside point
    """


    def __init__(self, function) -> None:
        self.function = function
        self.inside_points = None
        self.boundary_points = None
        self.closest_boundary = None
    
    
    def __call__(self, *args, **kwds):
        return self.function(*args, **kwds)
    
    
    def evaluate_points(self, start_points:set={(0.,0.)}, max_iter:int=1000, print_iter:int=None):
        """
        Finds the inside and boundary points according to the constraint function
        """

        inside_points = copy(start_points)
        points_to_explore = copy(start_points)
        bondary_points = set()

        n = 0
        if print_iter!=None:
            print(f'n° iter (of {max_iter}):', end = '\t')

        while len(points_to_explore)!=0 and n<max_iter:
            if print_iter!=None and n%10 == 0:
                print(n, end='\t')            
            
            n+=1
            # select a point to explore and analyze its neighbours
            point = points_to_explore.pop()
            neighbors = find_neighbors(*point)
            new_inside = {neighbor for neighbor in neighbors \
                if ((neighbor not in inside_points) and self.function(*neighbor))}
            new_bondary = {neighbor for neighbor in (neighbors-new_inside) \
                if  not self.function(*neighbor)}
            # add the good neighbours in the inside_points and points_to_explore
            inside_points = inside_points.union(new_inside)
            points_to_explore = points_to_explore.union(new_inside)
            bondary_points = bondary_points.union(new_bondary)
        
        self.inside_points = inside_points
        self.boundary_points = bondary_points

        if len(points_to_explore)>0:
            raise 'The boundaries are too large. Increase the max_iter variable to explore more points.'
        
        print(f'\nNumber of points inside the boundaries: {len(self.inside_points)}\n')

        return inside_points, bondary_points
    
    def find_closest_boundary(self):
        """
        Finds the closest boundary point and its distance per each inside point
        """

        if self.inside_points==None or self.boundary_points==None:
            raise "No inside_points of boundary_points detected"
    
        closest_boundary = dict()
        for ip in self.inside_points:
            distances = {bp: points_distance(ip, bp) for bp in self.boundary_points}
            best = min(distances, key=distances.get)
            closest_boundary[ip] = (best, distances[best])
        
        self.closest_boundary = closest_boundary
        
        return closest_boundary
    
   