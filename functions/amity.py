from people import Fellow, Staff
from rooms import LivingSpace, Office
import random
class Amity (object):
	def __init__(self):
		self.rooms = []
		self.people = []
		self.staff = []
		self.fellow = []
		self.livingspace = []
		self.office = []
		self.occupants = []
		self.vacantoffice = []
		self.vacantrooms = []
		self. occupied = []
		

	def create_room(self, newroom, room_type):
		'''Creates a new room (office or living space)'''

		room = None
		if room_type.upper()== "OFFICE" or "LIVINGSPACE":
			if room_type.upper() == "OFFICE":

				for room in self.rooms:
					if newroom.upper() == room.name.upper() or len(newroom) == 0:
						return "The room name you entered exists or your input is empty. Please input a valid name"
				room = Office(newroom)
				self.office.append (room)
				print ("Room successfully added")
			else:
				if room_type.upper() == 'LIVINGSPACE':
					'''checks if the name exists'''
					for room in self.rooms:
						if newroom.upper() == room.name.upper() or len(newroom) == 0:
							return "The room name you entered exists or your input is empty. Please input a valid name"
					room = LivingSpace(newroom)
					self.livingspace.append(room)
					print (room)
			
			if room is not None:
				self.rooms.append (room)
			print ("You have created the following rooms:" )
			print 
			print ({newroom: room_type})

	def add_person(self, fname, lname, position, wants_accommodation = False):
		self.fname = fname
		self.lname = lname
		self.position = position
		self.wants_accommodation = wants_accommodation
		self.fullname = fname + ' ' + lname

		for namey in self.people:
			if self.fullname == namey.name.upper() or len(self.fullname) <1:
				return "The name exists or the input is empty. Please try again"
		if position.upper() == 'STAFF':
			if wants_accommodation == False:
				allnames = Staff(self.fullname)
				self.staff.append (allnames)
				print (allnames)

			else:
				for office in Amity.office:
					if office.max_occupants > office.roomcount:
						self.vacantoffice.append(office)
						self.vacantrooms.append(office)
						allocate = random.choice(self.vacantoffice)
						staff = Staff(name)
						allocate.occupants.append (staff)
						self.occupied.append(staff)
						print (name + "with Employee ID" + staff.person_id + "has been allocated to office" + allocate.name)

					elif office.max_occupants == office.roomcount:
						print ("No rooms available") 

		else:
			if position.upper() == 'FELLOW':
				if wants_accommodation == False:
					allnames = Fellow(self.fullname)
					self.fellow.append(allnames)
				else:
					for rooms in self.vacantrooms:
						if rooms.max_occupants > rooms.roomcount:
							self.vacantrooms.append(rooms)
							allocate = random.choice(self.rooms)
							fellow = Fellow(self.name)
							allocate.occupants.append (fellow)
							self.occupied.append(fellow)
							print (name + "with Employee ID" + fellow.person_id + "has been allocated to office" + allocate.name)

						elif rooms.max_occupants == room.roomcount:
							print ("No rooms available")
amity = Amity()
print (amity.add_person("Judy", "Njagi", "Staff"))

# 	def reallocate(self, your_id, newroom):
# 		self.your_id = your_id
		
# 		'''check if the persons id exists'''
# 		for ident in self.people:
# 			if your_id != ident.person_id and len(your_id)<1:
# 				print ("That identification number does not exist")
			
# 		'''check if newroom exists '''
# 		for room in self.rooms:
# 			if newroom not in room.name:
# 				print ("That room does not exist")

# 		'''check if newroom is vacant'''
# 		for room in self.vacantrooms:
# 			if newroom not in room.name:
# 				print ("There are no vacant rooms")

# 		'''Do not allocate staff to livingspace'''
# 		for person in self.people:
# 			if type(person) == 'staff':
# 				for room in self.


			




				



























# 		# else:
# 		# 	return "Invalid Position"
# 		# self.people.append(allnames)
# 		# 	#print(type(allnames))
# 		# 	return (allnames.name)
		
# # 	def check_availability(self):
# # 		for office in self.office:
# # 			if office.max_occupants > office.roomcount:
# # 				self.vacantoffice.append(office)
# # 				self.rooms.append(office)
# # 			elif office.max_occupants == office.roomcount:
# # 				print ("No rooms available") 
# # 		for livingspace in self.livingspace:
# # 			if livingspace.max_occupants > livingspace.roomcount:
# # 				self.vacantlivingrooms.append(livingspace)
# # 					self.rooms.append(livingspace)
# # 						elif livingspace.max_occupants == livingspace.roomcount:
# # 							print ("No rooms available")

		
# # 		amity = Amity()
# # print (amity.check_availability())


# # 	def allocate_room (self)

	

# # # class Person (Amity):
# # 	def __init__(self):
# # 		self.name = []
# # 		self.id = []		
# # class Staff(Person):
# # 	def staff_member(self, name , staff_id):
# # 		a = Person()
# # 		a.name.append(name)
# # 		a.id.append(staff_id)

# # 		return {'staffid': a.id, 'staffname': a.name, }
# s = Staff()
# print (s.staff_member('Judy', '567'))


# # 	pass
# # class Fellow(Person):
# # 	pass
# # class Room (Amity):
# # 	pass
# # class Office (Room):
# # 	pass
# # class LivingSpace(Room):
# # 	pass

