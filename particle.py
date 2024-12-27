import time
from util import V
import tkinter
from random import randint

class Particle:
    _el = None
    _rendered = False
    _bounds = (0, 0, 0, 0)
    _x = _y = _v = _dim = _velocity = 0

    def __init__(self, bounds):
        self._bounds = bounds
        self._x = randint(0, 250)
        self._y =  randint(0, 150)
        self._v = (randint(1, 3), randint(1, 3))
        self._dim = randint(2, 20)
        self._velocity = randint(1, 5)
        
    def bounds(self, bounds):
        self._bounds = bounds

    def render(self, canvas: tkinter.Canvas, x = None, y = None):
        self._x = x if x is not None else self._x 
        self._y = y if y is not None else self._y

        x = self._x
        y = self._y

        if self._rendered:
            canvas.moveto(self._el, x, y)
            return self
        
        self._rendered = True
        self._el = canvas.create_oval(x, y, x+self._dim, y + self._dim, fill="white")
        return self 
    
    def flow(self):
        x = self._x
        y = self._y
        v = self._v
        bounds = self._bounds

        velocity = self._velocity

        x +=  velocity * v[0]
        y +=  velocity * v[1]
        
        vx = v[0]
        vy = v[1]

        dim = self._dim
        
        if x <= bounds[0]:
            vx = (-1 if vx > 0 else 1) * randint(1, 3)
            velocity = randint (1, 3)
            x = bounds[0]
        elif x + dim >= bounds[2]:
            vx = (-1 if vx > 0 else 1) * randint(1, 3)
            x = bounds[2] - dim
            velocity = randint (1, 3)
        elif y <= bounds[1]:
            vy = (-1 if vy > 0 else 1) * randint(1, 3)
            y = bounds[1]
            velocity = randint (1, 3)
        elif y + dim >= bounds[3]:
            vy = (-1 if vy > 0 else 1) * randint(1, 3)
            y = bounds[3] - dim
            velocity = randint (1, 3)

        self._v = (vx, vy)
        self._x = x
        self._y = y
        self._velocity = velocity
      
        return self 

    pass

def _key_handler(event):
    pass


last = time.time_ns() // 1_000_000
def _render_world():
    global last
   
    current = time.time_ns() // 1_000_000 # ms
    if (current - last) >= 10: # ~ 1 secs 
        for p in ps:
            p.flow().render(canvas)

        last = current
        pass

    canvas.after(1, _render_world)

    pass

win = tkinter.Tk()
win.title("particle")

canvas = tkinter.Canvas(win, bg='black')
canvas.pack(fill="both", expand=True)

def resize(event):    
    w,h = event.width, event.height
    for p in ps:
        p.bounds((0, 0, w, h))


canvas.bind('<Configure>', resize)


ps = [
    Particle((0, 0, 300, 200)),
    Particle((0, 0, 300, 200)),
    Particle((0, 0, 300, 200)),
    Particle((0, 0, 300, 200)),
    Particle((0, 0, 300, 200)),
    Particle((0, 0, 300, 200)),
    Particle((0, 0, 300, 200)),
    Particle((0, 0, 300, 200)),
    Particle((0, 0, 300, 200)),
    Particle((0, 0, 300, 200)),
    Particle((0, 0, 300, 200)),
    Particle((0, 0, 300, 200)),
    Particle((0, 0, 300, 200)),
    Particle((0, 0, 300, 200)),
    Particle((0, 0, 300, 200)),
    Particle((0, 0, 300, 200))
]

_render_world()


win.bind("<Key>", _key_handler)
win.mainloop()



def run(args):
    print(args[1:])

if __name__ == '__main__':
    run(sys.argv)



