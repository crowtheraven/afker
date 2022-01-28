from pynput.keyboard import Controller as keyboard, Listener, Key
from pynput.mouse import Controller as mouse, Button
import time, csv, winsound, random

#initialize variables
keyPressed = False
runningScript = False
closeProgram = False
changePreset = False
index = 0
waitingForNextKey = True
randomLines = []

class Command:
    def __init__(self, keyIn, onPress, onRelease):
        self.keyIn = keyIn
        self.onPress = onPress
        self.onRelease = onRelease
        
class hotkeyCheck:
    index = 0
    def __init__(self, word):
        self.word = word

def handleBrackets(word, i, release):
    temp = ''
    while(word[i] != '}' and word[i] != '{'):
        temp = temp + word[i]
        i = i + 1
    #numeric >> insert wait
    try:
        temp = float(temp)
        time.sleep(temp)
        return i, False
    #special key
    except:
        try:
            key = findKey(temp)
            keyboard().press(key)
            if(release): keyboard().release(key)
            return i, key
        except:
            print("ERROR: can't press Key.", temp)
        return i, False

def pressThese(word):
    typeThis(word)

def typeThis(word):
    i = 0
    while(i < len(word)):
        #either special key or a wait
        if(word[i] == '{'):
            i = i + 1
            if(word[i] != '{'): i = handleBrackets(word, i, True)[0]
            else:
                keyboard().press('{')
                keyboard().release('{')
        #press multiple keys at once
        elif(word[i] == '<'):
            i = i + 1
            temp = []
            while(word[i] != '>' and word[i] != '<'):
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
            if(word[i] == '<'):
                keyboard().press('<')
                keyboard().release('<')
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
        #run in random direction
        elif(word[i] == '['):
            spacebarred = False
            i = i + 1
            pressArray = []
            if(not word[i].isnumeric()):
                spacebarred = True
                while(not word[i].isnumeric()):
                    pressArray.append(word[i])
                    i = i + 1
            temp = ''
            while(word[i] != ']' and word[i] != '['):
                temp = temp + word[i]
                i = i + 1
            try: wait = float(temp)
            except: print(temp + ' within []s is not a number')
            rand = random.randrange(0, 8)
            if(rand == 0):
                keyboard().press('w')
                if(spacebarred): pressThese(pressArray)
                time.sleep(wait)
                keyboard().release('w')
            elif(rand == 1):
                keyboard().press('a')
                if(spacebarred): pressThese(pressArray)
                time.sleep(wait)
                keyboard().release('a')
            elif(rand == 2):
                keyboard().press('s')
                if(spacebarred): pressThese(pressArray)
                time.sleep(wait)
                keyboard().release('s')
            elif(rand == 3):
                keyboard().press('d')
                if(spacebarred): pressThese(pressArray)
                time.sleep(wait)
                keyboard().release('d')
            elif(rand == 4):
                keyboard().press('w')
                keyboard().press('a')
                if(spacebarred): pressThese(pressArray)
                time.sleep(wait)
                keyboard().release('w')
                keyboard().release('a')
            elif(rand == 5):
                keyboard().press('a')
                keyboard().press('s')
                if(spacebarred): pressThese(pressArray)
                time.sleep(wait)
                keyboard().release('a')
                keyboard().release('s')
            elif(rand == 6):
                keyboard().press('s')
                keyboard().press('d')
                if(spacebarred): pressThese(pressArray)
                time.sleep(wait)
                keyboard().release('s')
                keyboard().release('d')
            else:
                keyboard().press('d')
                keyboard().press('w')
                if(spacebarred): pressThese(pressArray)
                time.sleep(wait)
                keyboard().release('d')
                keyboard().release('w')
            if(word[i] == '['):
                keyboard().press('[')
                keyboard().release('[')
        #type random message
        elif(word[i] == '?'):
            time.sleep(0.1)
            keyboard().press(Key.enter)
            keyboard().release(Key.enter)
            time.sleep(0.1)
            rand = random.randrange(0, len(randomLines))
            typeThis = str(randomLines[rand])
            for i in range(len(typeThis)-4):
                keyboard().press(typeThis[i+2])
                keyboard().release(typeThis[i+2])
            time.sleep(0.1)
            keyboard().press(Key.enter)
            keyboard().release(Key.enter)
        else:
            keyboard().press(word[i])
            keyboard().release(word[i])
        i = i + 1

def on_press(key):
    global keyPressed, runningScript, changePreset
    if(not keyPressed):
        if(str(key) == hotkeys[0]):#toggle on/off
            if(hotkeys[2] == 'True'):
                if(not runningScript): winsound.Beep(600, 400)
                if(runningScript): winsound.Beep(50, 400)
            runningScript = not runningScript
        elif(str(key) == hotkeys[1]):#wait and then toogle on/off
            if(hotkeys[2] == 'True'):
                if(not runningScript): winsound.Beep(600, 400)
                if(runningScript): winsound.Beep(50, 400)
            temp = time.strftime("%S", time.localtime())
            while(temp[1] != '0' and temp[1] != '5'):
                temp = time.strftime("%S", time.localtime())
            runningScript = not runningScript
        elif(str(key) == hotkeys[3]):#change preset
            print('time to change preset')
            changePreset = True        
    keyPressed = True

def on_release(key):
    global keyPressed
    keyPressed = False
    return False

#this is where the main part of the code starts executing
def input_thread():
    while (not closeProgram):
        with Listener(on_press = on_press, on_release = on_release) as listener:
            listener.join()
    return False

def nextKey_thread():
    global waitingForNextKey
    waitingForNextKey = True
    while(changePreset):
        with Listener(on_press = changingPreset, on_release = windowIsKill) as listener:
            listener.join()
    print('next key thread should be closing*')
    return False

def windowIsKill(key):
    return False
        
def changingPreset(key):
    global changePreset, index, waitingForNextKey
    if(changePreset):
        try:
            index = keyToInt(key)
            print('now using preset ', index)
        except: print('ERROR: not valid input')
        changePreset = False
    else: print('not changing preset')
    waitingForNextKey = False

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

def loadSettings(openThis):
    hotkeys = []
    with open(openThis, 'r') as file:
        reader = csv.reader(file, delimiter = ',')
        for row in reader:
            hotkeys.append(row[1])
        file.close()
        return hotkeys
    
def loadRandomLines():
    randomLines = []
    with open('randomlines.txt', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            randomLines.append(row)
        file.close()
        return randomLines
                
try: hotkeys = loadSettings('afker.txt')
except:
    try: hotkeys = loadSettings('afker.csv')
    except: print('ERROR: failed to open afker.txt')
time.sleep(0.1)
try: randomLines = loadRandomLines()
except: print('ERROR: failed to load randomlines.txt')

