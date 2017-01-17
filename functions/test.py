import unittest
import sys
from space import Amity
class TestClasses(unittest.TestCase):
	def setUp(self):
		self.space = Amity()

	def test_create_offices_and_and_them_to_a_list(self):
		# create rooms and append to an office list
		initial_count = len(self.space.office)
		self.assertEqual(self.space.create_room("Room1", "OFFICE"), "office successfully created")
		new_count = len(self.space.office)
		self.assertEqual(new_count, initial_count+1)

	def test_if_room_exists_in_the_list(self):
		# check if room name exists in the room list
		self.assertNotIn("Room2", self.space.rooms, msg="Room exists")	

	def test_create_livingspace_rooms_and_them_to_a_list(self):
		# check if a livingspace rooms have been created and appended to the lspace list
		initial_count = len(self.space.lspace)
		self.assertEqual(self.space.create_room("Room3", "LIVINGSPACE"), "Livingspace successfully created")
		new_count = len(self.space.lspace)
		self.assertEqual(new_count, initial_count + 1)

	def test_room_has_been_added_to_room_list(self):
		#check that office and livingspace rooms have been added to the rooms list
		initial_count = len(self.space.rooms)
		self.assertEqual(self.space.create_room("Room3", "LIVINGSPACE"), "Livingspace successfully created")
		self.assertEqual(self.space.create_room("Room1", "OFFICE"), "office successfully created")
		new_count = len(self.space.rooms)
		self.assertEqual(new_count, initial_count + 2)
	
	def test_if_roomtype_does_not_exist(self):
		# check that only an office and livingspace room type can be created
		self.assertEqual(self.space.create_room("Room3", "BEDROOM"), "The room type does not exist")
		
	

	def test_add_person(self):
		# check if the name of the person exists in the people list
		self.assertNotIn("JUDY NJAGI", self.space.people, msg="Name exists")

	def test_check_if_staff_has_been_added_to_a_list(self):
		# test to add a staff and append him or her in the staff list
		initial_count = len(self.space.staff)
		self.assertEqual(self.space.add_person("JUDY", "NJAGI", "STAFF", "N"), "Staff successfully added")
		new_count = len(self.space.staff)
		self.assertEqual(new_count, initial_count + 1)

	def test_check_if_fellow_has_been_added_to_a_list(self):
		# test to add a fellow and append him or her in the staff list
		initial_count = len(self.space.fellow)
		self.assertEqual(self.space.add_person("JUDY", "NYAWIRA", "FELLOW", "N"), "Fellow successfully added")
		new_count = len(self.space.fellow)
		self.assertEqual(new_count, initial_count + 1)

	def test_position_is_staff_fellow(self):
		# test that a person can only be a staff or fellow and that it cannot also be left empty
		self.assertEqual(self.space.add_person("JUDY", "NJAGI", "YEGO","Y"), "Position can either be Fellow or Staff")
		self.assertEqual(self.space.add_person("JUDY", "NJAGI", "","Y"), "Position can either be Fellow or Staff")

	def test_fellow_or_staff_has_been_allocated_a_random_room(self):
		# check random room allocation
		initial_count = len(self.space.vacantoffice)
		new_count = len(self.space.vacantoffice)-1
		self.assertNotEqual(new_count, initial_count)

	def test_fellow_has_been_allocated_a_livingspace_room(self):
		# check random lspace allocation
		initial_count = len(self.space.vacantlspace)
		new_count = len(self.space.vacantlspace)-1
		self.assertNotEqual(new_count, initial_count)

	def test_fellow_has_been_allocated_an_office_room(self):
		# check random office allocation
		initial_count = len(self.space.vacantoffice)
		new_count = len(self.space.vacantoffice)-1
		self.assertNotEqual(new_count, initial_count)

	def test_staff_cannot_be_allocated_a_living_space(self):
		# check that a staff cannot be allocated a living space 
		self.assertEqual(self.space.add_person("JUDY", "NJAGI", "STAFF","Y"), "Staff cannot be allocated a livingspace")

	# def test_reallocate(self):
	# 	# check that the room and name of the person you want to reallocate exist
	# 	self.assertIn("JACK MAYOR", self.space.people, msg="The persons name does not exist in the database")
	# 	self.assertIn("ROOM1", self.space.rooms, msg="The room does not exist in the database")


	# def test_check_if_fellow_has_been_added_to_a_list(self):
	# 	initial_count = len(self.space.fellow)
	# 	self.assertEqual(self.space.add_person("JUDY", "NJAGI", "FELLOW"), "Fellow successfully added")
	# 	new_count = len(self.space.fellow)
	# 	self.assertEqual(new_count, initial_count + 1)


	# def test_check_if_staff_has_been_added(self):
	# 	self.assertEqual()
	
	# def test_add_person(self):
	# self.assertNotIn("JUDY NJAGI", self.space.people, msg="Name exists")

if __name__ == '__main__':
	unittest.main()

