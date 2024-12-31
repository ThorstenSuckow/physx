import pyglet
from pyglet.gl import *
import random
import math

window = pyglet.window.Window(width=1280, height=720)

vertex_source = """#version 150 core
    uniform vec2 offset;
    attribute vec2 position;
    void main()
    {
    gl_Position = vec4(position + offset, 0.0, 1.0);
    }
"""

fragment_source = """#version 150 core
    void main()
    {
        gl_FragColor.rgb = vec3(1.0, 0.0, 0.0);
    }
"""

batch = pyglet.graphics.Batch()

# Re-use vertex source and create new shader with alpha testing.
vertex_shader = pyglet.graphics.shader.Shader(vertex_source, "vertex")
fragmet_shader = pyglet.graphics.shader.Shader(fragment_source, "fragment")
shader = pyglet.graphics.shader.ShaderProgram(vertex_shader, fragmet_shader)

vertices = []
NUM = 5000

for _ in range(0, NUM):
    base_x = random.randint(-100, 100) / 100
    base_y = random.randint(-100, 100) / 100
    
    triangle_data = [
        base_x + 0.0,  base_y + 0.0,  # Vertex 1
        base_x + 0.01, base_y +  0.0,  # Vertex 2
        base_x + 0.0,  base_y + 0.01   # VErtex 3
    ]

    vertex_list = shader.vertex_list_indexed(
    3, GL_TRIANGLES, [0, 1, 2], batch, None,
    position=('f', triangle_data)
    )
    vertices.append(vertex_list)


dx = 0
dy = 0
def update(dt):
    global dx
    global dy
    dx += 0.001
    dy += 0.001
    
    for v in vertices:
        #triangle_data[0] = (triangle_data[0] + 0.001) % 1
        #triangle_data[2] = (triangle_data[2] + 0.001) % 1
        #triangle_data[4] = (triangle_data[4] + 0.001) % 1
        
        v.position[:] = list(map(lambda x: x+0.0001, v.position))

    pass    

def get_fps_display(window):
    fps_display = pyglet.window.FPSDisplay(window=window)
    fps_display.label.y = window.height - 50
    fps_display.label.x = window.width - 100
    return fps_display

fps_display = get_fps_display(window)


@window.event
def on_draw():
    window.clear()
    
    batch.draw()
    fps_display.draw()    

pyglet.clock.schedule_interval(update, 1/60)

pyglet.app.run()