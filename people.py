class People(object):
	""""""
	
	def __init__(self,name, role = "None", wants_accommodation="N"):
		self.name = name.upper()
		self.role = role.upper()
		self.wants_accommodation = wants_accommodation.upper()
		self.allocated = []
		

	def __repr__(self):
		return self.name .upper()+  " " + self.role.upper() + " " + self.wants_accommodation

class Fellow(People):

	def __init__(self, name):
		
		super(Fellow, self).__init__(name, role = "Fellow", wants_accommodation="N")

	
class Staff(People):
	def __init__(self, name):
	
		super(Staff, self).__init__(name, role = "Staff", wants_accommodation="N")




