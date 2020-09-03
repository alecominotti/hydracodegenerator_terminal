#!/usr/bin/python3

# Ale Cominotti - 2020

from resources import CodeGenerator
import time
import random
import os
import argparse
import base64
import re
import webbrowser

# User Variables -----
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
txtfile="hydraCode.txt"
hydraURL="https://hydra.ojack.xyz/?code="
web=False
# End Script Variables -----


def printBanner():
    if(os.name=='nt'):
        os.system("cls")
    else:
        os.system("clear")
    print(YELLOW + """  _   _           _              ____          _         ____                           _             
 | | | |_   _  __| |_ __ __ _   / ___|___   __| | ___   / ___| ___ _ __   ___ _ __ __ _| |_ ___  _ __ 
 | |_| | | | |/ _` | '__/ _` | | |   / _ \ / _` |/ _ \ | |  _ / _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
 |  _  | |_| | (_| | | | (_| | | |__| (_) | (_| |  __/ | |_| |  __/ | | |  __/ | | (_| | || (_) | |   
 |_| |_|\__, |\__,_|_|  \__,_|  \____\___/ \__,_|\___|  \____|\___|_| |_|\___|_|  \__,_|\__\___/|_|   
        |___/
                """ + WHITE)

def showInfo():
    printBanner()
    helptxt=open(resourcesFolder + "help.txt", 'r').read()
    print(helptxt)


#Argument handling -----
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--function", type=int, metavar='<Integer>', help="Constant amount of functions")
parser.add_argument("-fmin", type=int, metavar='<Integer>', help="Minimum amount of functions")
parser.add_argument("-fmax", type=int, metavar='<Integer>', help="Maximum amount of functions")
parser.add_argument("-amin", type=float, metavar='<Float>', help="Minimum value for arguments")
parser.add_argument("-amax", type=float, metavar='<Float>', help="Maximum value for arguments")
parser.add_argument("-web", action='store_true', help="Open hydra in web browser with generated code")
parser.add_argument("-info", "--info", action='store_true', help="Shows information")
parser.add_argument("-i", "--ignore", type=str, help="Specify which sources or functions to ignore.")
parser.add_argument("--use-all", action='store_true', help="Doesn't ignore any source or function.")
parser.add_argument("-xs", type=str, help="Specify exclusive sources to use.")
parser.add_argument("-xf", type=str, help="Specify exclusive functions to use.")
parser.add_argument("-ap", "--arrow-prob", type=int, help="Probability of generating an arrow function as an argument.")
parser.add_argument("-mp", "--mouse-prob", type=int, help="Probability of generating a mouse arrow function as an argument.")
parser.add_argument("-mip", "--modulate-itself-prob", type=int, help='Probability of generating an modulation function with "o0" as an argument.')
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
        print(RED+"ERROR: " + WHITE + "Function max value must be bigger than min value")
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
if args.web:
    web=True
#End argument handling -----
    


def generateCode(hydra, functionsAmount): #This method will be refactored
    fullCode="" # hydra code to generate URL
    staticBar = "----------------------------------------------------------------------------------------------"
    info="// Random Hydra code generated by HCG: https://github.com/alecominotti/hydracodegenerator/\n// @alecominotti\n"
    if args.function:
        print(WHITE+"Functions: " + str(functionsAmount) + " (Constant)")
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
    if not args.arrow_prob:
        print(DARKCYAN + " (Default)" + WHITE)
    else:
        print()
    print(WHITE+"Mouse arrow functions probability: " + str(mouseArrowFunctionProb) +"%", end="")
    if not args.mouse_prob:
        print(DARKCYAN + " (Default)" + WHITE)
    else:
        print()
    print(WHITE+"Modulate itself probability: " + str(modulateItselfProb) +"%", end="")
    if not args.modulate_itself_prob:
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
    terminalSize = os.get_terminal_size().columns
    bar=""
    for z in range(int(terminalSize)):
        bar+="-"
    print(CYAN + bar + WHITE)
    if not os.path.exists(txtfile):
        with open(txtfile, 'w') as txt: # writes if not exists
            txt.write(info)
            txt.write("// All generated codes are stored here. You can delete this file if you want.\n")
            txt.write(staticBar + "\n\n")
    elif os.stat(txtfile).st_size == 0:
        with open(txtfile, 'w') as txt: # writes if content was emptied
            txt.write(info)
            txt.write("// All generated codes are stored here. You can delete this file if you want.\n")
            txt.write(staticBar + "\n\n")
    with open(txtfile, 'a') as txt:
        txt.write("//" + time.strftime('%H:%M:%S%p - %d %b. %Y' + "\n\n"))
        fullCode+="""{info}\n""".format(info=info)
        source = hydra.genSource()
        txt.write(source + "\n")
        fullCode+="""{source}\n""".format(source=source)
        print(GREEN + source)        
        for x in range(functionsAmount):
            func = hydra.genFunction()
            txt.write('  ' + func + "\n")
            fullCode+="""  {func}\n""".format(func=func)
            print("  " + func)
        txt.write(".out(o0)")
        txt.write("\n\n" + staticBar + "\n\n")
        fullCode += ".out(o0)"
        print(".out(o0)")
    print(CYAN + bar + WHITE)     
    #fullCode= fullCode.replace(" ", '%0D')
    #fullCode= fullCode.replace("=", '%3D')
    #fullCode= fullCode.replace("\n", '%0A')
    fullCode= fullCode.replace(">", '%3E') #solves encoding interpretation problems
    fullCode = base64.b64encode(fullCode.encode())
    fullCode= str(fullCode)[2:-1]
    finalURL = hydraURL + str(fullCode)
    return(str(finalURL))


def main():
    hydra=CodeGenerator.CodeGenerator(minRandomArgument, maxRandomArgument, mathArrowFunctionProb, mouseArrowFunctionProb, modulateItselfProb, ignoredList, exclusiveSourceList, exclusiveFunctionList)
    functionsAmount= random.randint(minRandomFunctions,maxRandomFunctions)
    printBanner()
    hydraCodeURL = generateCode(hydra, functionsAmount)
    print(WHITE+"Select code and press " + GREEN + "Ctrl+Shift+C " + WHITE + "to copy it")
    print(WHITE+"Press " + GREEN + "Enter " + WHITE + "to generate new code")
    print(WHITE+"Code was saved in '" + GREEN + "hydraCode.txt" + WHITE + "'")
    print(WHITE+"\nOpen the following link to run Hydra with this code:")
    print(BLUE+hydraCodeURL)
    print(WHITE)
    print("Press " + GREEN + "Ctrl+C " + WHITE + "to exit")
    if web:
        webbrowser.open_new(hydraCodeURL)
    input()
    
   

try:
    while True:    
        main()        
except KeyboardInterrupt:
        print(YELLOW + "\nProcess stopped." + WHITE)