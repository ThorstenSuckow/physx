import tkinter

class Block:
    _count = 0
    _width = _height = 50
    _x = _y = 0
    _el = None 
    _tag = None

    _rendered = False
    _borders = None

    _group_tags = None

    _color = None

    def tag(self):
        return self._tag

    def get_width(self):
        return self._width
    

    def add_group_tag(self, tag_id):
        if tag_id in self._group_tags:
            raise Exception("tag id already in group tags")
        
        self._group_tags.append(tag_id)

    def __init__(self, color="Grey"):
        self._color=color
        self._group_tags = []
        Block._count += 1
        self._tag = f"block_{Block._count}"
        
        pass


    def render(self,canvas: tkinter.Canvas, x = None, y = None):   
        self._x = self._x if x is None else x
        self._y = self._y if y is None else y

        height = self._height
        width = self._width

        if self._rendered == True:
            canvas.moveto(self._tag, x, y)
            return self._el

        
        tags = self._group_tags + [self._tag]

        self._el = canvas.create_rectangle(
            x, y, x + width, y + height, 
            outline="", fill=self._color, tags=tags
        )

        self._borders = (
            # clockwise, starting w/ top
            canvas.create_line(x, y, x + width, y,  fill="white", tags=tags),
            canvas.create_line(x + width -1, y, x + width -1, y + height,  fill="white", tags=tags),
            canvas.create_line(x, y + height - 1, x + width, y + height - 1, fill="white", tags=tags),
            canvas.create_line(x, y, x, y + height,  fill="white", tags=tags)
        )    

        self._rendered = True
        return self._el

    def update_xy(self, x, y):
        self._x = x
        self._y = y

