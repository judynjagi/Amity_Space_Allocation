class People(object):
	""""""
	
	def __init__(self,name, wants_accomodation, role = "None"):
		self.name = name.upper()
		self.role = role.upper()
		self.wants_accomodation = wants_accomodation.upper()
		self.allocated = []
		

	def __repr__(self):
		return self.name .upper()+  " " + self.role.upper() + " " + self.wants_accomodation

class Fellow(People):

	def __init__(self, name, wants_accomodation):
		
		super(Fellow, self).__init__(name, wants_accomodation, "Fellow")

	
class Staff(People):
	def __init__(self, name):
	
		super(Staff, self).__init__(name, 'N', "Staff")