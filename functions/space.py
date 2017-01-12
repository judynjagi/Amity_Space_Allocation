import random

from people import People, Fellow, Staff
from rooms import Room, LivingSpace, Office
class Amity (object):
	def __init__(self):
		self.rooms = []
		self.people = []
		self.office = []
		self.lspace = []
		self.staff = ["Judy Njagi"]
		self.fellow = ["Judy Njagi"]
		self.vacantoffice = []
		self.vacantlspace =[]

	def create_room(self, rname, rtype):
		if rname in self.rooms:
			print ("Room exists")

		if rtype.upper()=="OFFICE":
			room = Office(rname, rtype)
			self.office.append(room)
			self.rooms.append(room)
			print ("office successfully created")

		elif rtype.upper()=="LIVINGSPACE":
			room = LivingSpace(rname, rtype)
			self.lspace.append(room)
			self.rooms.append(room)
			print ("Livingspace successfully created")
		else:
			print ("The room type does not exist")

	def check_vacant_rooms(self):
		for room in self.office:
		
			if room.is_full():
				return "There are no vacant offices"
			else:
				self.vacantoffice.append(room)
				self.rooms.append(room)
			
		for room in self.lspace:

			if room.is_full():
				return "There are no vacant livingspace"
			else:
				self.vacantlspace.append(room)
				self.rooms.append(room)

	def add_person(self, fname, lname, position, wants_accommodation ="N"):

		fullname = (fname + ' ' + lname)

		if fullname.upper() in self.people:
			print("Name exists")

		staff = Staff(fullname, position)
		fellow = Fellow(fullname, position)


		if position.upper() == "STAFF":
			if wants_accommodation == "N":
				self.staff.append(staff)
				self.people.append(staff)
				print("Staff successfully added") 

				self.check_vacant_rooms()
				allocaterandomly = random.choice(self.vacantoffice)
				allocaterandomly.occupants.append(staff)
				print (allocaterandomly, "has been allocated to ", staff )
							
			else:
				return "Staff cannot be allocated a livingspace"

		elif position.upper() == "FELLOW":
			self.staff.append(fellow)
			self.people.append(fellow)
			print("Staff successfully added") 

			if wants_accommodation == "N":
				self.check_vacant_rooms()
				allocaterandomly = random.choice(self.vacantoffice)
				allocaterandomly.occupants.append(fellow)

				print (allocaterandomly, "has been allocated to ", fellow )

			elif wants_accommodation == "Y":

				self.check_vacant_rooms()
				allocaterandomly = random.choice(self.vacantoffice)
				allocaterandomly.occupants.append(fellow)

				print (allocaterandomly, "has been allocated to ", fellow )


				allocaterandomly = random.choice(self.vacantlspace)
				allocaterandomly.occupants.append(fellow)

				print (allocaterandomly, "has been allocated to ", fellow )
					
		else:
			return "Position can either be Fellow or Staff"

	def allocate (self):
		self.check_vacant_rooms
		if len()

