from random import randint
import pyglet as py


class Particle:
    _bounds = None
    v = None
    dx = dy = _x = _y = _px = _py = _dim = _age = 0
    _triggered_at = _acceleration = 0

    def __init__(self, bounds, dim = None):
        self._dim = dim
        self._bounds = bounds
        pass

    def trigger(self, event):
        self._triggered_at = self._age
        self._acceleration = 20
        x = self._x
        y = self._y
        event_x = event.x
        event_y = event.y
        vx = self.v[0]
        vy = self.v[1]
        
        if (x < event_x and vx == 1) or (x > event_x and vx == -1):
            vx *= -1
        if (y < event_y and vy == 1) or (y > event_y and vy == -1):
            vy *= -1
            
        self.v = (vx, vy)

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
        self._age += dt
        x = self._x
        y = self._y
        dim = self._dim
        v = self.v
        bounds = self._bounds

        velocity = max(0.005, (dim/10)) * (dt * 10) * self._acceleration
        

        self._acceleration = max(1, self._acceleration - (0.1 if self._acceleration > 10 else 0.01))
        
        
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
        
        self._x += dx
        self._y += dy
        return self 
    
py.resource.path = ['./resources']
py.resource.reindex()

img = py.resource.image("sprite.png")

def particle2pyglet(particle, particle_batch, groups, order):
    p = particle
    cl = (255, randint(0, 255), randint(0, 255))#50)
    #shape = py.shapes.Circle(
    shape = py.sprite.Sprite(img=img,
        x = p._x, y = p._y, z = 0,
        #radius = p._dim / 2, 
        batch = particle_batch, group = groups[order]
    )
    shape.color=cl
    shape.width=p._dim 
    shape.height=p._dim 
    
    shape.opacity = randint(0, 255)
    return shape
        