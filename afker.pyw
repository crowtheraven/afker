import tkinter, scriptforgui as s

def toggleOnOff():
    s.runningScript = not s.runningScript
    if(s.runningScript): 
        statuslbl.config(text = 'Mashing tf out of these keys my dude.')
        go.config(text = "OMG STOP.")
        gui.update_idletasks()
        try: gui.after(int(entry2.get()) * 1000, pleaseDontLogOff)
        except: print(entry2.get(),' is not a valid input.')
    else:
        statuslbl.config(text = 'Not pressing keyos.')
        go.config(text = 'PRESS KEYS.')
        gui.update_idletasks()

def pleaseDontLogOff():
    if(s.runningScript):
        s.typeThis(entry1.get())
        try:
            print('Not afking in ', entry2.get(), ' seconds.')
            gui.after(int(entry2.get()) * 1000, pleaseDontLogOff)
        except: print(entry2.get(),' is not a valid input.')

gui = tkinter.Tk()
gui.title('Key masher')
go = tkinter.Button(gui,text = "OMG STOP.", command = toggleOnOff, width = 10)
go.grid(row = 0)
tkinter.Label(gui, text = 'Press key(s): ').grid(row = 1)
tkinter.Label(gui, text = 'Repeat every x seconds: ').grid(row = 2)
statuslbl = tkinter.Label(gui)
statuslbl.config(text = 'Mashing tf out of these keys my dude.')
statuslbl.grid(row = 0, column = 1)
entry1 = tkinter.Entry(gui, width = 30)
entry2 = tkinter.Entry(gui, width = 5)
entry1.insert(0, '{enter}{0.1}/clap{enter}')
entry2.insert(0, '2')
entry1.grid(row = 1, column = 1)
entry2.grid(row = 2, column = 1)
gui.mainloop()
