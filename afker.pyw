import time, tkinter, afker2 as s, _thread
wasRunningScript = False

def toggleOnOff():
    global wasRunningScript
    s.runningScript = not s.runningScript
    wasRunningScript = s.runningScript
    pleaseDontLogOff()
        
def pleaseDontLogOff():
    if(s.runningScript):
        s.typeThis(keysEntry[s.index].get())
        try: gui.after(int(float(delayEntry[s.index].get()) * 1000), pleaseDontLogOff)
        except: print(delayEntry[s.index].get(),' is not a valid input.')
        
def changeScript():
    s.changePreset = True
    print('Changing macro.')
    s.runningScript = False
    print('starting new next key thread')
    _thread.start_new_thread(s.nextKey_thread, ())
    print('waiting for next key input')
    while(s.waitingForNextKey):
        time.sleep(0.1)
    hi = s.index
    textis = 'Preset ' + str(hi) + ' Loaded'
    presetLoadedLabel.config(text = textis)
    gui.update_idletasks()
    pleaseDontLogOff()
    
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
    if(s.changePreset):
        s.changePreset = False
        changeScript()
    gui.after(50, backgroundTask)

def pressOnSync():
    global wasRunningScript
    s.runningScript = False
    wasRunningScript = False
    temp = time.strftime("%S", time.localtime())
    while(temp[1] != '0' and temp[1] != '5'):
        temp = time.strftime("%S", time.localtime())
    s.runningScript = True
    wasRunningScript = True
    pleaseDontLogOff()
    
def changePresetFunc(i):
    s.index = i
    textis = 'Preset ' + str(i) + ' Loaded'
    presetLoadedLabel.config(text = textis)
    gui.update_idletasks()
    s.changePreset = False
    pleaseDontLogOff()

_thread.start_new_thread(s.input_thread, ())
gui = tkinter.Tk()
gui.title('Key masher')

go = tkinter.Button(gui,text = "Press Keys", command = toggleOnOff, width = 10)
go.grid(row = 0)
onSyncButton = tkinter.Button(gui, text = "Sync Keys", command = pressOnSync, width = 10)
onSyncButton.grid(row = 0, column = 1)
statuslbl = tkinter.Label(gui)
statuslbl.config(text = 'Not pressing keys or anything.')
statuslbl.grid(row = 0, column = 2)
tkinter.Label(gui, text = 'Press key(s): ').grid(row = 1, column = 1)
tkinter.Label(gui, text = 'Repeat every x seconds: ').grid(row = 1, column = 2)
presetLoadedLabel = tkinter.Label(gui)
presetLoadedLabel.config(text = 'Preset 0 Loaded')
presetLoadedLabel.grid(row = 1, column = 0)

#input row
keysEntry = []
delayEntry = []
presetButton = []
for i in range(10):
    try:
        keysEntry.append(tkinter.Entry(gui, width = 35))
        delayEntry.append(tkinter.Entry(gui, width = 10))
        keysEntry[i].insert(0, s.hotkeys[4+i*2])
        delayEntry[i].insert(0, s.hotkeys[5+i*2])
        keysEntry[i].grid(row = i+2, column = 1)
        delayEntry[i].grid(row = i+2, column = 2)
        presetButton.append(tkinter.Button(gui, text = 'Enable ' + str(i), command = lambda temp = i: changePresetFunc(temp)))
        presetButton[i].grid(row = i+2, column = 0)
    except:
        print('index ', i, 'has no preset values and is not being loaded')

gui.after(100, backgroundTask)
gui.mainloop()
s.closeProgram = True
