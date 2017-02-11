import random
import sys

from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text, select
from termcolor import cprint, colored

from people import People, Fellow, Staff
from rooms import Room, LivingSpace, Office
from models import OfficeModel, PeopleModel, LivingSpaceModel, create_db, Base

class Amity(object):
	""" Main Class for the Amity Program"""
	def __init__(self):
		self.rooms = []
		self.people = []
		self.allocated_rooms = []
		self.unallocatedpeople = []

	def create_room(self, rname, rtype):
		if rname.upper() in [room.name for room in self.rooms]:
			return ("Name exists")
		else:
			if rtype.upper()=="OFFICE":
				room = Office(rname)
				self.rooms.append(room)
				return ("office successfully created")

			elif rtype.upper()=="LIVINGSPACE":
				room = LivingSpace(rname)
				self.rooms.append(room)
				return("Livingspace successfully created")
			else:
				return ("The room type does not exist")

	def check_vacant_rooms(self):
		"""Check if the rooms are vacant"""
		vacantrooms = {'offices':[], 'lspace':[]}
		for room in self.rooms:
			if not room.is_full():
				if isinstance(room, Office):
					vacantrooms['offices'].append(room)
				elif isinstance(room, LivingSpace):
					vacantrooms['lspace'].append(room)

		return vacantrooms

	def add_person(self, fname, lname, position, wants_accomodation="N"):

		"""Add a person"""

		fullname = (fname + ' ' + lname)

		for person in self.people:
			if fullname.upper() == person.name.upper():
				return "Name exists"

		if position.upper() == "STAFF":
			staff = Staff(fullname)
			self.people.append(staff)
			cprint("Staff created successfully", 'green') 
			self.allocate_office(fullname, wants_accomodation)
			staff.allocated.append(self.search_roomoccupants(fullname))

		elif position.upper() == "FELLOW":
			fellow = Fellow(fullname)
			self.people.append(fellow)
			cprint("Fellow created successfully", 'green')

			self.allocate_office(fullname, wants_accomodation)
			self.allocate_livingspace(fullname, wants_accomodation)
			fellow.allocated.append(self.search_roomoccupants(fullname))

		else:
			return"Position can either be Fellow or Staff"

	def load_people(self, filename):
		""" Add people from a text file"""
		# Open the file and read all the lines
		with open(filename, 'r') as f:
			people = f.readlines()

		# Place the data in each line in a list and use indexing to get the name, role etc
		for employee in people:
			employee_information = employee.split()
			employee_fname = employee_information[0] 
			employee_lname = employee_information[1]
			role = employee_information[2]

		# Check the role of each employee and if they want accomodation
			if role == 'STAFF':
				wants_accomodation = 'N'
			elif role == 'FELLOW':
				if len(employee_information) <= 3:
					wants_accomodation = 'N'
				elif len(employee_information) == 4:
					accomodation = employee_information[3]
					if accomodation.upper() == 'Y':
						wants_accomodation = 'Y'
					else:
						wants_accomodation = 'N'
				else:
					print ("Wrong file")

			self.add_person(employee_fname, employee_lname, role, wants_accomodation)

		return "People added successfully"


	def allocate_office(self, person, wants_accommodation="N"):
		"""Allocate a person"""
		
		# Check whether person exists
		if person.upper() not in [p.name.upper() for p in self.people]:
			return "The name does not exist, please enter a valid name"

		# Check if person is a staff and they want accomodation
		for p in self.people:
			if p.name.upper() == person.upper():
				try:
					vacantrooms = self.check_vacant_rooms()
					random_office = random.choice(vacantrooms['offices'])
					random_office.occupants.append(p)
					self.allocated_rooms.append(random_office)
					return p, "has been allocated to", random_office

				except (IndexError, TypeError):
					self.unallocatedpeople.append(p)

	def allocate_livingspace(self, person, wants_accommodation="N"):
		# Check whether person exists
		if person.upper() not in [p.name.upper() for p in self.people]:
			return "The name does not exist, please enter a valid name"

		# Check if person is a staff and they want accomodation
		for p in self.people:
			if p.name.upper() == person.upper():
				break

		if isinstance(p, Staff) and wants_accommodation == "Y":
			return ("staff cannot be allocated a livingspace")

		# Allocate a staff or a fellow for an vacant office
		if isinstance(p, Fellow):
			if wants_accommodation == "Y":
				try:
					vacantrooms = self.check_vacant_rooms()
					random_lspace = random.choice(vacantrooms['lspace'])
					random_lspace.occupants.append(p)
					self.allocated_rooms.append(random_lspace)
					print(p, "has been allocated to", random_lspace)

				except (IndexError, TypeError):
					self.unallocatedpeople.append(p)


	def print_allocations(self, filename = "None"):
		""" A function that prints rooms and its occupants"""
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
						file.write("%s\n" % occupant.name )
		else:
			record = set()			
			for room in self.allocated_rooms:
				if room.name not in record:
					record.add(room)
			for sortedrooms in record:
				cprint ('\n' + sortedrooms.name + ': ' + sortedrooms.room_type, 'red')
				cprint ('-' * 50, 'red')
				for occupant in sortedrooms.occupants:
					if len(sortedrooms.occupants)>0:
						cprint (''.join(occupant.name) + ' ', 'green')

	def print_unallocated (self, filename="None"):
		"""A function that prints people who haven't been allocated yet"""
		if filename != "None":
			file = open(filename, 'w')
			for people in self.unallocatedpeople:
				file.write("%s\n" % people.name + ': ' + people.role)
		else:
			cprint ('*' * 50, 'red')
			cprint("UNALLOCATED PEOPLE", 'red')
			cprint ('*' * 50, 'red')
			for people in self.unallocatedpeople:
				if len(self.unallocatedpeople)<0:
					cprint("Everyone is allocated")
				else:
					cprint (''.join(people.name) + ' ', 'green')
					

	def print_room(self, roomname):
		"""A function that prints the occupants in the specified room"""
		for room in self.rooms:
			if roomname.upper() == room.name:
				for person in room.occupants:
					return person			
					
	def search_person(self, pname):		
		"""A function that checks if the person to be reallocated exists"""
		for p in self.people:
			if pname.upper() == p.name:
				return p
		return "The name doesn't exist. Please try again"

	def search_roomoccupants(self, pname):
		occupants_list = []
		for room in self.rooms:
			for person in room.occupants:
				if pname.upper() == person.name:
					occupants_list.append(room)
					
		return occupants_list

	def search_room(self, room):
		"""A function that checks if the room to reallocate a person to exists"""
		for r in self.rooms:
			if room.upper() == r.name:
				return r
		return "The room name you have entered doesn't exist. Please enter a valid name"


	def reallocate (self, pname, new_room):
		""" Reallocate a person from one room to another """
		
		person_obj = self.search_person(pname)
		room_obj = self.search_room(new_room)

		# check if the new room is vacant
		vacant_rooms_list = self.check_vacant_rooms()
		if room_obj.name not in [vacant_rooms.name for vacant_rooms in vacant_rooms_list['lspace']+ vacant_rooms_list['offices']]:
			return "The room you entered is not vacant"

		# prevent a staff from being reallocated to a livingspace
		if isinstance(person_obj, Staff) and isinstance (room_obj, LivingSpace):
			return "Staff cannot be reallocated to a  livingspace"

		# check if the person is already allocated to the room so as to avoid reallocating them in the same room 

		for vacant_rooms in vacant_rooms_list['lspace']+ vacant_rooms_list['offices']:
			for person_to_reallocate in vacant_rooms.occupants:
				if person_obj.name == person_to_reallocate.name:
					if room_obj.name.upper() == vacant_rooms.name:
						return person_obj.name, "is already allocated to", room_obj.name
					else: # if person doesn't exist then deallocate them
						vacant_rooms.occupants.remove(person_to_reallocate)
						# vacant_rooms.occupants-=1
						print (vacant_rooms.occupants)
			# Rellocate a staff to an office
			if isinstance (room_obj, Office):
				vacant_rooms.occupants.remove(person_to_reallocate)
				room_obj.occupants.append(person_obj)
				
				return person_obj.name, "successfully moved to", room_obj.name
			# Reallocate a fellow to a livingspace
			if isinstance(person_obj, Fellow) and isinstance (room_obj, LivingSpace):
				room_obj.occupants.append(person_obj)
				print(person_obj.name, "successfully moved to", room_obj.name) 

	def update_tables(self, session):
		""" Clears the information in database tables before populating the database
			again """
		metadata = Base.metadata
		for table in reversed(metadata.sorted_tables):
			session.execute(table.delete())
		session.commit()

	def save_state(self, db_name='newest'):
		engine = create_db(db_name)
		Base.metadata.bind = engine
		Session = sessionmaker()
		session = Session()
		self.update_tables(session)
		for room in self.rooms:
			if isinstance(room, Office):
				allocated_members = ', '.join([str(i.name) for i in room.occupants])
				room_name = room.name
				room_type = room.room_type
				capacity = room.max_capacity
				office_record = OfficeModel(office_name = room_name, occupants = allocated_members,\
					room_type = room_type, max_capacity = capacity)
				session.add(office_record)
				session.commit()

			if isinstance(room, LivingSpace):
				allocated_members = ', '.join([str(i.name) for i in room.occupants])
				room_name = room.name
				room_type = room.room_type
				capacity = room.max_capacity
				lspace_record = LivingSpaceModel(lspace_name = room_name, occupants = allocated_members,\
					room_type = room_type, max_capacity = capacity)
				session.add(lspace_record)
				session.commit()

		for person in self.people:
			name = person.name
			role = person.role
			wants_accommodation = person.wants_accommodation
			rooms = self.search_roomoccupants(name)
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
				wants_accommodation == False
				for allocated_room in rooms:
					if isinstance(allocated_room, Office):
						office = allocated_room.name
					elif isinstance(allocated_room, LivingSpace):
						livingspace = allocated_room.name

			person_records = PeopleModel(name = name, role = role,\
					accomodate = wants_accommodation, living_space = livingspace, office= office)

			session.add(person_records)
			session.commit()

	def load_state(self, db_name='newest'):
		engine = create_db(db_name)
		Base.metadata.bind = engine
		Session = sessionmaker()
		Session.configure(bind=engine)
		session = Session()

		people = session.query(PeopleModel).all()
		offices = session.query(OfficeModel).all()
		livingspaces = session.query(LivingSpaceModel).all()

		for person in people:
			person_name = person.name
			person_role = person.role
			if person_role == "STAFF":
				staff= Staff(person_name)
				self.people.append(staff)
				if person.office is None:
					self.unallocatedpeople.append(staff)
			else:
				fellow = Fellow(person_name)
				self.people.append(fellow)
				if person.living_space is None and person.office is None:
					self.unallocatedpeople.append(fellow)

		for room in offices:
			if len(room.occupants) > 0:
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

	
		for room in livingspaces:
			if len(room.occupants) > 0:
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

					

amity = Amity()
amity.load_state()
# print (amity.create_room("Mordor2", "livingspace"))
# print (amity.create_room("Mordor3", "office"))
# print (amity.create_room("Mordor4", "livingspace"))
# print (amity.create_room("Mordor9", "office"))
# print (amity.create_room("Mordor1", "office"))

# print (amity.check_vacant_rooms())
# print (amity.add_person("judy", "njagi", "staff", "N"))
# print (amity.add_person("jay", "havy", "staff", "N"))
# print (amity.add_person("robert", "maina", "staff", "N"))
# print (amity.add_person("jane", "wangu", "fellow", "Y"))
# print (amity.add_person("cb", "mwaura", "staff", "N"))
# print (amity.add_person("harriet", "njeri", "staff", "N"))
# print (amity.add_person("jay", "son", "fellow", "Y"))
# print(amity.load_people("people.txt"))
print (amity.print_allocations())
# 
# print (amity.print_unallocated())
# print (amity.print_room("Mordor"))
print (amity.reallocate("cb mwaura", "Mordor3"))
# print (amity.rooms)
amity.save_state()


# import pdb; pdb.set_trace()



