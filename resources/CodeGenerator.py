#!/usr/bin/python3

# Class that generates sources and functions in Hydra sintax

# Ale Cominotti - 2020

import time
import random
import math
import operator

RED = '\033[91m'
WHITE = '\033[0m'   


class CodeGenerator:

    minValue = 0  # lower bound value to set as function argument
    maxValue = 5  # upper bound value to set as function argument
    modulateItselfProb = 20 # Probabilities of modulating with itself (ex.: modulate(o0,1))
    timeFunctionProb = 5 # Probabilities of generating a function that changes over time (ex.: () => Math.sin(time * 0.3))
    mouseFunctionProb = 10 # Probabilities of generating a mouse function that changes over time (ex.: () => mouse.x)

    mathFunctions = ["sin", "cos", "tan"]
    mouseList = ["mouse.x", "mouse.y"]
    sourcesList = ["gradient", "noise", "osc", "shape", "solid", "voronoi"]
    colorList = ["brightness", "contrast", "color", "colorama", "invert", "luma", "saturate"]
    geometryList = ["kaleid", "pixelate", "repeat", "repeatX", "repeatY", "rotate", "scale", "scrollX", "scrollY"]
    modulatorsList = ["modulate", "modulateHue", "modulateKaleid", "modulatePixelate", "modulateRepeat", "modulateRepeatX", "modulateRepeatY", "modulateRotate", "modulateScale"]
    operatorsList = ["add", "blend", "diff", "mask", "mult"]
    functionsList = ["genColor", "genGeometry", "genModulator", "genOperator"]
    ignoredList = []
    exclusiveSourceList = []
    exclusiveFunctionList = []


    def __init__(self, min=None, max=None, ignoredList=None, exclusiveSourceList=None, exclusiveFunctionList=None):
        if not (min is None):
            self.minValue = min
        if not (max is None):
            self.maxValue = max
        if not (ignoredList is None) and (len(ignoredList)>0):
            self.ignoredList = ignoredList
        if not (exclusiveSourceList is None) and (len(exclusiveSourceList)>0):
            if(self.checkSources(exclusiveSourceList)):
                self.exclusiveSourceList = exclusiveSourceList
            else:
                self.printError("One or more of the specified exclusive sources don't exist")
                exit(1)
        if not (exclusiveFunctionList is None) and (len(exclusiveFunctionList)>0):
            if(self.checkFunctions(exclusiveFunctionList)):
                self.exclusiveFunctionList = exclusiveFunctionList
            else:
                self.printError("One or more of the specified exclusive functions don't exist")
                exit(1)
        if(len(ignoredList)>0 and (len(exclusiveSourceList)>0 or len(exclusiveFunctionList)>0)):
            exclusiveSourceAndFunction= self.exclusiveSourceList+self.exclusiveFunctionList
            if( len([i for i in exclusiveSourceAndFunction if i in self.ignoredList]) > 0):
                self.printError("You can't ignore sources or functions specified as exclusive")
                exit(1)
            


    def truncate(self, number, digits) -> float:
        stepper = 10.0 ** digits
        return math.trunc(stepper * number) / stepper

    def isIgnored(self, chosen):
        return(chosen.lower() in [x.lower() for x in self.ignoredList])     
    
    def isExclusiveSource(self, chosen):
        if(len(self.exclusiveSourceList)==0):
            return True
        else:
            return(chosen.lower() in [x.lower() for x in self.exclusiveSourceList])     
    
    def isExclusiveFunction(self, chosen):
        if(len(self.exclusiveFunctionList)==0):
            return True
        else:
            return(chosen.lower() in [x.lower() for x in self.exclusiveFunctionList])   

    def checkSources(self, inputSourcesList):
        return set(inputSourcesList).issubset(self.sourcesList)
    
    def checkFunctions(self, inputFunctionsList):
        allFunctions= self.colorList+self.geometryList+self.modulatorsList+self.operatorsList
        return set(inputFunctionsList).issubset(allFunctions)

    def printError(self, message):
        print(RED + "\nERROR: " + WHITE + message)



    # VALUE GENERATION METHODS ---

    def genValue(self):  # generates a number, mouse, or math functions
        # probabilities of generating a function of time
        if(random.randint(1, 100) <= self.timeFunctionProb):
            # probabilities of generating a mouse function
            if(random.randint(1, 100) <= self.mouseFunctionProb):
                return("""() => """ + self.mouseList[random.randint(0, len(self.mouseList)-1)])
            else:
                randomTimeMultiplier = self.truncate(random.uniform(0.1, 1), 1)
                return("""() => Math."""+self.mathFunctions[random.randint(0, len(self.mathFunctions)-1)]+"(time * "+str(randomTimeMultiplier)+")")
        randomTruncate = random.randint(0, 3)
        val = self.truncate(random.uniform(
            self.minValue, self.maxValue), randomTruncate)
        return(str(val))

    def genPosOrNegValue(self):
        if(random.randint(1, 5) == 5):
            return("-" + self.genValue())
        else:
            return(self.genValue())

    def genCeroOneValue(self):  # generates a number between 0 and 1
        return str(self.truncate(random.uniform(0, 1), 1))

    def genCeroPointFiveValue(self):  # generates a number between 0 and 0.5
        return str(self.truncate(random.uniform(0, 0.5), 2))
    
    def genCeroPointOneToMax(self):  # generates a number between 0.1 and maxValue
        return str(self.truncate(random.uniform(0.1, self.maxValue), 2))

    # END VALUE GENERATION METHODS ---


    # MAIN METHODS ---

    def genSource(self):  # returns a source calling one of them randomly
        fullSource = operator.methodcaller(random.choice((self.sourcesList)))(self)
        source=fullSource.split("(")[0] # just source name
        start = time.time() # avoids failing when everything is ignored
        while((not self.isExclusiveSource(source)) or self.isIgnored(source) and (time.time() < (start + 10))):
            fullSource = operator.methodcaller(random.choice((self.sourcesList)))(self)
            source=fullSource.split("(")[0]
        if(time.time() >= (start + 15)):
            self.printError("Could't generate a Source (You ignored all of them")
            exit(1)
        else:
            return fullSource

    def genFunction(self):  # returns a source function calling one of them randomly
        fullFunction = operator.methodcaller(random.choice((self.functionsList)))(self)
        function = fullFunction[1:].split("(")[0] # just its name
        start = time.time() # avoids failing when everything is ignored
        while((not self.isExclusiveFunction(function)) or (self.isIgnored(function)) and (time.time() < (start + 10)) ):
            fullFunction = operator.methodcaller(random.choice((self.functionsList)))(self)
            function = fullFunction[1:].split("(")[0]
        if(time.time() >= (start + 15)):
            print(RED + "\nERROR:" + WHITE + " Could't generate a Function (You ignored all of them)")
            exit(1)
        else:
            return fullFunction

    # END MAIN METHODS ---


    # FUNCTION METHODS ---

    def genColor(self):  # returns a color function calling one of them randomly
        return operator.methodcaller(random.choice((self.colorList)))(self)

    def genGeometry(self):  # returns a geometry function calling one of them randomly
        return operator.methodcaller(random.choice((self.geometryList)))(self)

    def genModulator(self):  # returns a geometry function calling one of them randomly
        return operator.methodcaller(random.choice((self.modulatorsList)))(self)

    def genOperator(self):  # returns an operator function calling one of them randomly
        return operator.methodcaller(random.choice((self.operatorsList)))(self)

    # END FUNCTION METHODS ---


    # SOURCES ---

    def gradient(self):
        return("gradient("+self.genValue()+")")

    def noise(self):
        return("noise("+self.genValue()+", "+self.genValue()+")")

    def osc(self):
        return("osc("+self.genValue()+", "+self.genValue()+", "+self.genValue()+")")

    def shape(self):
        return("shape("+self.genValue()+", "+self.genCeroPointFiveValue()+", "+self.genValue()+")")

    def solid(self):
        return("solid("+self.genCeroOneValue()+", "+self.genCeroOneValue()+", "+self.genCeroOneValue()+", "+self.genCeroOneValue()+")")

    def voronoi(self):
        return("voronoi("+self.genValue()+", "+self.genValue()+", "+self.genCeroOneValue()+")")

    # END SOURCES ---


    # COLOR ---

    def brightness(self):
        return(".brightness("+self.genCeroOneValue()+")")

    def contrast(self):
        return(".contrast("+self.genValue()+")")

    def color(self):
        return(".color("+self.genCeroOneValue()+", "+self.genCeroOneValue()+", "+self.genCeroOneValue()+")")

    def colorama(self):
        return(".colorama("+self.genValue()+")")

    def invert(self):
        return(".invert("+self.genCeroOneValue()+")")

    def luma(self):
        return(".luma("+self.genCeroOneValue()+")")

    def posterize(self):
        return(".posterize("+self.genCeroOneValue()+", "+self.genCeroOneValue()+")")

    def saturate(self):
        return(".saturate("+self.genValue()+")")

    def thresh(self):
        return(".thresh("+self.genCeroOneValue()+", "+self.genCeroOneValue()+")")

    # ENDCOLOR ---


    # GEOMETRY ---

    def kaleid(self):
        return(".kaleid("+self.genValue()+")")

    def pixelate(self):
        return(".pixelate("+self.genCeroPointOneToMax()+", "+self.genCeroPointOneToMax()+")")

    def repeat(self):
        return(".repeat("+self.genValue()+", "+self.genValue()+", "+self.genValue()+", "+self.genValue()+")")

    def repeatX(self):
        return(".repeatX("+self.genValue()+", "+self.genValue()+")")

    def repeatY(self):
        return(".repeatY("+self.genValue()+", "+self.genValue()+")")

    def rotate(self):
        return(".rotate("+self.genValue()+", "+self.genValue()+")")

    def scale(self):
        return(".color("+self.genPosOrNegValue()+", "+self.genCeroOneValue()+", "+self.genCeroOneValue()+")")

    def scrollX(self):
        return(".scrollX("+self.genValue()+", "+self.genValue()+")")

    def scrollY(self):
        return(".scrollY("+self.genValue()+", "+self.genValue()+")")

    # ENDGEOMETRY ---


    # MODULATORS ---

    def modulate(self):
        if(random.randint(1, 100) <= self.modulateItselfProb):
            return(".modulate(o0," + self.genValue()+")")
        else:
            return(".modulate("+self.genSource()+", "+self.genValue()+")")

    def modulateHue(self):
        if(random.randint(1, 100) <= self.modulateItselfProb):
            return(".modulateHue(o0," + self.genValue()+")")
        else:
            return(".modulateHue("+self.genSource()+", "+self.genValue()+")")

    def modulateKaleid(self):
        if(random.randint(1, 100) <= self.modulateItselfProb):
            return(".modulateKaleid(o0," + self.genValue()+")")
        else:
            return(".modulateKaleid("+self.genSource()+", "+self.genValue()+")")

    def modulatePixelate(self):
        if(random.randint(1, 100) <= self.modulateItselfProb):
            return(".modulatePixelate(o0," + self.genValue()+")")
        else:
            return(".modulatePixelate("+self.genSource()+", "+self.genValue()+")")

    def modulateRepeat(self):
        if(random.randint(1, 100) <= self.modulateItselfProb):
            return(".modulateRepeat(o0, "+self.genValue()+", "+self.genValue()+", "+self.genValue()+")")
        else:
            return(".modulateRepeat("+self.genSource()+", "+self.genValue()+", "+self.genValue()+", "+self.genValue()+")")

    def modulateRepeatX(self):
        if(random.randint(1, 100) <= self.modulateItselfProb):
            return(".modulateRepeatX(o0, "+self.genValue()+", "+self.genValue()+", "+self.genValue()+")")
        else:
            return(".modulateRepeatX("+self.genSource()+", "+self.genValue()+", "+self.genCeroOneValue()+")")

    def modulateRepeatY(self):
        if(random.randint(1, 100) <= self.modulateItselfProb):
            return(".modulateRepeatY(o0, "+self.genValue()+", "+self.genValue()+", "+self.genValue()+")")
        else:
            return(".modulateRepeatY("+self.genSource()+", "+self.genValue()+", "+self.genCeroOneValue()+")")

    def modulateRotate(self):
        if(random.randint(1, 100) <= self.modulateItselfProb):
            return(".modulateRotate(o0, "+self.genValue()+", "+self.genValue()+", "+self.genValue()+")")
        else:
            return(".modulateRotate("+self.genSource()+", "+self.genValue()+", "+self.genCeroOneValue()+")")

    def modulateScale(self):
        if(random.randint(1, 100) <= self.modulateItselfProb):
            return(".modulateScale(o0," + self.genValue()+")")
        else:
            return(".modulateScale("+self.genSource()+", "+self.genCeroOneValue()+")")

    def modulateScrollX(self):
        if(random.randint(1, 100) <= self.modulateItselfProb):
            return(".modulateScrollX(o0," + self.genValue()+")")
        else:
            return(".modulateScrollX("+self.genSource()+", "+self.genCeroOneValue()+", "+self.genCeroOneValue()+")")

    def modulateScrollY(self):
        if(random.randint(1, 100) <= self.modulateItselfProb):
            return(".modulateScrollY(o0," + self.genValue()+")")
        else:
            return(".modulateScrollX("+self.genSource()+", "+self.genCeroOneValue()+", "+self.genCeroOneValue()+")")

    # END MODULATORS ---


    # OPERATORS ---

    def add(self):
        return(".add("+self.genSource()+", "+self.genCeroOneValue()+")")

    def blend(self):
        return(".blend("+self.genSource()+", "+self.genCeroOneValue()+")")

    def diff(self):
        return(".diff("+self.genSource()+")")

    def layer(self):
        return(".layer("+self.genSource()+")")

    def mask(self):
        return(".modulateRotate("+self.genSource()+", "+self.genValue()+", "+self.genCeroOneValue()+")")

    def mult(self):
        return(".mult("+self.genSource()+", "+self.genCeroOneValue()+")")

    # END OPERATORS ---
