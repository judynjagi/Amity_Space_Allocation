import random

from people import People, Fellow, Staff
from rooms import Room, LivingSpace, Office
class Amity (object):
	def __init__(self):
		self.rooms = []
		self.people = []
		self.office = []
		self.lspace = []
		self.staff = []
		self.fellow = []
		self.vacantoffice = []
		self.vacantlspace =[]
		self.vacantrooms = []
		self.staffsallocated = []
		self.fellowsallocated = []
		self.peopleallocate = []
		self.unallocatedpeople = []

	def create_room(self, rname, rtype):
		for room in self.rooms:
			if rname == room.name:
				return ("Room exists")

		if rtype.upper()=="OFFICE":
			room = Office(rname, rtype)
			self.office.append(room)
			self.rooms.append(room)
			return ("office successfully created")

		elif rtype.upper()=="LIVINGSPACE":
			room = LivingSpace(rname, rtype)
			self.lspace.append(room)
			self.rooms.append(room)
			return("Livingspace successfully created")
		else:
			return ("The room type does not exist")

	def check_vacant_rooms(self):
		self.vacantoffice = []
		self.vacantrooms = []
		self.vacantlspace = []
		for room in self.office:
		
			if room.is_full():
				# self.vacantoffice.remove(room)
				# self.vacantrooms.remove(room)		
				print("There are no vacant offices")
			else:
				self.vacantoffice.append(room)
				self.vacantrooms.append(room)				
			
		for room in self.lspace:

			if room.is_full():
				return "There are no vacant livingspaces"
			else:
				self.vacantlspace.append(room)
				self.vacantrooms.append(room)
				

	def add_person(self, fname, lname, position, wants_accommodation ="N"):

		fullname = (fname + ' ' + lname)

		for name in self.people:
			if fullname.upper()== name.name:
				return("Name exists")

		staff = Staff(fullname, position)
		fellow = Fellow(fullname, position)
		


		if position.upper() == "STAFF":
			if wants_accommodation == "N":
				self.staff.append(staff)
				self.people.append(staff)
				self.unallocatedpeople.append(staff)
				
				print("Staff successfully added") 

				self.check_vacant_rooms()
				try:
					allocaterandomly = random.choice(self.vacantoffice)
					allocaterandomly.occupants.append(staff)
					self.staffsallocated.append(staff)
					self.peopleallocate.append(staff)
					self.unallocatedpeople.remove(staff)

					print (allocaterandomly, "has been allocated to ", staff )

				except TypeError:
					return ("Ha")

							
			else:
				print ("Staff cannot be allocated a livingspace")

		elif position.upper() == "FELLOW":
			self.fellow.append(fellow)
			self.people.append(fellow)
			self.unallocatedpeople(fellow)
			print("Fellow successfully added") 

			self.check_vacant_rooms()
			allocaterandomly = random.choice(self.vacantoffice)
			allocaterandomly.occupants.append(fellow)
			self.fellowsallocated.append(fellow)
			self.peopleallocate.append(fellow)
			self.unallocatedpeople.remove(fellow)
			print(allocaterandomly, "has been allocated to ", fellow )
				

			if wants_accommodation == "Y":

				self.check_vacant_rooms()
				allocaterandomly = random.choice(self.vacantoffice)
				allocaterandomly.occupants.append(fellow)
				self.fellowsallocated.append(fellow)
				self.allocatedpeople.append(fellow)
				self.unallocatedpeople.remove(fellow)

				return (allocaterandomly, "has been allocated to ", fellow )


				self.check_vacant_rooms()
				allocaterandomly = random.choice(self.vacantlspace)
				allocaterandomly.occupants.append(fellow)
				self.fellowsallocated.append(fellow)
				self.peopleallocate.append(fellow)
				self.unallocatedpeople.remove(fellow)

				print (allocaterandomly, "has been allocated to ", fellow )

					
		else:
			return "Position can either be Fellow or Staff"



	def load_people(self, filename = "None"):
		""" Add people from a text file"""
		for line in open(filename,'r').readlines():
			self.people.append(line.strip())
    		print (self.people)

 	
 	def print_allocations(self, filename = "None"):
		for room in self.rooms:
			print (room.name)
			print ("-"*10)
			for occupants in room.occupants:
				if len(room.occupants)>0:
					print (occupants.name)
					# self.peopleallocate.append(room.name, occupants.name)
					# print self.peopleallocate

		# if filename is not None:
		# 	with open(filename, 'w') as f:
		# 		f.writelines(self.peopleallocate )
					
		# 		f.close()



	def reallocate (self, firstname, lastname, new_room):

		person_name = firstname + ' ' + lastname

		# check if the person's name exists
		for person in self.people:
			if person_name not in person.name:
				("Persons' name does not exist")

		# check if the room exists and is vacant
		for room in self.rooms:
			if new_room not in room.name:
				print ("Room name does not exist")

		# check if the room is vacant
		for room in self.vacantrooms:
			if new_room not in room.name:
				print ("Either the room does not exist or it is not vacant, please enter another name")
				
		# prevent a staff from being allocated a living space
		if isinstance(person_name, Staff) and isinstance(new_room, LivingSpace):
			print ("Staff cannot be allocated a living space")

		# check if a person has been allocated a room 
		for room in self.vacantrooms:
			if person_name in[person.name for person in room.occupants]:
				if new_room == room.name:
					print (person_name  + "is already allocated to " + new_room)
				else:
					room.occupants.remove(staff)

		# Reallocate a person 
		if isinstance(person_name, Fellow):
			if isinstance(office, Office):
				new_room.occupants.append(person_name)
				self.fellowsallocated.append (person_name)

			elif isinstance(new_room, LivingSpace):
				new_room.occupants.append(person_name)
				self.fellowsallocated.append (person_name)

		elif isinstance(person_name, Staff):
			new_room.occupants.append(person_name)
			self.staffsallocated.append (person_name)

		if person_name in self.unallocatedpeople:
			self.unallocatedpeople.remove(person_name) 


amity = Amity()
print (amity.create_room("Mordor", "office"))
# print (amity.create_room("m1", "livingspace"))

print (amity.check_vacant_rooms())
# print (amity.add_person("nz", "h", "fellow", "N"))
print (amity.add_person("Stephen", "k", "staff", "N"))
print (amity.add_person("Jane", "l", "staff", "N"))
print (amity.add_person("Martin", "m", "staff", "N"))
print (amity.add_person("Judy", "n", "staff", "N"))
print (amity.add_person("Ryan", "o", "staff", "N"))
print (amity.add_person("Mary", "p", "staff", "N"))
print (amity.add_person("John", "Doe", "staff", "N"))
print(amity.print_allocations())
print (amity.add_person("OLUWAFEMI","SULE" "FELLOW","Y"))
# print("%"*70, amity.fellow)
print (amity.load_people("test.txt"))


#print(amity.print_allocations("test.py"))


# print (amity.reallocate("nz", "h", "my"))
# print (amity.reallocate("n", "k", "m"))
# print (amity.reallocate("n", "l", "m1"))



		

			

		

























