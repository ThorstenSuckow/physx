import time
def V():
    return [
        (-1,0),
        (0, 1),
        (1, 0),
        (0, -1)
    ]

def rgb(r, g, b):
    return '#%02x%02x%02x' % (r, g, b)

def calltime(since):
    stop = time.perf_counter_ns()
    ns = stop - since
    ms = (ns / 1_000_000)
    sec = ns / 1_000_000_000
    fps = 1/sec
    return [ns, ms, sec, fps]
    