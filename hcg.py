#!/usr/bin/python3

# Ale Cominotti - 2020

print("Loading...")

from resources import CodeGenerator
import time
import random
import os
import argparse
import base64
import re
import webbrowser
import warnings
import platform
import importlib.util
import sys
runningOnLinux = platform.system()=='Linux'
runningOnMac = platform.system()=='Darwin'
runningOnWindows = platform.system()=='Windows'
name = 'selenium'
if name in sys.modules:
    print(f"{name!r} already in sys.modules")
elif (spec := importlib.util.find_spec(name)) is not None:
    import selenium
    from selenium.webdriver import ActionChains
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
else:
    if runningOnWindows:
        os.system("py -m pip install -r resources/requirements.txt")
    else:
        os.system("python3 -m pip install -r resources/requirements.txt")
    print("\033[92mDependencies were installed correctly!. Please restart Hydra Code Generator.\033[0m")
    exit(1)


# User Variables -----
hideBrowserMediaPopUps = True # True if you want to remove microphone and camera permission pop ups. False if you want to use them
keepBrowserOpenAtExit = True  # True: keeps browser open when script is stopped. False: otherwise. NOT WORKING ON WINDOWS
minRandomFunctions = 0 #lower bound value for functions amount
maxRandomFunctions = 5 #upper bound value for functions amount
minRandomArgument = 0  #lower bound value for the source and function arguments
maxRandomArgument = 5  #upper bound value for he source and function arguments
mathArrowFunctionProb = 10 # Probabilities of generating an arrow function that changes value over time (ex.: () => Math.sin(time * 0.3))
mouseArrowFunctionProb = 10 # Probabilities of generating an arrow function that uses mouse position (ex.: () => mouse.x)
modulateItselfProb = 20 # Probabilities of generating a modulation function with "o0" as argument (ex.: modulate(o0,1))

# Put in this list whatever source or function you don't want to be generated:
ignoredList = ["posterize", "thresh", "layer", "modulateScrollX", "modulateScrollY"]
exclusiveSourceList = []
exclusiveFunctionList = []
# End User Variables -----


# Script Variables, DO NOT MODIFY -----
PURPLE = '\033[95m'
CYAN = '\033[96m'     
DARKCYAN = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
ITALIC = '\033[3m'
WHITE = '\033[0m'   
resourcesFolder="resources/"
txtfile="hydraCodes.txt"
terminalSize = os.get_terminal_size().columns
web=False
if(runningOnMac):
    controlKey=Keys.COMMAND
else:
    controlKey=Keys.CONTROL
# End Script Variables -----


def printBanner(terminalSize):
    if(runningOnWindows):
        os.system("cls")
    else:
        os.system("clear")
    if(terminalSize>102):
        print(YELLOW + """  _   _           _              ____          _         ____                           _             
 | | | |_   _  __| |_ __ __ _   / ___|___   __| | ___   / ___| ___ _ __   ___ _ __ __ _| |_ ___  _ __ 
 | |_| | | | |/ _` | '__/ _` | | |   / _ \ / _` |/ _ \ | |  _ / _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
 |  _  | |_| | (_| | | | (_| | | |__| (_) | (_| |  __/ | |_| |  __/ | | |  __/ | | (_| | || (_) | |   
 |_| |_|\__, |\__,_|_|  \__,_|  \____\___/ \__,_|\___|  \____|\___|_| |_|\___|_|  \__,_|\__\___/|_|   
        |___/
                """ + WHITE)
    else:
        print(YELLOW + """  _   _    ____    ____ 
 | | | |  / ___|  / ___|
 | |_| | | |     | |  _ 
 |  _  | | |___  | |_| |
 |_| |_|  \____|  \____|
                        """ + WHITE)
def showInfo():
    printBanner(terminalSize)
    helptxt=open(resourcesFolder + "help.txt", 'r').read()
    print(helptxt)

def printError(message):
    print(RED+"ERROR: " + WHITE + message)


