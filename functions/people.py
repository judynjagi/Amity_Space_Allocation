class People (object):
	def __init__(self,name, role):
		self.name = name
		self.role = role
		self.person_id = id(self)

	def __repr__(self):
		return self.name + " who is " + self.role

	
class Fellow(People):

	def __init__(self, name, role):
		super().__init__(name, role)

	
class Staff (People):
	def __init__(self, name, role):
		super().__init__(name, role)




