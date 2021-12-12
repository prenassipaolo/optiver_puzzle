class Constraint():
    def __init__(self, function) -> None:
        self.function = function
        self.inside_points = None
        self.boundary_points = None
    
    def __call__(self, *args, **kwds):
        return self.function(*args, **kwds)
    
    def find_neighbors(x, y):
        return {(x+1, y), (x-1, y), (x, y+1), (x, y-1)}
    
    def evaluate_points(self, max_iter:int=100, start_points:set={(0,0)}, print_iter:int=None):

        inside_points = start_points
        points_to_explore = start_points
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
            neighbors = self.function(*point)
            new_inside = {neighbor for neighbor in neighbors \
                if ((neighbor not in inside_points) and self.function(*neighbor))}
            new_bondary = {neighbor for neighbor in (neighbors-new_inside) \
                if  not self.function(*neighbor)}
            # add the good neighbours in the inside_points and points_to_explore
            inside_points |= new_inside
            points_to_explore |= new_inside
            bondary_points |= new_bondary
        
        self.inside_points = inside_points
        self.boundary_points = bondary_points

        return inside_points, bondary_points



def square(x, y):
    f = (-2<x<2) and (-2<y<2)
    return f

def half_plane(x, y):
    f = (x + y - 1 < 0)
    return f

def ellipse(x, y):
    f = ((x - 0.25)**2/9 + (y - 0.25)**2/16 -1) < 0
    return f