#Argument handling -----
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--function", type=int, metavar='<Integer>', help="Constant amount of functions")
parser.add_argument("-fmin", type=int, metavar='<Integer>', help="Minimum amount of functions")
parser.add_argument("-fmax", type=int, metavar='<Integer>', help="Maximum amount of functions")
parser.add_argument("-amin", type=float, metavar='<Float>', help="Minimum value for arguments")
parser.add_argument("-amax", type=float, metavar='<Float>', help="Maximum value for arguments")
parser.add_argument("-info", "--info", action='store_true', help="Shows longer help and information")
parser.add_argument("-i", "--ignore", type=str, metavar='<source1,source2,func1,func2,...sourceN,funcN>', help="Specify which sources or functions to ignore. (ex.: osc,brightness)")
parser.add_argument("--use-all", action='store_true', help="Doesn't ignore any source or function.")
parser.add_argument("-xs", type=str, metavar='<source1,source2,...sourceN>', help="Specify exclusive sources to use. (ex.: osc,voronoi)")
parser.add_argument("-xf", type=str, metavar='<func1,func2,...funcN>', help="Specify exclusive functions to use. (ex.: colorama,modulate)")
parser.add_argument("-ap", "--arrow-prob", type=int, metavar='<Integer>', help="Probability of generating an arrow function as an argument.")
parser.add_argument("-mp", "--mouse-prob", type=int, metavar='<Integer>', help="Probability of generating a mouse arrow function as an argument.")
parser.add_argument("-mip", "--modulate-itself-prob", metavar='<Integer>', type=int, help='Probability of generating an modulation function with "o0" as an argument.')
parser.add_argument("-web", action='store_true', help="Open hydra in web browser with the generated code")
parser.add_argument("-live", action='store_true', help="Starts a live session where HCG writes automatically to Hydra in the web browser.")
parser.add_argument("-hc", "--hide-code", action='store_true', help="Hides executed code when running a Live Session.")
parser.add_argument("-um", "--use-media", action='store_true', help="Allows camera and microphone in Live Session Mode.")
parser.add_argument("-cb", "--close-browser", action='store_true', help="Closes browser in Live Session Mode when script is stopped. NOT COMPATIBLE WITH WINDOWS")
parser.add_argument("-l", "--localhost", type=str, metavar='<PORT|IP>', help="Allows you to use your locally running Hydra")
args = parser.parse_args()

if args.info:
    showInfo()
    exit(0)
if args.function or args.function==0:
    minRandomFunctions=args.function
    maxRandomFunctions=args.function
else:
    if args.fmin or args.fmin==0:
        minRandomFunctions=args.fmin
        if(minRandomFunctions>maxRandomFunctions):
            maxRandomFunctions=minRandomFunctions
    if args.fmax or args.fmax==0:
        maxRandomFunctions=args.fmax
    if args.fmin and args.fmax and (args.fmin>args.fmax):
        printError("Function max value must be bigger than min value.")
        exit(1)
if args.ignore:
    ignoredList = args.ignore.split(",")
if args.xs:
    exclusiveSourceList = args.xs.split(",")
if args.xf:
    exclusiveFunctionList = args.xf.split(",")
if args.amin:
    minRandomArgument = args.amin
if args.amax:
    maxRandomArgument = args.amax
if args.arrow_prob or args.arrow_prob==0:
    mathArrowFunctionProb = args.arrow_prob
if args.mouse_prob or args.mouse_prob==0:
    mouseArrowFunctionProb = args.mouse_prob
if args.modulate_itself_prob or args.modulate_itself_prob==0:
    modulateItselfProb = args.modulate_itself_prob
if args.use_all:
    ignoredList = []
    exclusiveSourceList = []
    exclusiveFunctionList = []
if args.web and args.live:
    printError("Can't use Web and Live Session mode at the same time.")
    exit(1)
if args.localhost or args.localhost==0:
    hydraURL="https://localhost:" + str(args.localhost) + "/?code="
else:
    hydraURL="https://hydra.ojack.xyz/?code="
if args.web:
    web=True
hideCode=args.hide_code
hideBrowserMediaPopUps = not args.use_media
keepBrowserOpenAtExit = not args.close_browser  

#End argument handling -----

def setWebDriver():
    warnings.simplefilter("ignore", category=DeprecationWarning) # just because I'm using the chromedriver inside hcg folder, not PATH
    opt = Options()
    if hideBrowserMediaPopUps:
        opt.add_argument("--use-fake-ui-for-media-stream")
    opt.add_experimental_option("detach", keepBrowserOpenAtExit)
    caps = webdriver.DesiredCapabilities.CHROME.copy()
    caps['acceptInsecureCerts'] = True
    webDriversRootFolder = "resources/webdrivers/"
    if runningOnLinux:
        driverpath= webDriversRootFolder + "linux/chromedriver"
        os.system("chmod +rwx " + driverpath)
    elif runningOnMac:
        driverpath= webDriversRootFolder + "mac/chromedriver"
    elif runningOnWindows:
        driverpath= webDriversRootFolder + "windows/chromedriver"
    else:
        printError("Your operating system is not compatible with Live Session Mode.")
        exit(1)

    return webdriver.Chrome(executable_path= driverpath, options=opt, desired_capabilities=caps)
    
