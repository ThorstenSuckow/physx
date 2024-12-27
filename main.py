import tkinter
import sys
import time
from IShape import IShape
from Block import Block

V = {
    37: (-1, 0), 
    38: (0, -1),
    39: (1, 0),
    40: (0, 1)
}

def _get_dir(keycode):
    if V.get(keycode):
        return V[keycode]
    
    return (0, 0)

def _key_handler(event):
    #print(event.char, event.keysym, event.keycode)
    keycode = event.keycode
    
    if keycode == 38:
        i1.rotate().render(canvas)
        return

    dir = _get_dir(event.keycode)
    i1.update_by(canvas=canvas, x=dir[0] * 10 , y=dir[1] * 10)


last = time.time_ns() // 1_000_000
def _render_world():
    global last
    dir = V[40]

    current = time.time_ns() // 1_000_000 # ms
    if (current - last) >= 1000: # ~ 1 secs 
        i1.update_by(canvas=canvas, x=dir[0] * 10 , y=dir[1] * 10)
        #i2.update_by(canvas=canvas, x=dir[0] * 10 , y=dir[1] * 10)
        
        last = current

    canvas.after(100, _render_world)

    pass

win = tkinter.Tk()
win.title("physx")

canvas = tkinter.Canvas(win, bg='black')
canvas.pack()

win.resizable(False, False)


i1 = IShape([Block("red"), Block("green"), Block("blue"), Block("yellow")], 100, 150)
i2 = IShape([Block(), Block(), Block(), Block()], 0, 0)

i1.render(canvas)
i2.render(canvas)

_render_world()


win.bind("<Key>", _key_handler)
win.mainloop()



def run(args):
    print(args[1:])

if __name__ == '__main__':
    run(sys.argv)