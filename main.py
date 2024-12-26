import tkinter
import sys

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


win = tkinter.Tk()
win.title("physx")

canvas = tkinter.Canvas(win, bg='black')
canvas.pack()

win.resizable(False, False)

o = canvas.create_oval(5, 5, 100, 100, outline="white", fill="Black")

win.bind("<Key>", _key_handler)

win.mainloop()



def run(args):
    print(args[1:])

if __name__ == '__main__':
    run(sys.argv)