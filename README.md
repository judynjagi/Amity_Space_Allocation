# AMITY ROOM ALLOCATION SYSTEM.
#1. `ABOUT AMITY ROOM ALLOCATION SYSTEM`
The objective of this project is to build a room allocation application for a facility in Andela called Amity.

Amity has rooms which can be offices or living spaces. An office can occupy a maximum of 6 people. A living space can inhabit a maximum of 4 people.

A person to be allocated could be a fellow or staff. Staff cannot be allocated living spaces. Fellows have a choice to choose a living space or not.

This system will be used to automatically allocate spaces to people at random.


#2.`COMMANDS AVAILABLE`

Fellows and staff at Andela's Amity facility are the immediate consumers of the system.

Command | Argument |
--- | --- | ---
create_room | livingspace or office
add_person | (fname) (lname) (role) [--wants_accomodate=N]
reallocate_person | (person_name) (new_room_name)
load_people | (filename)
print_allocations| [--o=filename]
print_unallocated| [--o=filename]
print_room | (room_name)
print_unallocated_room|
save_state | [--db=sqlite_database]
load_state |(sqlite_database)
#3. `Installation.`

1. Clone this repository to your local machine using 
`git clone https://github.com/judynjagi/Amity_Space_Allocation.git`

2. Create a **virtualenv** on your machine and activate it
3. Install the dependencies via `pip install -r requirements.txt`

4. cd into the **amity_app** folder and run `python user_interface.py`

#4. `Usage`
The following video will guide you on how to run different commands. 
[![asciicast](https://asciinema.org/a/6rd047s2g3k6y15ms98xok3vp.png)](https://asciinema.org/a/6rd047s2g3k6y15ms98xok3vp)

#5. `Tests.`
Ensure that you are within your environment and run the following command
`nosetests --rednose --with-coverage --cover-package=app

