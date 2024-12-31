class ShapeEvent:

    ns = x = y = 0
    source = None
    
    def __init__(self, x, y, ns, source):
        self.x = x
        self.y = y
        self.ns = ns
        self.source = source