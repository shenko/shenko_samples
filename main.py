#!/usr/bin/env python3

"""
Just a quick simple menu to help us 
load everything quickly
"""

import os
import sys
from s001_tools import tools_menu

def menu():
    while True:
        print("#---MAIN MENU---#")

        choice = input("""
        1: tools

        0:          (h)elp, gives us more info
        (clear):    Clears the screen / terminal 
        q or quit:  (q)uit exits the program

        Please enter your choice: """)

        if choice == "0" or choice == "h" or choice == "help":
            help()
        elif choice == "1" or choice == "001" or choice == "tools":
            tools_menu.sub_menu()
        elif choice=="q" or choice == "Q" or choice=="quit" or choice == "-":
            #print('initializing exit routine')
            #quit()
            #return 'exit'
            sys.exit()

def help():
    print("************HELP**************")
    print(" visit www.shenko.org for help ")

if __name__ == '__main__':
   print('starting shenko samples...')
   menu()
