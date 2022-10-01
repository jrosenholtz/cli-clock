#!/bin/python
import pyfiglet
from datetime import datetime
from os import system, name
from time import sleep
import curses

#screen = curses.initscr()
#curses.noecho()
#curses.cbreak()

def timeUpdate():
    return datetime.now()

def screenResize(y, x):
    curses.resizeterm(y, x)

def drawTime(screen):
    y, x = screen.getmaxyx()
    currentTime = timeUpdate()
    drawTarget = pyfiglet.figlet_format(str(currentTime))
    midX = int(x / 2)
    midY = int(y / 2)
    midMess = int(len(drawTarget) / 2)
    xPos = midX - midMess
    screen.addstr(midY, 0, drawTarget)
    screen.refresh()
    curses.napms(200)
    screen.refresh()
    newY, newX = screen.getmaxyx()
    if y != newY or x != newX:
        screenResize(newY, newX)
        screen.clear()

def main(screen):
    while True:
        drawTime(screen)

curses.wrapper(main)
