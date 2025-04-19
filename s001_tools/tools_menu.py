#!/usr/bin/env python3

"""
tools_menu.py

"""

import os
import sys
import subprocess

from . import tools_help as helper
from . import tools_purge as purge

def sub_menu():
    os.system('clear')
    while True:
        print("************SUB MENU**************")
        choice = input("""
                0: help
                1: purge

                (b)ack   (q)uit
                Please enter your choice: """)

        if choice == "0" or choice == "h" or choice == "help":
            print("visit www.shenko.org to get more information")
        elif choice == "1" or choice == "purge":
            purge.purge()
        elif choice=="b" or choice == "B" or choice=="back":
            # breaks out of sub-menu, goes back to main_menu
            break
        elif choice == "q" or choice == "Q" or choice == "quit":
            sys.exit()

if __name__ == '__main__':
   sub_menu()
