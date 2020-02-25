import sys, random, argparse
import numpy as np
import math
import turtle
import random
from PIL import Image
from datetime import datetime
from fractions import gcd
#simulates drawing of spirals using turtle api, TURTLE is NOT EFFECIENT
class graph_simulation:
    # constructor
    def __init__(self, xc, yc, col, R, r, l):
        # create own turtle
        self.t = turtle.Turtle()
        # set step in degrees, later used in drawing
        self.step = 5
        # set drawing complete flag
        self.drawingComplete = False
        # set parameters
        self.setparams(xc, yc, col, R, r, l)
        # initiatize drawing
        self.restart()

    # set parameters
    def setparams(self, xc, yc, col, R, r, l):
        # parameters of spiral and graph
        self.xc = xc
        self.yc = yc
        self.R = int(R)
        self.r = int(r)
        self.l = l
        self.col = col
        # we want the smallest value, use gcd
        gcdVal = gcd(self.r, self.R)
        self.nRot = self.r//gcdVal
        # k-> ratio of radius compared to full circle
        self.k = r/float(R)
        # set color using color pointers
        self.t.color(*col)
        # current angle
        self.a = 0

    # restart drawing, clears current state
    def restart(self):
        # set flag
        self.drawingComplete = False
        # show turtle
        self.t.showturtle()
        # go to first point
        self.t.up()
        R, k, l = self.R, self.k, self.l
        a = 0.0
        x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
        self.t.setpos(self.xc + x, self.yc + y)
        self.t.down()
    def draw(self):
        # use given parameters to visualize points and drawing
        R = self.R
        k = self.k
        l = self.l
        for i in range(0, 360*self.nRot + 1, self.step):
            a = math.radians(i)
            x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
            y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
            self.t.setpos(self.xc + x, self.yc + y)
        # done - hide turtle
        self.t.hideturtle()

    # update by one step
    def update(self):
        # skip if done
        if self.drawingComplete:
            return
        # increment angle
        self.a += self.step
        # draw step
        R, k, l = self.R, self.k, self.l
        # set angle
        a = math.radians(self.a)
        x = self.R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = self.R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
        self.t.setpos(self.xc + x, self.yc + y)
        # check if drawing is complete and set flag
        if self.a >= 360*self.nRot:
            self.drawingComplete = True
            # done - hide turtle
            self.t.hideturtle()

    # clear everything
    def clear(self):
        self.t.clear()

# A class for animating spirographs
class SpiroAnimator:
    # constructor
    def __init__(self, N):
        # timer value in milliseconds
        self.deltaT = 10
        # get window dimensions
        self.width = turtle.window_width()
        self.height = turtle.window_height()
        self.spiros = []
        for i in range(N):
            # generate random parameters
            rparams = self.genRandomParams()
            # set spiro params
            spiro = graph_simulation(*rparams)
            self.spiros.append(spiro)
        # call timer
        turtle.ontimer(self.update, self.deltaT)

    # restart sprio drawing
    def restart(self):
        for spiro in self.spiros:
            # clear
            spiro.clear()
            # generate random parameters
            rparams = self.genRandomParams()
            # set spiro params
            spiro.setparams(*rparams)
            # restart drawing
            spiro.restart()

    # generate random parameters
    def genRandomParams(self):
        width, height = self.width, self.height
        R = random.randint(50, min(width, height)//2)
        r = random.randint(10, 9*R//10)
        l = random.uniform(0.1, 0.9)
        xc = random.randint(-width//2, width//2)
        yc = random.randint(-height//2, height//2)
        col = (random.random(),
               random.random(),
               random.random())
        return (xc, yc, col, R, r, l)

    def update(self):
        # update all spiros
        nComplete = 0
        for spiro in self.spiros:
            # update
            spiro.update()
            # count completed ones
            if spiro.drawingComplete:
                nComplete+= 1
        # if all spiros are complete, restart
        if nComplete == len(self.spiros):
            self.restart()
        # call timer
        turtle.ontimer(self.update, self.deltaT)


def main():
    print('generating spirograph, locate external window...')
    # create parser
    parser = argparse.ArgumentParser()
    #python spirograph.py --sparams R r l / --help
    parser.add_argument('--sparams', nargs=3, dest='sparams', required=False,
        help="The three arguments in sparams: R, r, l.")
    # parse args
    args = parser.parse_args()

    #enable coverage of half the screen
    turtle.setup(width=0.5)

    # checks args and draw
    if args.sparams:
        params = [float(x) for x in args.sparams]
        # draw spirograph with given parameters
        # black by default
        col = (0.0, 0.0, 0.0)
        spiro = Spiro(0, 0, col, *params)
        spiro.draw()
    else:
        # create animator object
        spiroAnim = SpiroAnimator(4)
        # add key handler to toggle turtle cursor
        #turtle.onkey(spiroAnim.toggleTurtles, "t")
        # add key handler to restart animation
        turtle.onkey(spiroAnim.restart, "space")

    turtle.mainloop() #begin looping of graph

# call main
if __name__ == '__main__':
    main()
