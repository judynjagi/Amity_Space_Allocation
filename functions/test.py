import unittest
import sys
from space import Amity
class TestClasses(unittest.TestCase):
	def setUp(self):
		self.space = Amity()

	def test_create_office_rooms(self):
		#check if an office room has been created
		self.assertEqual(self.space.create_room("Room1", "Office"), "office successfully created")
		
	def test_room_has_been_added_to_office_list(self):
		initial_count = len(self.space.office)
		self.assertEqual(self.space.create_room("Room1", "Office"), "office successfully created")
		new_count = len(self.space.office)
		self.assertEqual(new_count, initial_count+1)

	def test_create_livingspace_rooms(self):
		# check if a livingspace rooms have been created
		initial_count = len(self.space.lspace)
		self.assertEqual(self.space.create_room("Room3", "LIVINGSPACE"), "Livingspace successfully created")
		new_count = len(self.space.lspace)
		self.assertEqual(new_count, initial_count + 1)

	def test_room_has_been_added_to_room_list(self):
		#check that office and livingspace rooms have been added to the rooms list
		initial_count = len(self.space.rooms)
		self.assertEqual(self.space.create_room("Room3", "LIVINGSPACE"), "Livingspace successfully created")
		self.assertEqual(self.space.create_room("Room1", "Office"), "office successfully created")
		new_count = len(self.space.rooms)
		self.assertEqual(new_count, initial_count + 2)
	
	def test_if_roomtype_does_not_exist(self):
		# check if a livingspace rooms have been created
		self.assertEqual(self.space.create_room("Room3", "Bedroom"), "The room type does not exist")
		
	def test_if_room_exists_in_the_list(self):
		#check if room name exists
		self.assertNotIn("Room2", self.space.rooms, msg="Room exists")

		""" Test for the add person Method"""

	def test_add_person(self):
		self.assertNotIn("JUDY NJAGI", self.space.people, msg="Name exists")

	def test_

	# def test_check_if_staff_has_been_added(self):
	# 	self.assertEqual()
	
	# def test_add_person(self):
	# self.assertNotIn("JUDY NJAGI", self.space.people, msg="Name exists")

if __name__ == '__main__':
	unittest.main()

