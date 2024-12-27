import tkinter

class IShape:
    _count = 0
    _tag = None
    _x = _y = 0

    _blocks = None 
    _block_dim = 0    
    def __init__(self, blocks: list, x, y):
        IShape._count += 1
        self._tag = f"iblock_{IShape._count}"
        
        for b in blocks:
            b.add_group_tag(self._tag)

        self._block_dim = b.get_width()

        self._x = x
        self._y = y
        self._blocks = blocks
        
        pass

    def render(self, canvas: tkinter.Canvas):
        i = 0
        x = self._x
        y = self._y
        width = self._block_dim
        
        for b in self._blocks:
            b.render(canvas, x + i * width, y)
            i+=1

    def update_by(self, x, y, canvas=None):
        self._x += x
        self._y += y 
        
        if canvas is not None:
            canvas.move(self._tag, x, y)