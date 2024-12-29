import pyglet as py

class Block:
    _width = _height = 50
    _x = _y = 0
    _el = None 
    _tag = None
    _rendered = False
    _borders = None

    _color = None
    
    
    def __init__(self, x=0, y=0, width=50, height= 50, opacity=255, color = (255, 255, 255)):
        self._color = color
        self._opacity = opacity
        self._width = width
        self._height = height
        self.spawn(x, y)
        pass

    def spawn(self, x, y):
        return self.update(x, y)    


    def update(self, x = None, y = None):   
        self._x = self._x if x is None else x
        self._y = self._y if y is None else y

        height = self._height
        width = self._width

        self._borders = (
            [x, y, x + width - 1, y],
            [x + width -1, y, x + width -1, y + height],
            [x, y + height - 1, x + width - 1, y + height - 1],
            [x, y, x, y + height]
        )    

        return self


def block2pyglet(block, batch=None):
    shapes = []
    x = block._x
    y = block._y
    width = block._width
    height = block._height
    color = block._color
    opacity = block._opacity
    rect = py.shapes.Rectangle(x, y, width, height, color=color)
    rect.opacity = opacity
    rect.draw()
    shapes.append(rect)
    for border in block._borders:
        b = py.shapes.Line(*border, batch=batch, color= (255, 255, 255))   
        shapes.append(b)
        b.draw()
        pass
    return shapes
    
