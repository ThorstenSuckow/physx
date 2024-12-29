import time
from util import V
import tkinter
from random import randint
import sys 
from util import rgb, calltime
import threading

class Particle:
    _el = None
    _rendered = False
    _bounds = (0, 0, 0, 0)
    _x = _y = _v = _dim = _velocity = _prev_x = _prev_y = 0
    _dirty = False
    _killed = False
    _color = None

    def __init__(self, bounds, color=None):
        if color is not None:
            self._color = color
        else:
            self._color = f"{rgb(randint(0, 255), randint(0, 255), randint(0, 255))}"
        self._bounds = bounds
        self.spawn()
        
    def spawn(self):
        self._x = randint(self._bounds[0], self._bounds[2])
        self._y =  randint(self._bounds[1], self._bounds[2])
        self._v = (randint(-3, 3), randint(-3, 3))
        if self._v[0] == 0 and self._v[1] == 0:
            self._v = (0, randint(-3, -1))
        self._dim = randint(2, 10)
        self._velocity = randint(10, 10)
        self._rendered = False
        self._killed = False
        return self

    def bounds(self, bounds):
        self._bounds = bounds

    def render(self, canvas: tkinter.Canvas, x = None, y = None):
        self._x = x if x is not None else self._x 
        self._y = y if y is not None else self._y

        x = self._x
        y = self._y

        if self._killed:
            return self
        
        if self._rendered:
            canvas.move(self._el,x - self._prev_x, y - self._prev_y)
            self._dirty = False
            self.prev_x = x
            self.prev_y = y
            return self
        
        self.prev_x = x
        self.prev_y = y


        self._rendered = True
        self._dirty = False
        
        self._el = canvas.create_oval(
            x, y, x+self._dim, y + self._dim, fill=self._color
        )
        return self 

    def kill(self, canvas):
        if self._killed:
            canvas.delete(self._el)


    def fade(self):

        x = self._x
        y = self._y
        v = self._v
        bounds = self._bounds

        velocity = self._velocity

        velocity = self._dim/100
    
        x +=  velocity * v[0]
        y +=  velocity * v[1]
        
        vx = v[0]
        vy = v[1]

        dim = self._dim
        
        if x <= bounds[0]:
            self._killed = True
        elif x + dim >= bounds[2]:
            self._killed = True
        
        elif y <= bounds[1]:
            self._killed = True
        
        elif y + dim >= bounds[3]:
            self._killed = True
        
        if self._killed:
            return self

        self._prev_x = self._x
        self._prev_y = self._y
        
        self._x = x
        self._y = y
        self._velocity = velocity
    
        self._dirty = True
        return self 


    def bounce(self):
        
        
        x = self._x
        y = self._y
        v = self._v
        bounds = self._bounds

        velocity = self._velocity

        velocity = self._dim/5
    
        x +=  velocity * v[0]
        y +=  velocity * v[1]
        
        vx = v[0]
        vy = v[1]

        dim = self._dim
        
        if x <= bounds[0]:
            vx = (-1 if vx > 0 else 1) * randint(1, 3)
            x = bounds[0]
            self._v = (vx, vy)
        elif x + dim >= bounds[2]:
            vx = (-1 if vx > 0 else 1) * randint(1, 3)
            x = bounds[2] - dim
            self._v = (vx, vy)
        
        elif y <= bounds[1]:
            vy = (-1 if vy > 0 else 1) * randint(1, 3)
            y = bounds[1]
            self._v = (vx, vy)
        
        elif y + dim >= bounds[3]:
            vy = (-1 if vy > 0 else 1) * randint(1, 3)
            y = bounds[3] - dim
            self._v = (vx, vy)
        
        self._prev_x = self._x
        self._prev_y = self._y
        
        self._x = x
        self._y = y
        self._velocity = velocity
    
        self._dirty = True
        return self 

    pass

def _key_handler(event):
    pass


last = time.perf_counter_ns()
rng = 0

def _flow_particles(fromp, top):
    global last
    global rng 
   
    print(fromp, top)
   
    k = 0
    while True:
        canvas.update_idletasks()
        i = fromp
        while i < top:
            ps[i].flow()
            i += 1
        canvas.update()
        #k += 1
       

        
rng = 0
def _render_world(ps, fromp, top):
    global last
    global rng 

    start = time.perf_counter_ns()
    #time.sleep(10)
    
    rng+=1
    #canvas.update_idletasks()
    i = fromp
    length = top
    while i < length:
        if ps[i]._killed:
            ps[i].kill(canvas)
            ps[i].spawn()
        else:
            ps[i].fade().render(canvas)
        
        i += 1
    
    
    #ns, ms, sec, fps = calltime(start)
    #print(f"[PARTICLES] ns: {ns}; ms: {ms}; sec {sec} ({1/sec})")
    
    ns, ms, sec, fps = calltime(last)
    print(f"[()] ns: {ns}; ms: {ms}; sec {sec} ({1/sec})")
    last = time.perf_counter_ns()

    canvas.after(16, _render_world, ps, fromp, top)
    #canvas.update();
    
    
    #if rng %2 == 0:
    #    frame.place(x = -1000, y= -1000)
    #else: 
    #frame.place(x = 0, y= 0)
    
    pass

def _init_world(ps):
    
    #threading.Thread(target=_flow_particles, args = [0, len(ps)], daemon=True).start()
    #threading.Thread(target=_flow_particles, args = [100, 200], daemon=True).start()
    
    #threading.Thread(target=_flow_particles, args = [500, 1000], daemon=True).start()
    
    canvas.after(16, _render_world, ps, 0, len(ps))
    

win = tkinter.Tk()
win.title("particle")

frame = tkinter.Frame(win, bg='')
frame.pack(fill="both", expand=True)
#frame.place(x=-1000, y=-1000)
canvas = tkinter.Canvas(frame, bg='black')
canvas.pack(fill="both", expand=True)

def resize(event):    
    global ps
    w,h = event.width, event.height
    for p in ps:
        p.bounds((0, 0, w, h))


frame.bind('<Configure>', resize)


ps = []


def run(args):
    global ps
    num = int(args[1])

    colors = {
        1: "grey",
        2: "lightgrey",
        3: "darkgrey"
    }

    for i in range(0, num):
        fill = colors[randint(1, 3)]
        ps.append(Particle((0, 0, 300, 200), color=fill))

    canvas.after(1, lambda:_init_world(ps))


    win.bind("<Key>", _key_handler)
    win.mainloop()

    
if __name__ == '__main__':
    run(sys.argv)



