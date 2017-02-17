class People(object):
	""""""
	
	def __init__(self,name, role = "None", wants_accomodation="N"):
		self.name = name.upper()
		self.role = role.upper()
		self.wants_accomodation = wants_accomodation.upper()
		self.allocated = []
		

	def __repr__(self):
		return self.name .upper()+  " " + self.role.upper() + " " + self.wants_accomodation

class Fellow(People):

	def __init__(self, name):
		
		super(Fellow, self).__init__(name, role = "Fellow", wants_accomodation="N")

	
class Staff(People):
	def __init__(self, name):
	
		super(Staff, self).__init__(name, role = "Staff", wants_accomodation="N")