def hideCodeKeys(action): # presses Ctrl + Shift + H
    action.key_down(controlKey)
    action.key_down(Keys.SHIFT)
    action.key_down("h")
    action.perform()
    action.key_down("h")
    action.key_up(Keys.SHIFT)
    action.key_up(controlKey)                   
    action.perform()

def executeCode(action): # presses Ctrl + Shift + Enter
    action.key_down(controlKey)
    action.key_down(Keys.SHIFT)
    action.key_down(Keys.ENTER)
    action.perform()
    action.key_up(Keys.ENTER)
    action.key_up(Keys.SHIFT)
    action.key_up(controlKey)                   
    action.perform()

def printLiveLoadingInfo(loadingText, loadingArray, loadingBackSpace):
    print(loadingBackSpace, end="\r")
    print(loadingText+loadingArray[random.randint(0,len(loadingArray)-1)], end="\r")

def printLiveCodeStatus(pos):
    if(pos==0):
        print(BOLD+YELLOW+"----------------------------")
        print("Loading new code in Hydra...")
        print("----------------------------")
        print('\033[2A', end="")
    if(pos==1):
        print('\033[1A', end="")
        print(GREEN+"                               ")
        print(GREEN+"                               ")
        print(GREEN+"                               ", end="\r")
        print('\033[2A', end="")      
    if(pos==2):
        print(BOLD+GREEN+"-------------")
        print("Code loaded √")
        print("-------------"+WHITE)

def livePrinting(fullCode, textarea, action, area):
    waitTime=0.01
    loadingText="Loading new code in Hydra "
    loadingBackSpace="                              "
    if runningOnWindows:
        loadingArray=["#", ".", "-", "/", "\\", "^", "+", "<", ">"] # windows friendly...
    else:
        loadingArray=["⠼", "⠩", "⠡", "⠌", "⠴", "⠲", "⠢", "⠦", "⠍"]
    done=False
    while not done:
        try:
            print(loadingText+loadingArray[random.randint(0,len(loadingArray)-1)], end="\r")            
            if args.hide_code:
                hideCodeKeys(action)
            print(loadingText+loadingArray[random.randint(0,len(loadingArray)-1)], end="\r")
            area.click(); #Click on browser screen
            #time.sleep(waitTime) 
            print(loadingBackSpace, end="\r")
            print(loadingText+loadingArray[random.randint(0,len(loadingArray)-1)], end="\r")
            textarea.send_keys(controlKey + "a"); #Ctrl+a to select all code
            #time.sleep(waitTime) 
            print(loadingBackSpace, end="\r")
            print(loadingText+loadingArray[random.randint(0,len(loadingArray)-1)], end="\r")
            textarea.send_keys(fullCode) #writes new code overwriting old one
            #time.sleep(waitTime) 
            print(loadingBackSpace, end="\r")
            print(loadingText+loadingArray[random.randint(0,len(loadingArray)-1)], end="\r")
            executeCode(action)
            print(loadingBackSpace, end="\r")
            print(loadingText+loadingArray[random.randint(0,len(loadingArray)-1)], end="\r")
            area.click(); #Click on browser screen
            if args.hide_code:
                hideCodeKeys(action)
            done = True
        except selenium.common.exceptions.ElementNotInteractableException:
            print("Please click on Hydra text editor to write new code (in the web browser)")
            time.sleep(1)

def encodeText(fullCode):
    #fullCode= fullCode.replace(" ", '%0D')
    #fullCode= fullCode.replace("=", '%3D')
    #fullCode= fullCode.replace("\n", '%0A')
    fullCode= fullCode.replace(">", '%3E') #solves encoding interpretation problems
    fullCode = base64.b64encode(fullCode.encode())
    fullCode= str(fullCode)[2:-1]
    return fullCode

