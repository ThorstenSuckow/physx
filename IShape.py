from util import V
from Block import Block, block2pyglet

class IShape:
    _x = _y = 0

    _blocks = None 
    _block_dim = 0    

    _rotation = (0, 1)

    def __init__(self, blocks: list, x, y):
        self._blocks = blocks
        self._block_dim = blocks[0]._width

        self._x = x
        self._y = y
        self.spawn(x, y)
    def spawn(self, x, y):
        self.update(x, y)

    def update(self, x = None, y = None):
        
        self._x = x if x is not None else self._x
        self._y = y if y is not None else self._y

        i = 0
        for b in self._blocks:
            alignment = self.align_block(i, self._rotation, self._x, self._y) 
            if (alignment is not None):
                b.update(alignment[0], alignment[1])
            i+=1

        return self


    def align_block(self, id, rotation, x, y):
        dim = self._block_dim
        
        id = (4 - id) if (rotation[1] == -1 or rotation[0] == -1) else id + 1
        if rotation[0] == 0:
            delta_x = -dim if rotation[1] == -1 else 0 
            return(x + delta_x, y + (id - 3) *dim) 
        else:
            delta_y = -dim if rotation[0] == 1 else 0 
            return(x + (id - 3) *dim, y + delta_y) 
        
         
    def rotate(self):
        vs = V()
        next = vs.index(self._rotation)
        self._rotation = vs[(next + 1) % len(vs)]
        return self
    

def ishape2pyglet(ishape, batch=None):
    shapes = []
    for block in ishape._blocks:
        shapes += block2pyglet(block)
    
    return shapes
