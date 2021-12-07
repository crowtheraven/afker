import tkinter, afker2 as s, _thread
wasRunningScript = False

def toggleOnOff():
    global wasRunningScript
    s.runningScript = not s.runningScript
    wasRunningScript = s.runningScript
    if(s.runningScript):
        try: gui.after(int(float(entry2.get()) * 1000), pleaseDontLogOff)
        except: print(entry2.get(),' is not a valid input.')
        
def pleaseDontLogOff():
    if(s.runningScript):
        s.typeThis(entry1.get())
        try:
            print('Not afking in ', entry2.get(), ' seconds.')
            gui.after(int(float(entry2.get()) * 1000), pleaseDontLogOff)
        except: print(entry2.get(),' is not a valid input.')

def backgroundTask():
    global wasRunningScript
    if(s.runningScript): 
        statuslbl.config(text = 'It do be hitting keys now.')
        go.config(text = "OMG STOP.")
        gui.update_idletasks()
        if(not wasRunningScript):
            wasRunningScript = True
            try: gui.after(int(float(entry2.get()) * 1000), pleaseDontLogOff)
            except: print(entry2.get(),' is not a valid input.')
    else:
        if(wasRunningScript): wasRunningScript = False
        statuslbl.config(text = 'Not pressing keys or anything.')
        go.config(text = 'PRESS KEYS.')
        gui.update_idletasks()
    gui.after(100, backgroundTask)

gui = tkinter.Tk()
gui.title('Key masher')
go = tkinter.Button(gui,text = "PRESS KEYS.", command = toggleOnOff, width = 10)
go.grid(row = 0)
tkinter.Label(gui, text = 'Press key(s): ').grid(row = 1)
tkinter.Label(gui, text = 'Repeat every x seconds: ').grid(row = 2)
statuslbl = tkinter.Label(gui)
statuslbl.config(text = 'Not pressing keys or anything.')
statuslbl.grid(row = 0, column = 1)
entry1 = tkinter.Entry(gui, width = 30)
entry2 = tkinter.Entry(gui, width = 5)
entry1.insert(0, '{enter}{0.1}/clap{enter}')
entry2.insert(0, '2')
entry1.grid(row = 1, column = 1)
entry2.grid(row = 2, column = 1)
_thread.start_new_thread(s.input_thread, ())
gui.after(100, backgroundTask)
gui.mainloop()
s.closeProgram = True