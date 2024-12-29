import pyglet as py
from random import randint
from Particle import Particle
from Block import Block
from IShape import IShape, ishape2pyglet
from pyglet.window import key

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

        cl = (255, randint(0, 255), randint(0, 255))#50)
        shape = py.shapes.Circle(
            x = p._x, y = p._y, radius = p._dim / 2, 
            color=cl, batch = particle_batch, group = groups[order]
        )
        shape.opacity = randint(0, 255)
        shapes.append(shape)

    return [particle_batch, particles, shapes] 

fps_display = get_fps_display(window)

bounds = (0, 0, window.width, window.height)
batches = [
    create_particles(bounds, 500, dim=4, order=0),
    create_particles(bounds, 250, dim=8, order=1),
    create_particles(bounds, 100, dim=12, order=2)
]

opacity = []
def update_opacity(dt, batch):
    i = 0
    for b in batch:
        for s in b[2]:
            if len(opacity) <= i:
                opacity.append(1)
            
            flip = opacity[i]
            if (s.opacity == 255 and flip > 0) or (s.opacity == 0 and flip < 0):
                opacity[i] *= -1
        
            s.opacity += opacity[i]
            i+=1
            
        
def update(dt, group):
    _, particles, particle_shapes = group
    for idx, _ in enumerate(particles, 0):
        p = particles[idx]
        p.update(dt)
        particle_shapes[idx].position = (p._x, p._y)  


def block(color):
    return Block(width=25, height=25, color=color, opacity=128)

col = c()
ishape = IShape([block(col), block(col), block(col), block(col)], 600, 400)

def on_key_press(symbol, modifiers):
    if symbol == key.UP:
        ishape.rotate().update()

window.push_handlers(on_key_press)

@window.event
def on_draw():
    window.clear()
    for batch in batches:
        batch[0].draw()

    
    fps_display.draw()    
    ishape2pyglet(ishape)


for idx, batch in enumerate(batches, 0):
    py.clock.schedule(update, batch)

py.clock.schedule_interval(update_opacity, 1/15, batches)

py.app.run()