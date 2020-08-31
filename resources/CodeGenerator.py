#!/usr/bin/python3

#Class that generates sources and modifiers in Hydra sintax

# Ale Cominotti - 2020

import time
import random
import math
import operator

class CodeGenerator:

    functions = ["sin", "cos", "tan"]
    mouseList = ["mouse.x", "mouse.y"]
    sourcesList=["gradient", "noise", "osc", "shape", "solid", "voronoi"]
    colorList=["brightness", "contrast", "color", "colorama", "invert", "luma", "posterize", "saturate", "thresh"]
    geometryList=["kaleid", "pixelate", "repeat", "repeatX", "repeatY", "rotate", "scale", "scrollX", "scrollY"]
    modulatorsList=["modulate", "modulateHue", "modulateKaleid", "modulatePixelate", "modulateRepeat", "modulateRepeatX", "modulateRepeatY", "modulateRotate", "modulateScale", "modulateScrollX", "modulateScrollY"]
    operatorsList=["add", "blend", "diff", "layer", "mask", "mult"]
    modifiersList=["genColor", "genGeometry", "genModulator", "genOperator"]


    def truncate(self, number, digits) -> float:
        stepper = 10.0 ** digits
        return math.trunc(stepper * number) / stepper

    
    def genValue(self): #generates a number or sin, cos or tan functions
        minValue=0
        maxValue=5
        if(random.randint(1,100)==100): # 1% of posibilities of generating a function
            if(random.randint(1,100)<=10): # 5% of posibilities of generating a mouse function
                return("() => " + self.mouseList[random.randint(0,len(self.mouseList)-1)])    
            else:
                randomTimeMultiplier=self.truncate(random.uniform(0,1), 1)
                return("() => Math."+self.functions[random.randint(0,len(self.functions)-1)]+"(time * "+str(randomTimeMultiplier)+")")
        randomTruncate=random.randint(0,3)
        val = self.truncate(random.uniform(minValue, maxValue), randomTruncate)
        return(str(val))
        
    def genPosOrNegValue(self):
        if(random.randint(1,5)==5):
            return("-" + self.genValue())
        else:
            return(self.genValue())

    def genCeroOneValue(self): #generates a number between 0 and 1
        return str(self.truncate(random.uniform(0,1),1))


    # MAIN METHODS ---

    def genSource(self): #returns a source calling one of them randomly
        return operator.methodcaller(random.choice((self.sourcesList)))(self)

    def genModifier(self): #returns a source modifier calling one of them randomly
        return operator.methodcaller(random.choice((self.modifiersList)))(self)

    # END MAIN METHODS ---


    # MODIFIER METHODS ---

    def genColor(self): #returns a color function calling one of them randomly
        return operator.methodcaller(random.choice((self.colorList)))(self)
    
    def genGeometry(self): #returns a geometry function calling one of them randomly
        return operator.methodcaller(random.choice((self.geometryList)))(self)

    def genModulator(self): #returns a geometry function calling one of them randomly
        return operator.methodcaller(random.choice((self.modulatorsList)))(self)

    def genOperator(self): #returns an operator function calling one of them randomly
        return operator.methodcaller(random.choice((self.operatorsList)))(self)

    # END MODIFIER METHODS ---
    


    # SOURCES ---
    
    def gradient(self):
        return("gradient("+self.genValue()+")")
        
    def noise(self):
        return("noise("+self.genValue()+", "+self.genValue()+")")

    def osc(self):
        return("osc("+self.genValue()+", "+self.genValue()+", "+self.genValue()+")")

    def shape(self):
        return("shape("+self.genValue()+", "+self.genValue()+", "+self.genValue()+")")

    def solid(self):
        return("solid("+self.genValue()+", "+self.genValue()+", "+self.genValue()+", "+self.genCeroOneValue()+")")

    def voronoi(self):
        return("voronoi("+self.genValue()+", "+self.genValue()+", "+self.genCeroOneValue()+")")
    
    # END SOURCES ---


    # COLOR ---

    def brightness(self):
        return(".brightness("+self.genCeroOneValue()+")")
    
    def contrast(self):
        return(".contrast("+self.genValue()+")")

    def color(self):
        return(".color("+self.genValue()+", "+self.genValue()+", "+self.genValue()+")")

    def colorama(self):
        return(".colorama("+self.genValue()+")")

    def invert(self):
        return(".invert("+self.genValue()+")")
    
    def luma(self):
        return(".luma("+self.genCeroOneValue()+")")

    def posterize(self):
        return(".posterize("+self.genValue()+", "+self.genCeroOneValue()+")")
        
    def saturate(self):
        return(".saturate("+self.genValue()+")")

    def thresh(self):
        return(".thresh("+self.genCeroOneValue()+", "+self.genCeroOneValue()+")")
    
    # ENDCOLOR ---


    # GEOMETRY ---

    def kaleid(self):
        return(".kaleid("+self.genValue()+")")
    
    def pixelate(self):
        return(".pixelate("+self.genValue()+", "+self.genValue()+")")

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
        return(".modulate("+self.genSource()+", "+self.genValue()+")")
    
    def modulateHue(self):
        return(".modulateHue("+self.genSource()+", "+self.genValue()+")")

    def modulateKaleid(self):
        return(".modulateKaleid("+self.genSource()+", "+self.genValue()+")")
    
    def modulatePixelate(self):
        return(".modulatePixelate("+self.genSource()+", "+self.genValue()+")")
    
    def modulateRepeat(self):
        return(".modulateRepeat("+self.genSource()+", "+self.genValue()+", "+self.genValue()+", "+self.genValue()+")")

    def modulateRepeatX(self):
        return(".modulateRepeatX("+self.genSource()+", "+self.genValue()+", "+self.genCeroOneValue()+")")

    def modulateRepeatY(self):
        return(".modulateRepeatY("+self.genSource()+", "+self.genValue()+", "+self.genCeroOneValue()+")")

    def modulateRotate(self):
        return(".modulateRotate("+self.genSource()+", "+self.genValue()+", "+self.genCeroOneValue()+")")

    def modulateScale(self):
        return(".modulateScale("+self.genSource()+", "+self.genCeroOneValue()+")")

    def modulateScrollX(self):
        return(".modulateScrollX("+self.genSource()+", "+self.genCeroOneValue()+", "+self.genCeroOneValue()+")")

    def modulateScrollY(self):
        return(".modulateScrollY("+self.genSource()+", "+self.genCeroOneValue()+", "+self.genCeroOneValue()+")")

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
