import unittest
import os
import sys

from ..app.classes.amity import Amity
from ..app.classes.rooms import Room, Office, LivingSpace
from ..app.classes.people import Fellow, Staff

class TestCreateRoom(unittest.TestCase):
	def setUp(self):
		self.space = Amity()
		self.offices = self.space.create_room("Room2", "OFFICE")
		self.lspaces = self.space.create_room("Room1", "LIVINGSPACE") 

		self.fellows = self.space.add_person("JUDY NYAWIRA", "FELLOW", "N")
		self.staffs = self.space.add_person("JUDY NJAGI", "STAFF", "N")
		self.fellowaccommodate = self.space.add_person("JAMES KURIA", "FELLOW", "Y")

	def test_create_room_exists_in_the_list(self):
		# check if room name exists in the room list
		print(self.space.rooms)
		self.assertTrue("Room2" .upper(), 'ROOM2')
		self.assertEqual(self.space.create_room("Room1", "OFFICE"), "Name exists")

	def test_create_room_office_and_to_a_list(self):
		# create rooms and append to an office list
		self.assertEqual(self.offices, "office successfully created")

	def test_create_room_livingspace_added_in_a_list(self):
		# check if livingspace rooms have been created and appended to the lspace list
		self.assertEqual(self.lspaces, "Livingspace successfully created")

	def test_create_room_check_roomtype_does_not_exist(self):
		# check that only an office and livingspace room type can be created
		self.assertEqual(self.space.create_room("Room4", "BEDROOM"), "The room type does not exist")

	def test_create_room_rooms_added_to_list(self):
		initial_count = len(self.space.rooms)
		self.space.create_room("Room4", "OFFICE")
		new_count = len(self.space.rooms)
		self.assertEqual(new_count, initial_count+1)

	def test_check_vacant_rooms(self):
		p = self.space.check_vacant_rooms()
		initial_count = len(p['offices'])
		self.space.create_room("Room4", "OFFICE")
		p = self.space.check_vacant_rooms()
		after_count = len(p['offices'])
		self.assertEqual(after_count, initial_count+1)

	def test_add_person_if_exist(self):
		# check if the name of the person exists in the people list
		self.assertEqual(self.space.add_person("JUDY NJAGI", "STAFF", "N"), "Name exists")

	def test_add_person_list_increases(self):
		initial_count = len(self.space.people)
		self.space.add_person("BATIAN THEURI", "FELLOW", "N")
		self.space.add_person("VERO WAIRIMU", "STAFF", "N")
		new_count = len(self.space.people)
		self.assertEqual(new_count, initial_count + 2)

	def test_add_person_position_either_staff_or_fellow(self):
		# test that a person can only be a staff or fellow and that it cannot also be left empty
		self.assertEqual(self.space.add_person("SHARON NJERI", "YEGO","Y"), "Position can either be Fellow or Staff")
		self.assertEqual(self.space.add_person("IAN KING", "","Y"), "Position can either be Fellow or Staff")

	def test_add_staff_who_wants_accomodation(self):
		self.space.create_room("Room4", "LIVINGSPACE")
		staff = self.space.add_person("JOHN NGATIA", "STAFF", "Y")
		self.assertEqual(staff, "staff cannot be created")

	def test_load_people(self):
		result = self.space.load_people("people.txt")
		self.assertEqual(result, "People added successfully")

	def test_load_people_file_exists(self):
		result = self.space.load_people("people.txt")
		path = os.path.dirname(os.path.realpath(__file__))+"/" + result
		self.assertTrue(path)

	def test_allocate_person_exists(self):
		self.assertEqual(self.space.allocate_office("RYAN CATEY", "N"),"The name does not exist, please enter a valid name")
		self.assertEqual(self.space.allocate_office("MARGARET AISHA", "N"),"The name does not exist, please enter a valid name")
	
	def test_allocate_staff_to_livingroom(self):
		allocate = self.space.allocate_livingspace("JUDY NJAGI", "Y")
		self.assertEqual(allocate, "staff cannot be allocated a livingspace")

	def test_allocate_staff_to_office(self):
		self.space.create_room("Hogwarts", "OFFICE")
		self.space.add_person("JAY HAVY", "STAFF", "N")

	def test_print_allocations(self):
		onscreen = self.space.print_allocations()
		file = self.space.print_allocations("load.txt")
		self.assertTrue(os.path.exists('load.txt'))
		self.assertTrue(os.path.isfile('load.txt'))
		self.assertEqual(len(self.space.allocations), 4)

	def test_print_unallocated(self):
		file = self.space.print_unallocated("unallocated.txt")
		self.assertTrue(os.path.exists('unallocated.txt'))
		self.assertTrue(os.path.isfile('unallocated.txt'))
		self.assertEqual(len(self.space.unallocatedpeople), 0)

	def test_print_unallocated_contains_people(self):
		if len(self.space.unallocatedpeople)>0:
			self.assertTrue(self.space.print_unallocated())

	def test_print_room(self):
		self.space.create_room("Modor", "OFFICE")
		self.space.print_room("Modor")
		self.assertEqual("Modor".upper(), 'MODOR')

	def test_search_person(self):
		self.assertTrue(self.space.search_person("JUDY NJAGI"))
		self.assertEqual(self.space.search_person("AMOS NDIGA"), "The name doesn't exist. Please try again") 

	def test_search_room(self):
		self.assertTrue(self.space.search_room("ROOM2"))
		self.assertEqual(self.space.search_room("ROOM6"), "The room name you have entered doesn't exist. Please enter a valid name") 

	def test_reallocate_person(self):
		self.space.create_room("ROOM3", "LIVINGSPACE")
		reallocate = self.space.reallocate_person("JUDY NJAGI", "ROOM3")
		self.assertEqual(reallocate, "Staff cannot be allocated an lspace")
		#self.space.search_person("JUDY NJAGI")
		# self.space.search_room("ROOM1")
		# self.assertNotIn("ROOM1", self.space.check_vacant_rooms(), msg="The room you entered is not vacant") 

	

# 	def test_load_state(self):
# 		pass
# 	def test_save_state(self):
# 		pass

if __name__ == '__main__':
	unittest.main()

