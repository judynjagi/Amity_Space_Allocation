class Room (object):

	def __init__(self, name, room_type):
		self.name = name.upper()
		self.room_type = room_type.upper()
		self.occupants = []
		max_capacity = 0

	def __repr__(self):
		return self.name + " :" + "  " + self.room_type 

	def is_full(self):
		return len(self.occupants) == self.max_capacity;
				
class LivingSpace(Room):

	def __init__(self, name, room_type ="LivingSpace"):
		self.max_capacity = 4
		super(LivingSpace, self).__init__(name, room_type)

class Office (Room):
	def __init__(self, name, room_type= "Office"):
		self.max_capacity = 6
		super(Office, self).__init__(name, room_type)

	# def __repr__(self): 
	# 	return "Room: {}".format(self.room_type)
# room = LivingSpace("Judy")
# print (room.max_capacity)



