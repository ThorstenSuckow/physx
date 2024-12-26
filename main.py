import tkinter
import sys
import time

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
    xy = canvas.coords(o)
    dir = _get_dir(event.keycode)
    print(dir)
    canvas.move(o, dir[0] , dir[1])


last = time.time_ns() // 1_000_000
def _render_world():
    global last
    dir = V[40]

    current = time.time_ns() // 1_000_000 # ms
    print(current, last, current-last)
    if (current - last) >= 1000: # 5 secs 
        canvas.move(o, dir[0] * 10 , dir[1] * 10)
        last = current

    canvas.after(100, _render_world)

    pass

win = tkinter.Tk()
win.title("physx")

canvas = tkinter.Canvas(win, bg='black')
canvas.pack()

win.resizable(False, False)

def create_l():
    x = 100
    y = 100
    width = 20
    height = 20
    
    hor_width = 4 * width
    hor_height = 1 * height
    vert_width = 1 * width
    vert_height = 4 * height

    pivot_dia = 10
    pivot_x = x + int(hor_width/2) - int(pivot_dia / 2)
    pivot_y = y + int(hor_height) - int(pivot_dia / 2)

    l = (
        canvas.create_rectangle(x, y,   x + width + 1,  y + height + 1, outline="white", fill="Black"),
        canvas.create_rectangle(x + width, y,   x + 2*width + 1,  y + height + 1, outline="white", fill="Black"),
        canvas.create_rectangle(x + 2*width, y,   x + 3*width + 1,  y + height + 1, outline="white", fill="Black"),
        canvas.create_rectangle(x + 3*width, y,   x + 4*width + 1,  y + height + 1, outline="white", fill="Black"),
        canvas.create_oval(pivot_x, pivot_y, pivot_x + pivot_dia + 1, pivot_y + pivot_dia + 1, outline="red", fill="")
        )

    pass

create_l()
    
o = canvas.create_oval(10,20, 10, 20, outline="white")

_render_world()


win.bind("<Key>", _key_handler)

win.mainloop()



def run(args):
    print(args[1:])

if __name__ == '__main__':
    run(sys.argv)