import pyglet as py
from random import randint

# use translate function to swap coords origin
# in pyglet, 0/0 coords are at the bottom left of the screen  
window = py.window.Window(1280, 720)

def c(r = None, g = None, b = None):
    if r is None:
        return (randint(0, 255), randint(0, 255), randint(0, 255))

    return (r, g, b)


def get_fps_display(window):
    fps_display = py.window.FPSDisplay(window=window)
    fps_display.label.y = window.height - 50
    fps_display.label.x = window.width - 100
    return fps_display

class Particle:
    _bounds = None
    v = None
    dx = dy = _x = _y = _px = _py = _dim = 0

    def __init__(self, bounds, dim = None):
        self._dim = dim
        self._bounds = bounds
        pass

    def spawn(self):
        bounds = self._bounds
        self._dim = randint(1, 20) if self._dim is None else self._dim 
        v = [randint(-1, 1), randint(-1, 1)]
        if v[0] == 0 and v[1] == 0:
            v[randint(0, 1)] = 1 if randint(0, 1) == 1 else -1

        self.v = tuple(v)
        self.dx = self.dy = self._px = self._py = 0
        
        self._x = randint(bounds[0], bounds[2])
        self._y = randint(bounds[1], bounds[3])


        return self
        pass

    def update(self, dt):
        
        x = self._x
        y = self._y
        dim = self._dim
        v = self.v
        bounds = self._bounds
        velocity = max(0.005, (dim/10)) * (dt * 10)
        
        vx, vy = v
        
        dim = self._dim
        
        if x < bounds[0] or x > bounds[2]:
            vx *= -1
        elif y <= bounds[1] or y > bounds[3]:
            vy *= -1

        dx = velocity * vx
        dy =  velocity * vy
        self.dx = dx
        self.dy = dy
        self.v = (vx, vy)
        #self.dx = x - self._px 
        #self.dy = y - self._py

        #self._px = self._x
        #self._py = self._y
        
        self._x += dx
        self._y += dy
        return self 

groups = {}
def create_particles(bounds, num, dim = 10, order = 1):
    
    if groups.get(order) is None:
        groups[order] = py.graphics.Group(order=order)

    particle_batch = py.graphics.Batch()
    
    shapes = []
    particles = []
    for _ in range(num):
        p = Particle(bounds, dim)
        particles.append(p.spawn())

        shape = py.shapes.Circle(
            x = p._x, y = p._y, radius = p._dim / 2, 
            color=c(), batch = particle_batch, group = groups[order]
        )
        shapes.append(shape)

    return [particle_batch, particles, shapes] 

fps_display = get_fps_display(window)

print(window.width)
bounds = (0, 0, window.width, window.height)
batch_small = create_particles(bounds, 500, dim=4, order=0)
batch_med = create_particles(bounds, 250, dim=8, order=1)
batch_big = create_particles(bounds, 100, dim=12, order=2)

flips = []
def update_colors (dt, shapes):

    for idx, shape in enumerate(shapes, 0):
        colidx = randint(0, 2)
        if len(flips) <= idx:
            flips.append(10)
        flip = flips[idx]
        cols = list(shape.color)
        
        if (cols[colidx] < 12 and flip < 0 ) or (cols[colidx] > 243 and flip > 0):
            flip *= -1
        cols[colidx] += flip     
        shape.color = cols
        flips[idx] = flip
        
def update(dt, group):
    _, particles, particle_shapes = group
    for idx, _ in enumerate(particles, 0):
        p = particles[idx]
        p.update(dt)
        particle_shapes[idx].x += p.dx
        particle_shapes[idx].y += p.dy  



@window.event
def on_draw():
    window.clear()
    fps_display.draw()
    batch_small[0].draw()
    batch_med[0].draw()
    batch_big[0].draw()

py.clock.schedule(lambda dt: update(dt, batch_small))
py.clock.schedule(lambda dt: update(dt, batch_med))
py.clock.schedule(lambda dt: update(dt, batch_big))
py.clock.schedule_interval(lambda dt: update_colors(dt, batch_small[2] + batch_med[2] + batch_big[2]), 1/15)

py.app.run()