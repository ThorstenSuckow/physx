import pyglet
from pyglet.gl import *
import random
import math
from Particle import Particle
import time
from ShapeEvent import ShapeEvent

WIDTH = 1280
HEIGHT = 720

vertex_list = None

window = pyglet.window.Window(width=WIDTH, height=HEIGHT, vsync=False)

def normalize(w, h):
    quot_w = WIDTH / w if w != 0 else 0 
    quot_h = HEIGHT / h  if h != 0 else 0
    return (1/quot_w if quot_w != 0 else 0, 1/quot_h if quot_h != 0 else 0) 

def normalize_pos(x, y):

    nx = (x - WIDTH / 2) 
    ny = (y - HEIGHT / 2) 

    xb = ((WIDTH / 2) / nx) if nx != 0 else  0  
    yb = ((HEIGHT / 2) / ny) if ny != 0 else 0
    

    return [1/xb if xb != 0 else 0, 1/yb if yb != 0 else 0]
 


vertex_source = """#version 150 core
    attribute vec2 position;
    out vec2 xy;

    void main()
    {
    xy = position;
    gl_Position = vec4(position, 0.0, 1.0);
    }
"""

fragment_source = """#version 150 core
    in vec2 xy;
   
    void main()
    {
        gl_FragColor = vec4(1, 0, 0, 0.5);
    }
"""

batch = pyglet.graphics.Batch()

# Re-use vertex source and create new shader with alpha testing.
vertex_shader = pyglet.graphics.shader.Shader(vertex_source, "vertex")
fragmet_shader = pyglet.graphics.shader.Shader(fragment_source, "fragment")
shader = pyglet.graphics.shader.ShaderProgram(vertex_shader, fragmet_shader)

shape_event = None
def update(dt):
    global shape_event

    event_ns = time_ns = time.time_ns()
    
    if shape_event is not None:
        radius = shape_event.source.radius
        center_x = shape_event.x
        center_y = shape_event.y
        event_ns = shape_event.ns


    global particles
    global triangles
    
    toff = 0
    for idx, _ in enumerate(particles, 0):
        p = particles[idx]
        if shape_event is not None:
            if (p._x-center_x)**2 + (p._y - center_y)**2 < radius**2:
                p.trigger(shape_event)
        p.update(dt)
        x, y = normalize_pos(p._x, p._y)
        w, h = normalize(p._dim, p._dim)
        triangles[toff:] = [
            x,      y,  
            x + w,  y,  
            x + w,  y + h,
            x,      y + h   
        ]

        toff += 8
    vertex_list.position[:] = triangles    

    if time_ns - event_ns > 0:#500_000_000:
        shape_event = None


def get_fps_display(window):
    fps_display = pyglet.window.FPSDisplay(window=window)
    fps_display.label.y = window.height - 50
    fps_display.label.x = window.width - 100
    return fps_display

fps_display = get_fps_display(window)


groups = {}
def create_particles(bounds, num, baseDim=None):
    
    particle_batch = pyglet.graphics.Batch()
    
    indices   = []
    triangles = []
    particles = []

    for i in range(0, num):
        if baseDim is None:
            dim=random.randint(10, 30)
        else: 
            dim = baseDim
            
        p = Particle(bounds, dim)
        particles.append(p.spawn())
        x, y = normalize_pos(p._x, p._y)
        w, h = normalize(p._dim, p._dim)
       
        triangle = [
            x,  y,  
            x + w,  y,  
            x + w,  y + h,
            x,  y + h   
        ]

        triangles += triangle
        indices += list(map(lambda x: x + (i*4), [0, 1, 2, 0, 2, 3]))


    return [particle_batch, particles, triangles, indices] 


bounds = (0, 0, WIDTH, HEIGHT)
batch, particles, triangles, indices = create_particles(bounds, 5000)

vertex_list = shader.vertex_list_indexed(
int(len(triangles) / 2), GL_TRIANGLES, indices, batch, None,
position=('f', triangles)
)

event_batch = pyglet.graphics.Batch()

def show_circle(x, y, circle):
    if circle is not None:
        circle.position = (x, y)
        return circle
        
    circle = pyglet.shapes.Circle(x, y, 30, color=(255, 255, 255), batch=event_batch)
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
    
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    batch.draw()
    fps_display.draw()    

pyglet.clock.schedule_interval(update, 1/60)




pyglet.app.run()