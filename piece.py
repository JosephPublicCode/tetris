from shapes import Shapes
class Piece(object):
    
    def __init__(self, x, y, shape):
        self.shapes = Shapes()
        self.x = x 
        self.y = y 
        self.shape = shape
        self.color = self.shapes.shape_colors[self.shapes.shapes.index(shape)]
        self.rotation = 0 
