#!/usr/bin/env python
# -*- coding: utf-8 -*-
#title           :menu.py
#description     :This program displays an interactive menu on CLI
#author          :
#date            :
#version         :0.1
#usage           :python menu.py
#notes           :
#python_version  :2.7.6  
#=======================================================================

# Import the modules needed to run the script.
import sys, os
from set_device_configuration import sendConfig
from sqltest import getAverage

# Main definition - constants
menu_actions  = {}  

# =======================
#     MENUS FUNCTIONS
# =======================

# Main menu
def main_menu():
    os.system('clear')
    
    print "Welcome,\n"
    print "Please choose the menu you want to start:"
    print "1. Show Stats"
    print "2. Settings"
    print "\n0. Quit"
    choice = raw_input(" >>  ")
    exec_menu(choice)

    return

# Execute menu
def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print "Invalid selection, please try again.\n"
            menu_actions['main_menu']()
    return

# Menu 1
def showStats():
    print "Show Stats !\n"
    print "3. By Date"
    print "9. Back"
    print "0. Quit"
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return


# Menu 2
def settings():
    print "Settings !\n"
    print "4. Set Sample Interval"
    print "9. Back"
    print "0. Quit" 
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return

def setInterval():
    print "Please enter value in minutes\n"
    choice = raw_input(" >> ")
    sendConfig('{} False'.format(choice))
    choice = '5'
    exec_menu(choice)

def configSent():
    print "Config Sent !\n"
    print "9. Back"
    print "0. Quit"
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return

def enterDate():
    print "Please enter date\n"
    choice = raw_input(" >> ")
    getAverage(choice)
    back()

# Back to main menu
def back():
    menu_actions['main_menu']()

# Exit program
def exit():
    sys.exit()

# =======================
#    MENUS DEFINITIONS
# =======================

# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': showStats,
    '2': settings,
    '3': enterDate,
    '4': setInterval,
    '5': configSent,
    '9': back,
    '0': exit,
}

# =======================
#      MAIN PROGRAM
# =======================

# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_menu()
