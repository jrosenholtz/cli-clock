#!/bin/python
import pyfiglet
import configparser
from datetime import datetime
from os import system, name
import curses

config = configparser.ConfigParser()
config.read('cli-clock.ini')
set_border = config.getboolean('Visuals', 'set_border')
smooth_border = config.getboolean('Visuals', 'smooth_border')
font_style = config.get('Visuals', 'font_style')

def timeUpdate():
    now =  datetime.now()
    return now.strftime("%H:%M:%S")

def screenResize(y, x):
    newY, newX = screen.getmaxyx()
    if y != newY or x != newX:
        curses.resizeterm(y, x)
        screen.clear()

def getTarget():
    currentTime = timeUpdate()
    drawTarget = pyfiglet.figlet_format(currentTime, font = font_style)
    splitTarget = drawTarget.splitlines()
    return splitTarget

def getDrawPos(y, x):
    target = getTarget()
    midX = int(x / 2)
    midY = int(y / 2) - int(len(target) / 2)
    midTarget = int(len(target) / 2)
    middleMessage = int(len(target[midTarget]) / 2 )
    xPos = midX - middleMessage 
    return midY, xPos

def cursesInit():
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)

def borders(screen):
    if set_border == True:
        if smooth_border == True:
            screen.border()
        else:
            screen.border('|', '|', '-', '-', '+', '+', '+', '+')


def drawTime(screen):
    cursesInit()
    while True:
        y, x = screen.getmaxyx()
        target = getTarget()
        yPos, xPos = getDrawPos(y, x)
        borders(screen)
        for num, line in enumerate(target):
            screen.addstr(num + yPos, xPos, line, curses.color_pair(0))
        screen.refresh()
        curses.napms(100)
        screen.erase()

def main(screen):
        drawTime(screen)

curses.wrapper(main)

