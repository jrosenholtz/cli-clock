#!/bin/python
import pyfiglet
from datetime import datetime
from os import system, name
from time import sleep
import curses

screen = curses.initscr()

def timeUpdate():
    return datetime.now()

def drawTime():
    currentTime = timeUpdate()
    drawTarget = pyfiglet.figlet_format(str(currentTime))
    screen.addstr(0, 0, drawTarget)
    curses.napms(100)
    screen.refresh()

while True:
    drawTime()
