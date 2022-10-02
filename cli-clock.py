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
clock_format = config.get('Format', 'clock_format')
clock_format = clock_format.split(',')
clock_justify = config.get('Format', 'clock_justify')

def timeUpdate():
    time = ''
    now =  datetime.now()
    for item in clock_format:
        time = time + now.strftime(item)
    time = time.replace(r'\n', '\n')
    return time

def screenResize(y, x):
    newY, newX = screen.getmaxyx()
    if y != newY or x != newX:
        curses.resizeterm(y, x)
        screen.clear()

def getTarget():
    currentTime = timeUpdate()
    drawTarget = pyfiglet.figlet_format(currentTime, font = font_style, justify = clock_justify)
    splitTarget = drawTarget.splitlines()
    return splitTarget

def getDrawPos(y, x):
    target = getTarget()
    longest = 0
    midX = int(x / 2)
    midY = int(y / 2) - int(len(target) / 2)
    for num, line in enumerate(target):
        if int(len(target[longest])) < int(len(target[num])):
            longest = num
    middleMessage = int(len(target[num]) / 2)
    if clock_justify == 'center':
        xPos = midX - middleMessage - int(middleMessage / 2.2)
    else:
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