def printMainInformation(hydra, hydraCode):
    info=hydra.getInfo()
    hydraCodeNoHeader = hydraCode[len(info):] 
    terminalSize = os.get_terminal_size().columns
    printBanner(terminalSize)
    staticBar = "----------------------------------------------------------------------------------------------"
    if args.live:
        print(CYAN+BOLD+"LIVE SESSION MODE" + WHITE+CYAN + " [BETA]\n" + WHITE)
    if args.function:
        print(WHITE+"Functions: " + str(minRandomFunctions) + " (Constant)")
    else:
        print(WHITE+"Functions: Random (" + str(minRandomFunctions) + "-" + str(maxRandomFunctions)+")", end="")
        if (not args.function) and (not args.fmin) and (not args.fmax):
            print(DARKCYAN + " (Default)" + WHITE)
        else:
            print()
    print(WHITE+"Argument values: Random (" + str(minRandomArgument) + "-" + str(maxRandomArgument)+")", end="")
    if (not args.amin) and (not args.amax):
        print(DARKCYAN + " (Default)" + WHITE)
    else:
        print()
    print(WHITE+"Arrow functions probability: " + str(mathArrowFunctionProb) +"%", end="")
    if not args.arrow_prob and args.arrow_prob!=0:
        print(DARKCYAN + " (Default)" + WHITE)
    else:
        print()
    print(WHITE+"Mouse arrow functions probability: " + str(mouseArrowFunctionProb) +"%", end="")
    if not args.mouse_prob and args.mouse_prob:
        print(DARKCYAN + " (Default)" + WHITE)
    else:
        print()
    print(WHITE+"Modulate itself probability: " + str(modulateItselfProb) +"%", end="")
    if not args.modulate_itself_prob and args.modulate_itself_prob!=0:
        print(DARKCYAN + " (Default)" + WHITE)
    else:
        print()
    if exclusiveSourceList:
        print(WHITE + "Exclusive sources: " + BLUE + str(exclusiveSourceList))
    if exclusiveFunctionList:
        print(WHITE+"Exclusive functions: " + BLUE + str(exclusiveFunctionList))
    if args.use_all:
        print(DARKCYAN + "Using all sources and functions" + WHITE)
    else:
        print(WHITE+"Ignoring: " + BLUE + str(ignoredList) + WHITE, end="")
        if args.ignore:
            print()        
    if not args.ignore and (not args.use_all):
        print(DARKCYAN + " (Default)" + WHITE)
    bar=""
    for z in range(int(terminalSize)):
        bar+="-"
    print(CYAN + bar + WHITE)
    if not os.path.exists(txtfile):
        with open(txtfile, 'w') as txt: # writes header if not exists
            txt.write(info)
            txt.write("// All generated codes are stored here. You can delete this file if you want.\n")
            txt.write(staticBar + "\n\n")
    elif os.stat(txtfile).st_size == 0:
        with open(txtfile, 'w') as txt: # writes header if content was emptied
            txt.write(info)
            txt.write("// All generated codes are stored here. You can delete this file if you want.\n")
            txt.write(staticBar + "\n\n")
    with open(txtfile, 'a') as txt:
        txt.write("//" + time.strftime('%H:%M:%S%p - %d %b. %Y' + "\n\n"))
        txt.write(hydraCodeNoHeader)
        txt.write("\n\n" + staticBar + "\n\n")
    print(GREEN + hydraCodeNoHeader + WHITE)
    print(CYAN + bar + WHITE)


def main():
    hydra=CodeGenerator.CodeGenerator(minRandomArgument, maxRandomArgument, mathArrowFunctionProb, mouseArrowFunctionProb, modulateItselfProb, ignoredList, exclusiveSourceList, exclusiveFunctionList)
    firstTime=True
    if args.live:
        driver = setWebDriver()
        textarea=""
        action=""
        area=""
    while True:
        hydraCode = hydra.generateCode(minRandomFunctions, maxRandomFunctions)
        printMainInformation(hydra, hydraCode)
        encodedHydraCode = encodeText(hydraCode)
        hydraFinalURL = hydraURL + encodedHydraCode
        print(WHITE+"Press " + GREEN + "Enter " + WHITE + "to generate new code")
        print(WHITE+"Code was saved in '" + GREEN + txtfile + WHITE + "'")
        if not args.live:            
            print(WHITE+"\nOpen the following link to run Hydra with this code:")
            print(BLUE + hydraFinalURL + WHITE +  "\n")
        print("Press " + GREEN + "Ctrl+C " + WHITE + "to exit\n")
        if args.live and firstTime:
            driver.get(hydraFinalURL)
            textarea = driver.find_elements(By.CSS_SELECTOR, '.CodeMirror textarea')[0]
            #area = driver.find_elements(By.ID, 'editor-container')[0]
            area = driver.find_elements(By.CLASS_NAME, 'CodeMirror')[0]
            action = ActionChains(driver)
            area.click(); #Click on browser screen
            if args.hide_code:
                hideCodeKeys(action)
        if args.live and not firstTime:
            try:
                printLiveCodeStatus(0)
                livePrinting(hydraCode, textarea, action, area)
                printLiveCodeStatus(1)                
            except (selenium.common.exceptions.WebDriverException, selenium.common.exceptions.NoSuchWindowException):
                printError("Web browser was closed.")
                exit(1)
        if args.live:       
            printLiveCodeStatus(2)
        if firstTime:
            firstTime = False
        if web:
            webbrowser.open_new(hydraFinalURL)
        input()    

try:
    main()        
except KeyboardInterrupt:
        print(YELLOW + "\nProcess stopped." + WHITE)