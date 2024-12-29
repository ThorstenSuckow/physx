from random import randint

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
        
        self._x += dx
        self._y += dy
        return self 
