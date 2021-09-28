from pynput.keyboard import Controller as keyboard, Listener, Key
from pynput.mouse import Controller as mouse, Button
import time, csv, os

#initialize variables
keyPressed = False
runningScript = True
closeProgram = False
changeCsvInput = True
changeScriptEvent = False
csvRunning = ''
updateScriptLbl = False

class Command:
    def __init__(self, keyIn, onPress, onRelease):
        self.keyIn = keyIn
        self.onPress = onPress
        self.onRelease = onRelease
        
class hotkeyCheck:
    index = 0
    def __init__(self, word):
        self.word = word
        
def listFiles(path):
    allFiles = os.listdir(path)
    print('looking in directory: ', path)
    goodFiles = []
    printThis = ['KEY\t  FILE']
    for file in allFiles:
        #checks for file extension, returns only .txt and .csv
        try: extension = file.split('.',2)[1]
        except: extension = ''
        if(extension == 'txt' or extension == 'csv'):
            #currently only supports 10 files
            if(len(goodFiles) < 10): 
                if(file != 'settings.csv' and file != 'settings.txt'): goodFiles.append(file)
            else:
                printThis.append('You have more files than the amount supported.')
                break
    for i in range(len(goodFiles)):
        temp = str(i) + '\t   ' + str(goodFiles[i])
        printThis.append(temp)
    return goodFiles, printThis

def handleBrackets(word, i, release):
    #numeric >> insert wait
    if(word[i].isnumeric()):
        moveDecimal = False
        temp = 0
        while(word[i] != '}'):
            if(word[i] == '.'):
                decimalPlace = 1
                moveDecimal = True
            elif(moveDecimal == True):
                temp = temp + (int(word[i]) / (decimalPlace * 10))
                decimalPlace = decimalPlace + 1
            else:
                temp = (temp * 10) + int(word[i])
            i = i + 1
        time.sleep(temp)
        return i, False
    #special key
    else:
        temp = word[i]
        i = i + 1
        while(word[i] != '}'):
            temp = temp + word[i]
            i = i + 1
        try:
            key = findKey(temp)
            keyboard().press(key)
            if(release): keyboard().release(key)
            return i, key
        except:
            print("ERROR: can't press Key.", temp)
        return i, False

def typeThis(word):
    i = 0
    while(i < len(word)):
        #either special key or a wait
        if(word[i] == '{'):
            i = i + 1
            i = handleBrackets(word, i, True)[0]
        #press multiple keys at once
        elif(word[i] == '<'):
            i = i + 1
            temp = []
            while(word[i] != '>'):
                #either special key or a wait
                if(word[i] == '{'):
                    i = i + 1
                    i, key = handleBrackets(word, i, False)
                    if(key != False): temp.append(key)
                else:
                    keyboard().press(word[i])
                    temp.append(word[i])
                i = i + 1
            for j in temp:
                keyboard().release(j)
        #mouse clicks
        elif(word[i] == '('):
            i = i + 1
            while(word[i] != ')'):
                if(word[i] == 'l'):
                    mouse().press(Button.left)
                    mouse().release(Button.left)
                elif(word[i] == 'r'):
                    mouse().press(Button.right)
                    mouse().release(Button.right)
                else: print('ERROR: not valid mouse input: ', word[i])
                i = i + 1
        else:
            keyboard().press(word[i])
            keyboard().release(word[i])
        i = i + 1

def openCsv(openThis):
    commands = []
    with open(openThis, 'r') as file:
        reader = csv.reader(file, delimiter = ',')
        for row in reader:
            commands.append(Command(row[0],row[1],row[2]))
    return commands, openThis

def settingsCsv(openThis):
    hotkeys = []
    with open(openThis, 'r') as file:
        reader = csv.reader(file, delimiter = ',')
        for row in reader:
            hotkeys.append(row[1])
        return hotkeys

