def square(x, y):
    f = (-2<x<2) and (-2<y<2)
    return f

def half_plane(x, y):
    f = (x + y - 1 < 0)
    return f

def ellipse(x, y):
    f = ((x - 0.25)**2/9 + (y - 0.25)**2/16 -1) < 0
    return f
