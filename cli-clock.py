#!/bin/python
import pyfiglet
import configparser
from datetime import datetime
import curses

# Get variables from configuration file
config = configparser.ConfigParser()
config.read("cli-clock.ini")

try:
    set_border = config.getboolean('Visuals', 'set_border')
    smooth_border = config.getboolean('Visuals', 'smooth_border')
    font_style = config.get('Visuals', 'font_style')
    clock_format = config.get('Format', 'clock_format')
    clock_format = clock_format.split(',')
    clock_justify = config.get('Format', 'clock_justify')
    font_color = config.getint('Visuals', 'font_color')
    border_color = config.getint('Visuals', 'border_color')

except:
    print("Uh oh, something went wrong with reading your config file! Make sure cli-clock.ini exists, and that there are no typos in the config.")
    exit()

# Get current time, turn it into a format to be sent to pyfiglet
def timeUpdate():
    time = ''
    now =  datetime.now()
    for item in clock_format:
        time = time + now.strftime(item)
    time = time.replace(r'\n', '\n')
    return time

# Resize screen if necessary
def screenResize(y, x):
    newY, newX = screen.getmaxyx()
    if y != newY or x != newX:
        curses.resizeterm(y, x)
        screen.erase()

# Send clock data to pyfiglet
def getTarget():
    currentTime = timeUpdate()
    drawTarget = pyfiglet.figlet_format(currentTime, font = font_style, justify = clock_justify)
    splitTarget = drawTarget.splitlines()
    return splitTarget

# Center text
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

# Init Curses values and colors from cli defaults
def cursesInit(screen):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    screen.nodelay(True)
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)

# Check if borders should be displayed
def borders(screen):
    global set_border
    screen.bkgdset(curses.color_pair(border_color))
    if set_border == True:
        if smooth_border == True:
            screen.border()
        else:
            screen.border('|', '|', '-', '-', '+', '+', '+', '+')

def readInput(screen):
    if screen.getch() == ord('q'):
        return False

# Main draw loop
def drawTime(screen):
    cursesInit(screen)
    try:
        while True:
            y, x = screen.getmaxyx()
            target = getTarget()
            yPos, xPos = getDrawPos(y, x)
            borders(screen)
            try:
                for num, line in enumerate(target):
                    screen.addstr(num + yPos, xPos, line, curses.color_pair(font_color))
            except:
                curses.endwin()
                print('Screen too small! try a larger window, smaller font, or smaller clock format')
                break
            screen.refresh()
            if readInput(screen) == False:
                break
            curses.napms(100)
            if readInput(screen) == False:
                break
            screen.erase()
    ## Handle ctrl+c gracefully 
    except KeyboardInterrupt:
        curses.endwin()
        print('Exited Program')
        pass

# wrapper func
def main(screen):
        drawTime(screen)

curses.wrapper(main)

