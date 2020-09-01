#!/usr/bin/python3

# Class that generates sources and functions in Hydra sintax

# Ale Cominotti - 2020

import time
import random
import math
import operator


class CodeGenerator:

    minValue = 0  # min value to set as function argument
    maxValue = 5  # max value to set as function argument
    modulateItselfProb = 20 # probabilities of modulating itself (ex.: modulate(o0,1))
    timeFunctionProb = 5 # probabilities of generating a function of time (ex.: () => Math.sin(time * 0.3))
    mouseFunctionProb = 10 # probabilities of generating a mouse function (ex.: () => mouse.x)
    functions = ["sin", "cos", "tan"]
    mouseList = ["mouse.x", "mouse.y"]
    sourcesList = ["gradient", "noise", "osc", "shape", "solid", "voronoi"]
    colorList = ["brightness", "contrast", "color",
                 "colorama", "invert", "luma", "saturate"]
    geometryList = ["kaleid", "pixelate", "repeat", "repeatX",
                    "repeatY", "rotate", "scale", "scrollX", "scrollY"]
    modulatorsList = ["modulate", "modulateHue", "modulateKaleid", "modulatePixelate",
                      "modulateRepeat", "modulateRepeatX", "modulateRepeatY", "modulateRotate", "modulateScale"]
    operatorsList = ["add", "blend", "diff", "mask", "mult"]
    functionsList = ["genColor", "genGeometry", "genModulator", "genOperator"]

    def truncate(self, number, digits) -> float:
        stepper = 10.0 ** digits
        return math.trunc(stepper * number) / stepper

    def genValue(self):  # generates a number or sin, cos or tan functions
        # probabilities of generating a function of time
        if(random.randint(1, 100) <= self.timeFunctionProb):
            # probabilities of generating a mouse function
            if(random.randint(1, 100) <= self.mouseFunctionProb):
                return("""() => """ + self.mouseList[random.randint(0, len(self.mouseList)-1)])
            else:
                randomTimeMultiplier = self.truncate(random.uniform(0.1, 1), 1)
                return("""() => Math."""+self.functions[random.randint(0, len(self.functions)-1)]+"(time * "+str(randomTimeMultiplier)+")")
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

    # MAIN METHODS ---

    def genSource(self):  # returns a source calling one of them randomly
        return operator.methodcaller(random.choice((self.sourcesList)))(self)

    def genFunction(self):  # returns a source function calling one of them randomly
        return operator.methodcaller(random.choice((self.functionsList)))(self)

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

    def posterize(self):  # not being called
        return(".posterize("+self.genCeroOneValue()+", "+self.genCeroOneValue()+")")

    def saturate(self):
        return(".saturate("+self.genValue()+")")

    def thresh(self): # not being called
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

    def modulateScrollX(self):  # not working properly
        if(random.randint(1, 100) <= self.modulateItselfProb):
            return(".modulateScrollX(o0," + self.genValue()+")")
        else:
            return(".modulateScrollX("+self.genSource()+", "+self.genCeroOneValue()+", "+self.genCeroOneValue()+")")

    def modulateScrollY(self):  # not working properly
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

    def layer(self): # not being called
        return(".layer("+self.genSource()+")")

    def mask(self):
        return(".modulateRotate("+self.genSource()+", "+self.genValue()+", "+self.genCeroOneValue()+")")

    def mult(self):
        return(".mult("+self.genSource()+", "+self.genCeroOneValue()+")")

    # END OPERATORS ---
