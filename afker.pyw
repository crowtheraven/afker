import time, tkinter, afker2 as s, _thread
wasRunningScript = False

def toggleOnOff():
    global wasRunningScript
    s.runningScript = not s.runningScript
    wasRunningScript = s.runningScript
    pleaseDontLogOff()
        
def pleaseDontLogOff():
    if(s.runningScript):
        s.typeThis(entry1.get())
        try: gui.after(int(float(entry2.get()) * 1000), pleaseDontLogOff)
        except: print(entry2.get(),' is not a valid input.')

def backgroundTask():
    global wasRunningScript
    if(s.runningScript): 
        statuslbl.config(text = 'It do be hitting keys now.')
        go.config(text = "OMG STOP.")
        gui.update_idletasks()
        if(not wasRunningScript):
            wasRunningScript = True
            pleaseDontLogOff()
    else:
        if(wasRunningScript): wasRunningScript = False
        statuslbl.config(text = 'Not pressing keys or anything.')
        go.config(text = 'Press Keys')
        gui.update_idletasks()
    gui.after(50, backgroundTask)

def pressOnMinute():
    global wasRunningScript
    s.runningScript = False
    wasRunningScript = False
    temp = time.strftime("%S", time.localtime())
    while(temp[1] != '0' and temp[1] != '5'):
        temp = time.strftime("%S", time.localtime())
    s.runningScript = True
    wasRunningScript = True
    pleaseDontLogOff()

gui = tkinter.Tk()
gui.title('Key masher')
go = tkinter.Button(gui,text = "Press Keys", command = toggleOnOff, width = 10)
go.grid(row = 0)
onMinuteButton = tkinter.Button(gui, text = "Sync Keys", command = pressOnMinute, width = 10)
onMinuteButton.grid(row = 3)
tkinter.Label(gui, text = 'Press key(s): ').grid(row = 1)
tkinter.Label(gui, text = 'Repeat every x seconds: ').grid(row = 2)
statuslbl = tkinter.Label(gui)
statuslbl.config(text = 'Not pressing keys or anything.')
statuslbl.grid(row = 0, column = 1)
entry1 = tkinter.Entry(gui, width = 30)
entry2 = tkinter.Entry(gui, width = 5)
entry1.insert(0, '{enter}{0.1}/dance{enter}')
entry2.insert(0, '600')
entry1.grid(row = 1, column = 1)
entry2.grid(row = 2, column = 1)
_thread.start_new_thread(s.input_thread, ())
gui.after(100, backgroundTask)
gui.mainloop()
s.closeProgram = True