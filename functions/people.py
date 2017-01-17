class People (object):
	def __init__(self,name, role = "None"):
		self.name = name
		self.role = role
		self.person_id = id(self)

	def __repr__(self):
		return self.name .upper()+  " " + self.role.upper()

	
class Fellow(People):

	def __init__(self, name, role = "Fellow"):
		
		super(Fellow, self).__init__(name, role)

	
class Staff (People):
	def __init__(self, name, role = "Staff"):
	
		super(Staff, self).__init__(name, role)




