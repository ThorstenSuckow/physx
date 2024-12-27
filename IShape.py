import tkinter
from Pivot import Pivot
from util import V

class IShape:
    _count = 0
    _tag = None
    _x = _y = 0

    _blocks = None 
    _block_dim = 0    

    _pivot = None

    _rotation = (0, 1)

    def __init__(self, blocks: list, x, y):
        IShape._count += 1
        self._tag = f"iblock_{IShape._count}"
        
        self._pivot = Pivot(self)

        for b in blocks:
            b.add_group_tag(self._tag)

        self._block_dim = b.get_width()

        self._x = x
        self._y = y
        self._blocks = blocks
        

    def tag(self):
        return self._tag


    def xy(self):
        return (self._x, self._y)


    def render(self, canvas: tkinter.Canvas):
        
        i = 0
        for b in self._blocks:
            alignment = self.align_block(i, self._rotation, self._x, self._y) 
            if (alignment is not None):
                b.render(canvas, alignment[0], alignment[1])
            i+=1

        self._pivot.render(canvas)
        return self


    def update_by(self, x, y, canvas=None):
        self._x += x
        self._y += y 
        
        if canvas is not None:
            canvas.move(self._tag, x, y)


    def align_block(self, id, rotation, x, y):
        dim = self._block_dim
        
        id = (4 - id) if (rotation[1] == -1 or rotation[0] == -1) else id + 1
        if rotation[0] == 0:
            delta_x = -dim if rotation[1] == - 1 else 0 
            return(x + delta_x, y + (id - 3) *dim) 
        else:
            delta_y = -dim if rotation[0] == 1 else 0 
            return(x + (id - 3) *dim, y + delta_y) 
        
         
    def rotate(self):
        vs = V()
        next = vs.index(self._rotation)
        self._rotation = vs[(next + 1) % len(vs)]
        return self