import random
import sys, os


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text, select
from termcolor import cprint, colored

from .people import People, Fellow, Staff
from .rooms import Room, LivingSpace, Office
from .models import OfficeModel, PeopleModel, LivingSpaceModel, create_db, Base

class Amity(object):
	""" Main Class for the Amity Program"""
	def __init__(self):
		self.rooms = []
		self.people = []
		self.allocated_rooms = []
		self.unallocatedpeople = {'offices':[], 'lspaces':[]}

	def create_room(self, room_name, room_type):
		"""fuction that creates a unique room"""

		# Check that a room can only be an office or livingspace
		if room_type.upper() not in ['OFFICE', 'LIVINGSPACE']:
			cprint("Room type can either  be an office or livingspace", 'green')
			return "The room type does not exist"

		# Check if room name exists
		for room in self.rooms:
			if room_name.upper() == room.name:
				cprint(room.name + " " + "is already in the system", 'green')
				return "Name exists"

		# Add an office
		if room_type.upper() == 'OFFICE':
			room = Office(room_name)
			self.rooms.append(room)
			cprint(room.name + " " + "office has been created successfully", 'green')
			return "office successfully created"

		# Add a livingspace
		elif room_type.upper() == 'LIVINGSPACE':
			room = LivingSpace(room_name)
			self.rooms.append(room)
			cprint(room.name + " " + "livingspace has been created successfully", 'green')
			return "Livingspace successfully created"	

	def check_vacant_rooms(self):
		""" Function that checks if the rooms are vacant"""

		vacantrooms = {'offices':[], 'lspace':[]}
		for room in self.rooms:
			if not room.is_full():
				if isinstance(room, Office):
					vacantrooms['offices'].append(room)
				elif isinstance(room, LivingSpace):
					vacantrooms['lspace'].append(room)

		return vacantrooms

	def add_person(self, fullname, position, wants_accomodation="N"):

		""" Function to add a person"""
		# Ensure that a person is either a staff or a fellow
		if type(fullname) != str:
			cprint("Incorrect name type format.", 'red')
			return 'Wrong type for name.'

		if position.upper() not in ['STAFF', 'FELLOW']:
			cprint("Position can either be Fellow or Staff", 'green')
			return "Position can either be Fellow or Staff"

		# Check if the person's name exists
		for person in self.people:
			if fullname.upper() == person.name.upper():
				cprint(person.name + " " + "is already in the system", 'green')
				return "Name exists"

		# Create a staff and automatically allocate them to an office
		if position.upper() == "STAFF":
			if wants_accomodation.upper() == "Y":
				cprint("staff cannot be created when the value of accomodation set to is 'Y'. Instead, change it to 'N'.", 'green')
				return "staff cannot be created"

			elif wants_accomodation.upper() == "N":
				staff = Staff(fullname)
				self.people.append(staff)
				cprint(staff.name + ' ' + "staff has been created successfully", 'green') 

				self.allocate_office(fullname, wants_accomodation)
				staff.allocated.append(self.search_roomoccupants(fullname))
				
			else:
				cprint("Wants_accommodation only takes 'N' or 'Y' values", 'green')
				return "Wants_accommodation only takes 'N' or 'Y' values"

	
		# Create a fellow and automatically allocate them to an office and livingspace
		elif position.upper() == "FELLOW":
			if wants_accomodation.upper() == "N":
				fellow = Fellow(fullname, wants_accomodation)
				self.people.append(fellow)
				cprint(fellow.name + ' ' + " fellow has been created successfully", 'green')

				self.allocate_office(fullname, wants_accomodation)
				fellow.allocated.append(self.search_roomoccupants(fullname))

			elif wants_accomodation.upper()== "Y":
				fellow = Fellow(fullname, wants_accomodation)
				self.people.append(fellow)
				cprint(fellow.name + ' ' + " fellow has been created successfully", 'green')

				self.allocate_office(fullname, wants_accomodation)
				self.allocate_livingspace(fullname, wants_accomodation)
				fellow.allocated.append(self.search_roomoccupants(fullname))

			else:
				cprint("Wants_accommodation only takes 'N' or 'Y' values", 'cyan', attrs=['bold'])
				return "Wants_accommodation only takes 'N' or 'Y' values"


	def load_people(self, filename):
		""" Function to add people into the system from a text file"""

		# Open the file and read all the lines
		try:
			if not os.path.isfile(filename):
				cprint("Please enter a invalid file path.", 'green', attrs=['bold'])
				return "Invalid path."

			with open(filename, 'r') as f:
				people = f.readlines()

			# Place the data in each line in a list and use indexing to get the name, role etc
			for employee in people:
				employee_information = employee.split()
				employee_fullname = employee_information[0] + ' ' + employee_information[1]
				role = employee_information[2]

			# Check the role of each employee and if they want accomodation
				if role == 'STAFF':
					wants_accomodation = 'N'
				elif role == 'FELLOW':
					if len(employee_information)<=3:
						wants_accomodation = 'N'
					elif len(employee_information)>3:
						accomodation = employee_information[3]
						if accomodation == 'N':
							wants_accomodation = 'N'
						else:
							wants_accomodation = 'Y'

				self.add_person(employee_fullname, role, wants_accomodation)


		except IndexError:
			cprint("End of file!.", 'green', attrs=['bold'])
			return " Empty file!."


	def allocate_office(self, person_name, wants_accomodation="N"):
		"""Function to allocate a fellow or staff to an office"""

		# Check whether the person exists

		if person_name.upper() not in [person.name.upper() for person in self.people]:

			cprint("The name does not exist, please enter a valid name", 'green', attrs=['bold'])
			return "The name does not exist, please enter a valid name"

		# Search for the person and allocate them an office
		for person in self.people:
			if person.name.upper() == person_name.upper():
				try:
					vacantrooms = self.check_vacant_rooms()
					random_office = random.choice(vacantrooms['offices'])
					random_office.occupants.append(person)
					self.allocated_rooms.append(random_office)
					cprint(person.name + ' ' + "has been allocated to" + ' ' +  random_office.name, 'green')

				except (IndexError, TypeError):
					self.unallocatedpeople['offices'].append(person)

	def allocate_livingspace(self, person_name, wants_accomodation="N"):
		""" Function to allocate a fellow to a livingspace"""

		# Check whether person exists

		if person_name.upper() not in [person.name.upper() for person in self.people]:

			cprint("The name does not exist, please enter a valid name", 'cyan', attrs=['bold'])
			return "The name does not exist, please enter a valid name"

		# Search for a fellow 
		for  person in self.people:
			if person.name.upper() == person_name.upper():
				break

		# Ensure that a staff cannot be allocated a livingspace

		if isinstance(person, Staff) and wants_accomodation == "Y":

			cprint("staff cannot be allocated a livingspace", 'green', attrs=['bold'])
			return "staff cannot be allocated a livingspace"

		# Allocate  a fellow for an vacant office
		if isinstance(person, Fellow):
			if wants_accomodation == "Y":
				try:
					vacantrooms = self.check_vacant_rooms()
					random_lspace = random.choice(vacantrooms['lspace'])
					random_lspace.occupants.append(person)
					self.allocated_rooms.append(random_lspace)
					cprint(person.name + ' ' + "has been allocated to" + ' ' + random_lspace.name, 'green')

				except (IndexError, TypeError):
					self.unallocatedpeople['lspaces'].append(person)


	def print_allocations(self, filename="None"):
		""" A function that prints rooms and its occupants"""

		# Write allocated rooms and its occupants into a file
		if not self.allocated_rooms:
			cprint("No allocations done yet", 'green', attrs=['bold'])

		else:
			if filename != "None":
				file = open(filename, 'w')
				record = set()			
				for room in self.allocated_rooms:
					if room.name not in record:
						record.add(room)
				for sortedrooms in record:
					file.write('\n' + "%s\n" % sortedrooms.name + '-'*50 + '\n')
					for occupant in sortedrooms.occupants:
						if len(sortedrooms.occupants)>0:

							file.write('\n'+ "%s\n" % occupant.name )
							cprint("Writing data into" + ' ' + filename +' '+ "text file", 'cyan', attrs=['bold'])


			# Sort the rooms to remove duplicated rooms and print out on the screen
			else:
				record = set()			
				for room in self.allocated_rooms:
					if room.name not in record:
						record.add(room)
				for sortedrooms in record:
					cprint ('\n' + sortedrooms.name + ': ' + sortedrooms.room_type, 'cyan', attrs=['bold'] )
					cprint ('-' * 50, 'red')
					if sortedrooms.occupants:
						for occupant in sortedrooms.occupants:
							cprint (''.join(occupant.name) + ' ', 'green')

				

	def print_unallocated (self, filename="None"):
		"""A function that prints people who haven't been allocated yet"""

		if not self.unallocatedpeople:

			cprint("No one is unallocated yet", 'green')


		else:
			# Write unallocated people into a file
			if filename != "None":
				file = open(filename, 'w')

				for people in self.unallocatedpeople['offices']+ self.unallocatedpeople['lspaces']:

					file.write("%s\n" % people.name + ': ' + people.role)

			# Print unallocated people on the screen
			else:
				cprint("UNALLOCATED PEOPLE TO OFFICES", 'cyan', attrs=['bold'] )
				cprint ('*' * 50, 'red')
				for people in self.unallocatedpeople['offices']:
						cprint (''.join(people.name) + ' ', 'green')

				cprint("UNALLOCATED PEOPLE TO LIVINGSPACES", 'cyan', attrs=['bold'] )
				cprint ('*' * 50, 'red')
				for people in self.unallocatedpeople['lspaces']:
						cprint (''.join(people.name) + ' ', 'green')

	def print_unallocated_rooms (self):
		"""A function that prints out unallocated rooms"""
		for room in self.rooms:
			if room not in self.allocated_rooms:

				cprint(''.join(room.name) + ' ', 'green', attrs=['bold'])


	def print_room(self, roomname):
		"""A function that prints the occupants in the specified room"""
		if not self.rooms:
			cprint ('Room' + ' ' + roomname + ' ' + "doesn't exist", 'green', attrs=['bold'])
		for room in self.rooms:
			if roomname.upper() == room.name:
				cprint ('\n' + room.name + ':' + ' ' + room.room_type, 'cyan', attrs=['bold'] )
				cprint ('*' * 50, 'red')
				if room.occupants:
					for person in room.occupants:
						cprint (''.join(person.name) + ' ', 'green')
				else:

					cprint("No occupants", 'green', attrs=['bold'])	

					
	def search_person(self, pname):		
		"""A function that checks if the person to be reallocated exists"""
		for p in self.people:
			if pname.upper() == p.name:
				return p
		return "The name doesn't exist. Please try again"

	def search_roomoccupants(self, person_name):
		"""A function that find the room that a person has been allocated to """
		occupied_rooms = []
		for room in self.rooms:
			for person in room.occupants:
				if person.name == person_name.upper(): 
					occupied_rooms.append(room)
					
		return occupied_rooms

	def search_room(self, room_name):
		"""A function that checks if the room to reallocate a person to exists"""
		for room in self.rooms:
			if room_name.upper() == room.name:
				return room
		return "The room name you have entered doesn't exist. Please enter a valid name."



	def reallocate_person (self, pname, new_room):
		""" Reallocate a person from one room to another """
		
		person = self.search_person(pname)
		room = self.search_room(new_room)

		# check if the new room is vacant
		vacant = self.check_vacant_rooms()
		if room not in [vacant_rooms for vacant_rooms in vacant['offices']+ vacant['lspace']]:
			cprint("The room you entered doesn't either exist or is not vacant", 'red')
			return "The room you entered doesn't either exist or is not vacant"

		# prevent a staff from being reallocated to a livingspace
		if isinstance(person, Staff) and isinstance (room, LivingSpace):
			cprint("Staff cannot be allocated an lspace", 'green')
			return "Staff cannot be allocated an lspace"

		for vacant_rooms in vacant['lspace']+ vacant['offices']:
			if person in [occupant for occupant in vacant_rooms.occupants]:
				if room == vacant_rooms:
					cprint(person.name + ' ' + "is already allocated to" + ' ' + room.name, 'cyan') 
					return "Already allocated"
				else:
					if vacant_rooms.room_type == room.room_type:
						vacant_rooms.occupants.remove(person)

		for occupiedroom in self.allocated_rooms:
			if person in [occupant for occupant in occupiedroom.occupants]:
				if room != occupiedroom:
					if occupiedroom.room_type == room.room_type:
						occupiedroom.occupants.remove(person)


		# Reallocate a staff or fellow to an office
		if isinstance (room, Office):
			room.occupants.append(person)
			person.allocated.append(self.search_roomoccupants(person.name))
			self.allocated_rooms.append(room)
			cprint(person.name + ' ' +"successfully moved to" + ' ' + room.name, 'green')

		# Reallocate a fellow to a livingspace
		elif isinstance(person, Fellow) and isinstance (room, LivingSpace):
			room.occupants.append(person)
			person.allocated.append(self.search_roomoccupants(person.name))
			self.allocated_rooms.append(room)
			cprint(person.name + ' ' +"successfully moved to" + ' ' + room.name, 'green')

		# Remove the person from the list of unallocated people
		for a_person in self.unallocatedpeople['offices']:
			if a_person.name == person.name:
				print(person)
				self.unallocatedpeople['offices'].remove(person)

		for a_person in self.unallocatedpeople['lspaces']:
			if a_person.name == person.name:
				if room.room_type == 'LIVINGSPACE':
					print(person)
					self.unallocatedpeople['lspaces'].remove(person)		


	def save_state(self, db_name='default'):
		"""Function that saves data from Amity's data structures to the database"""
		directory = 'databases/'
		if os.path.exists(directory + db_name + '.sqlite'):
			os.remove(directory + db_name + '.sqlite')
	
		engine = create_db(db_name)
		Base.metadata.bind = engine
		Session = sessionmaker()
		session = Session()

		# Saving rooms
		for room in self.rooms:
			existing_rooms = session.query(OfficeModel).filter_by(office_name=room.name).first()
			if existing_rooms == None:
				if isinstance(room, Office):
					allocated_members = ', '.join([str(i.name) for i in room.occupants])
					office_record = OfficeModel(office_name = room.name, occupants = allocated_members,\
						room_type = room.room_type, max_capacity = room.max_capacity)
					session.add(office_record)
					session.commit()

				elif isinstance(room, LivingSpace):
					allocated_members = ', '.join([str(i.name) for i in room.occupants])
					lspace_record = LivingSpaceModel(lspace_name = room.name, occupants = allocated_members,\
						room_type = room.room_type, max_capacity = room.max_capacity)
					session.add(lspace_record)
					session.commit()

		cprint('Rooms successfully saved to the Database','red', attrs=['bold'])

			
		# Saving people
		for person in self.people:
			existing_people = session.query(PeopleModel).filter_by(name=person.name).first()
			if existing_people == None:
				# check in the peoples
				livingspace = None
				office = None
				rooms = self.search_roomoccupants(person.name)
				if len(rooms) == 0:
					livingspace = None
					office = None
				elif len(rooms) == 1:
					for allocated_room in rooms:
						if isinstance(allocated_room, Office):
							office = allocated_room.name
							livingspace = None
						elif isinstance(allocated_room, LivingSpace):
							livingspace = allocated_room.name

							office = None
				elif len(rooms) == 2:
					person.wants_accomodation == 'Y'
					for allocated_room in rooms:
						if isinstance(allocated_room, Office):
							office = allocated_room.name
							
						elif isinstance(allocated_room, LivingSpace):
							livingspace = allocated_room.name

				person_records = PeopleModel(name = person.name, role = person.role,\
						accomodate = person.wants_accomodation, living_space = livingspace, office= office)

				session.add(person_records)
				session.commit()
			
		cprint('People successfully saved to the Database','red', attrs=['bold'])
		cprint('All data successfully saved to the Database','green', attrs=['bold'])


	def load_state(self, db_name='default'):
		"""Function that loads data from the database to Amity's data structures"""

		directory = 'databases/'
		engine = create_engine('sqlite:///' + directory + db_name + '.sqlite')
		Session = sessionmaker()
		Session.configure(bind=engine)
		session = Session()  

		self.people = []
		self.rooms = []
		self.unallocatedpeople = {'offices':[], 'lspaces':[]}
		self.allocated_rooms = []

		self.people = []
		self.rooms = []
		self.unallocatedpeople = []
		self.allocated_rooms = []

		people = session.query(PeopleModel).all()
		offices = session.query(OfficeModel).all()
		livingspaces = session.query(LivingSpaceModel).all()

		# Load people
		for person in people:
			person_name = person.name
			person_role = person.role
			accomodate = person.accomodate
			if person_role == "STAFF":
				staff= Staff(person_name)
				self.people.append(staff)
				if person.office is None:
					self.unallocatedpeople['offices'].append(staff)
			else:
				fellow = Fellow(person_name, accomodate)
				self.people.append(fellow)
				if person.living_space is None and person.office is None:
					self.unallocatedpeople['offices'].append(fellow)
					self.unallocatedpeople['lspaces'].append(fellow)

		cprint("Loading People", 'red', attrs=['bold'] )

		# Load offices
		for room in offices:
			if len(room.occupants) >= 1:
				allocated_members = room.occupants.split(', ')
				office = Office(room.office_name)
				self.rooms.append(office)
				for person_name in allocated_members:
					person = session.query(PeopleModel).filter_by(name=person_name).first()
					if person:
						person_obj = Staff(person.name)
						office.occupants.append(person_obj)

				if office.occupants:
					self.allocated_rooms.append(office)
			else:
				office = Office(room.office_name)
				self.rooms.append(office)

		cprint("Loading Offices ", 'red', attrs=['bold'] )


		# Load livingspaces
		for room in livingspaces:
			if len(room.occupants) >=1:
				allocated_members = room.occupants.split(', ')
				lspace = LivingSpace(room.lspace_name)
				self.rooms.append(lspace)
				for person_name in allocated_members:
					person = session.query(PeopleModel).filter_by(name=person_name).first()
					if person:
						person_obj = LivingSpace(person.name)
						lspace.occupants.append(person_obj)

				if office.occupants:
					self.allocated_rooms.append(lspace)
			else:
				lspace = LivingSpace(room.lspace_name)
				self.rooms.append(lspace)


		cprint("Loading livingspaces ", 'red', attrs=['bold'] )
		cprint("All data loaded successfully ", 'green', attrs=['bold'] )









