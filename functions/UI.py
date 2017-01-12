#!/usr/bin/env python
"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
Usage:
    UI.py create_room <newroom> <room_type>
    UI.py add_person <fname> <lname> <position> 
    UI.py (-i | --interactive)
    UI.py (-h | --help | --version)
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
    
"""

import sys
import cmd
from docopt import docopt, DocoptExit

import amity
amiti = amity.Amity()

def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class MyInteractive (cmd.Cmd):
    intro = 'Welcome to my interactive program!' \
        + ' (type help for a list of commands.)'
    prompt = '(Allocation) '
    file = None

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <newroom> <room_type>"""
        newroom = arg['<newroom>']
        roomtype = arg['<room_type>']

        print(amiti.create_room(newroom, roomtype))

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <fname> <lname> <position>"""
        fname = arg['<fname>']
        lname = arg['<lname>']
        position = arg ['<position>']
        #accommodate = arg ['<wants_accommodation']

        print (amiti.add_person(fname, lname, position))


#     @docopt_cmd
#     def do_serial(self, arg):
#         """Usage: serial <port> [--baud=<n>] [--timeout=<seconds>]
# Options:
#     --baud=<n>  Baudrate [default: 9600]
#         """

#         print(arg)

    # def do_quit(self, arg):
    #     """Quits out of Interactive Mode."""

    #     print('Good Bye!')
    #     exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    MyInteractive().cmdloop()

print(opt)