import tkinter, scriptforgui as s

def toggleOnOff():
    s.runningScript = not s.runningScript
    if(s.runningScript): 
        statuslbl.config(text = 'It is now safe to AFK.')
        go.config(text = "I'm back.")
        gui.update_idletasks()
        gui.after(int(entry2.get()) * 1000, pleaseDontLogOff)
    else:
        statuslbl.config(text = 'It is NOT safe to AFK.')
        go.config(text = 'Time to AFK.')
        gui.update_idletasks()

def pleaseDontLogOff():
    if(s.runningScript):
        s.typeThis(entry1.get())
        try:
            print('Not afking in ', entry2.get(), ' seconds.')
            gui.after(int(entry2.get()) * 1000, pleaseDontLogOff)
        except: print(entry2.get(),' is not a valid input.')

gui = tkinter.Tk()
gui.title('Let me afk')
go = tkinter.Button(gui,text = "I'm back.", command = toggleOnOff, width = 10)
go.grid(row = 0)
tkinter.Label(gui, text = 'Press key(s): ').grid(row = 1)
tkinter.Label(gui, text = 'Repeat every x seconds: ').grid(row = 2)
statuslbl = tkinter.Label(gui)
statuslbl.config(text = 'It is now safe to afk.')
statuslbl.grid(row = 0, column = 1)
entry1 = tkinter.Entry(gui)
entry2 = tkinter.Entry(gui)
entry1.insert(0, '=')
entry2.insert(0, '500')
entry1.grid(row = 1, column = 1)
entry2.grid(row = 2, column = 1)
gui.mainloop()
