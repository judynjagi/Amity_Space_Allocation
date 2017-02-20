"""WELCOME TO AMITY ROOM ALLOCATION APP
Usage:
  create_room <room_type> <room_name>...
  add_person <fname> <lname> <role> [--wants_accomodation=N] 
  print_allocations [--o=filename]
  print_unallocated [--o=filename]
  print_unallocated_room
  load_people <filename> #The filename only supports .txt extension"
  reallocate_person <person_name> <new_room_name>
  print_room <room_name>
  save_state [--db=sqlite_database]
  load_state <sqlite_database>

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

from docopt import docopt, DocoptExit
from termcolor import cprint, colored
from pyfiglet import figlet_format
import cmd
import sys
import os

from app.classes.amity import Amity

amity = Amity()

def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    
    def fn(self, arg):
        try:
            ARGS = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.
            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            return

        return func(self, ARGS)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class AmityApp(cmd.Cmd):
    cprint(figlet_format('AMITY APP', font='doom'), 'magenta')
    cprint('*' * 60, 'white')
    cprint("    AMITY ROOM ALLOCATION SYSTEM ", 'cyan')
    cprint('*' * 60, 'white')
    cprint(" Below is a list of available commands.", 'cyan')
    cprint('*' * 60, 'white')
    cprint(__doc__, 'cyan')
    cprint('*' * 60, 'white')

    @docopt_cmd
    def do_create_room(self, arg):
        """ Usage: create_room <room_type> <room_name>..."""
        for name in arg['<room_name>']:
            amity.create_room(name, arg['<room_type>'])

    @docopt_cmd
    def do_add_person(self, arg):
        """ Usage: add_person <fname> <lname> <role> [--wants_accomodation=N]

        Options:
        -w, --wants_accomodation=<N>  Wants accomodation [default: N]
        """
        person_name = arg["<fname>"].upper() + " " + arg["<lname>"].upper()
        fname =arg['<fname>'] 
        lname = arg['<lname>']
        role =  arg['<role>']
        accomodate = arg['--wants_accomodation']
        if accomodate is None:
            accomodate = "N"
        else:
            accomodate = accomodate
        
        amity.add_person(person_name, role, accomodate)

    @docopt_cmd
    def do_print_allocations(self, arg):
        """ Usage: print_allocations [--o=filename]"""
        filename = arg['--o']
        if filename:
            amity.print_allocations(filename)
        else:
            amity.print_allocations()

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [--o=filename]"""
        filename = arg['--o']
        if filename:
            amity.print_unallocated(filename)
        else:
            amity.print_unallocated()

    def do_print_unallocated_room(self, arg):
        """Usage: print_unallocated_room"""
        amity.print_unallocated_rooms()

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people <filename>"""
        filename = arg['<filename>']
        amity.load_people(filename)

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """ Usage: reallocate_person <first_name> <last_name> <new_room_name>"""
        fullname = arg['<first_name>'] + ' ' + arg['<last_name>']
        new_room = arg['<new_room_name>']
        amity.reallocate_person(fullname, new_room)

    @docopt_cmd
    def do_print_room(self, arg):
        """ Usage: print_room <room_name> """
        room_name = arg['<room_name>']
        amity.print_room(room_name)

    @docopt_cmd
    def do_save_state(self, arg):
        """ Usage: save_state [--db=sqlite_database]"""
        db = arg['--db']
        if db:
            amity.save_state(db)
        else:
            amity.save_state()

    @docopt_cmd
    def do_load_state(self,arg):
        """ Usage: load_state <sqlite_database>"""
        database = arg['<sqlite_database>']
        amity.load_state(database)

    @docopt_cmd
    def do_exit(self, arg):
        """ Usage: exit"""
        cprint('GOODBYE!', 'magenta')
        exit()


if __name__ == '__main__':

    AmityApp().cmdloop()