def on_press(key):
    global keyPressed, runningScript, closeProgram, commands, changeScriptEvent
    keyPressed = True
    for i in range(len(hotkeys)):
        if(str(key) == hotkeys[i]):
            if(i == 0):#enable
                runningScript = True
            if(i == 1):#disable
                runningScript = False
            if(i == 2):#close
                print('Script closing.')
                closeProgram = True
                runningScript = False
            if(i == 3):#change script
                changeScriptEvent = True
    #blocks it from typing in the chat
    if(key == Key.enter):
        runningScript = False
    for readyCheck in readychecks:
        if(checkThis(readyCheck, key)):
            time.sleep(0.1)
            runningScript = True
            typeThis(hotkeys[4])
    #commands
    if(runningScript):
        for command in commands:
            if(str(key) == command.keyIn):
                typeThis(command.onPress)

def on_release(key):
    global keyPressed
    keyPressed = False
    if(runningScript):
        for command in commands:
            if(str(key) == command.keyIn):
                typeThis(command.onRelease)
    return False

#this is where the main part of the code starts executing
def input_thread():
    global hotkeys, readychecks, commands, csvRunning
    if(csvRunning == ''):
        #open default csv titled def.csv
        try: commands, csvRunning = openCsv('def.csv')
        except: print('ERROR: failed to open default def.csv')
    readMe(commands, csvRunning)
    hotkeys = settingsCsv('settings.csv')
    readychecks = [hotkeyCheck(['Key.enter',"'r'",'Key.enter']),hotkeyCheck(["'/'","'p'",'Key.space',"'r'","Key.enter"])]
    while (not closeProgram):
        with Listener(on_press = on_press, on_release = on_release) as listener:
            listener.join()
    print('input thread should be closing*')
    return False

def nextKey_thread():
    while(changeCsvInput):
        with Listener(on_press = changingCsvs, on_release = windowIsKill) as listener:
            listener.join()
    print('next key thread should be closing*')
    return False

def windowIsKill(key):
    return False
        
def changingCsvs(key):
    global changeScriptEvent, changeCsvInput, files, commands, csvRunning, updateScriptLbl
    if(changeCsvInput):
        try:
            num = keyToInt(key)
            print(num)
            try: commands, csvRunning = openCsv(files[num])
            except: 
                try: print('ERROR: failed to open ', files[num])
                except: print('ERROR: input out of range')
        except: print('ERROR: not valid input')
        changeCsvInput = False
        readMe(commands, csvRunning)
    else: print('not changing csv input')
    updateScriptLbl = False
        
#print off commands currently being executed by the code
def readMe(commands, csvTitle):
    print('')
    print('top text\n')
    print('Macro running: ', csvTitle)
    print('\nInputs\tOn Press\tOn Release')
    for command in commands:
        print(command.keyIn,'\t',command.onPress,'\t\t',command.onRelease)
    print('\nbottom text')
    print('')

def findKey(string):
    if(string == 'f1'): return Key.f1
    if(string == 'f2'): return Key.f2
    if(string == 'f3'): return Key.f3
    if(string == 'f4'): return Key.f4
    if(string == 'f5'): return Key.f5
    if(string == 'f6'): return Key.f6
    if(string == 'f7'): return Key.f7
    if(string == 'f8'): return Key.f8
    if(string == 'f9'): return Key.f9
    if(string == 'f10'): return Key.f10
    if(string == 'f11'): return Key.f11
    if(string == 'f12'): return Key.f12
    if(string == 'space'): return Key.space
    if(string == 'enter'): return Key.enter
    if(string == 'tab'): return Key.tab
    if(string == 'shift'): return Key.shift
    if(string == 'ctrl'): return Key.ctrl
    if(string == 'alt'): return Key.alt
    
def keyToInt(key):
    if(str(key) == "'1'"): return 1
    if(str(key) == "'2'"): return 2
    if(str(key) == "'3'"): return 3
    if(str(key) == "'4'"): return 4
    if(str(key) == "'5'"): return 5
    if(str(key) == "'6'"): return 6
    if(str(key) == "'7'"): return 7
    if(str(key) == "'8'"): return 8
    if(str(key) == "'9'"): return 9
    if(str(key) == "'0'"): return 0

#for keywords/hotkeys
def checkThis(readycheck, key):
    if(readycheck.word[readycheck.index] == str(key)):
        readycheck.index = readycheck.index + 1
        if(readycheck.index == len(readycheck.word)):
            readycheck.index = 0
            return True
        else: return False
    else:
        if(readycheck.index == 0): return False
        else:
            readycheck.index = 0
            checkThis(readycheck, key)