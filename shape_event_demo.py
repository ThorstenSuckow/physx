import pyglet as py
from random import randint
from Particle import Particle, particle2pyglet
from pyglet.window import key
import time
from ShapeEvent import ShapeEvent

# use translate function to swap coords origin
# in pyglet, 0/0 coords are at the bottom left of the screen  
window = py.window.Window(1280, 720, vsync = False)

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
        shape = particle2pyglet(p, particle_batch, groups, order)
        shapes.append(shape)

    return [particle_batch, particles, shapes] 

fps_display = get_fps_display(window)

bounds = (0, 0, window.width, window.height)
batches = [
    create_particles(bounds, 2000, dim=10, order=0),
]

        
shape_event = None
def update(dt, group):
    global shape_event

    event_ns = time_ns = time.time_ns()
    
    if shape_event is not None:
        radius = shape_event.source.radius
        center_x = shape_event.x
        center_y = shape_event.y
        event_ns = shape_event.ns


    _, particles, particle_shapes = group
    for idx, _ in enumerate(particles, 0):
        p = particles[idx]

        if shape_event is not None:
            if (p._x-center_x)**2 + (p._y - center_y)**2 < radius**2:
                p.trigger(shape_event)
               
        p.update(dt)
        particle_shapes[idx].position = (p._x, p._y, 0)  
    
    if time_ns - event_ns > 0:#500_000_000:
        shape_event = None

event_batch = py.graphics.Batch()
def show_circle(x, y, circle):

    if circle is not None:
        circle.position = (x, y)
        return circle
        
    circle = py.shapes.Circle(x, y, 30, color=(255, 255, 255), batch=event_batch)
    circle.opacity = 0
    return circle

circle = None
def on_mouse_press(x, y, button, modifiers):
    global circle, shape_event
    circle = show_circle(x, y, circle)
    shape_event = ShapeEvent(x, y, time.time_ns(), source = circle)
    
    pass

window.push_handlers(on_mouse_press)

@window.event
def on_draw():
    window.clear()
    for batch in batches:
        batch[0].draw()

    event_batch.draw()
    fps_display.draw()    


for idx, batch in enumerate(batches, 0):
    py.clock.schedule(update, batch)


py.app.run()