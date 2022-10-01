#!/bin/python
import pyfiglet
from datetime import datetime
from os import system, name
import curses

#screen = curses.initscr()
#curses.noecho()
#curses.cbreak()

def timeUpdate():
    now =  datetime.now()
    return now.strftime("%H:%M:%S")

def screenResize(y, x):
    curses.resizeterm(y, x)

def getTarget():
    currentTime = timeUpdate()
    drawTarget = pyfiglet.figlet_format(currentTime)
    splitTarget=drawTarget.splitlines()
    return splitTarget

def getDrawPos(y, x):
    target = getTarget()
    midX = int(x / 2)
    midY = int(y / 2)
    midTarget = int(len(target) / 2)
    midMess = int(len(str(target[midTarget])) / 2)
    xPos = midX - midMess
    return midY, xPos

def cursesInit():
    curses.curs_set(0)
    curses.use_default_colors()

def drawTime(screen):
    cursesInit()
    while True:
        y, x = screen.getmaxyx()
        target = getTarget()
        yPos, xPos = getDrawPos(y, x)
        for num, line in enumerate(target):
            screen.addstr(num + yPos, xPos, line)
        screen.refresh()
        curses.napms(200)
        screen.erase()
        newY, newX = screen.getmaxyx()
        if y != newY or x != newX:
            screenResize(newY, newX)
            screen.clear()

def main(screen):
        drawTime(screen)

curses.wrapper(main)
