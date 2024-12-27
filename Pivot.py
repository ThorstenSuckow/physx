import tkinter

class Pivot:
    
    _count = 0
    _width = _height = 20
    _el = None 
    _owner = None
    _rendered = False
    _tag = 0

    def __init__(self, owner):
        self._owner = owner
        Pivot._count += 1
        self._tag = f'pivot_{Pivot._count}'
        pass


    def render(self,canvas: tkinter.Canvas):

        x, y = self._owner.xy()

        self._x = x - int(self._width / 2)
        self._y = y - int(self._height / 2) 

        height = self._height
        width = self._width

        if self._rendered == True:
            return self._el

        tags = [self._owner.tag(), self._tag]

        self._el = canvas.create_oval(
            self._x, self._y, 
            self._x + width, 
            self._y + height, 
            outline="red", fill="", tags=tags
        )

        canvas.create_line(
            x, y, x + 1, y + 1, fill="red", tags=tags
        )


        self._rendered = True
        return self._el


