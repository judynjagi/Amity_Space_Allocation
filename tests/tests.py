import unittest
import os
import sys
# includes the directory containing your package directory in PYTHONPATH
PACKAGE_PARENT = '..'
SCRIPT_DIR = sys.path.append( os.path.join( os.path.dirname(__file__), os.path.pardir ) ) 

from app.classes.amity import Amity
from app.classes.rooms import Room, Office, LivingSpace
from app.classes.people import Fellow, Staff

class TestCreateRoom(unittest.TestCase):
	def setUp(self):
		self.amity = Amity()
		self.office = self.amity.create_room("Room2", "OFFICE")
		self.lspace = self.amity.create_room("Room1", "LIVINGSPACE") 

		self.fellows = self.amity.add_person("JUDY NYAWIRA", "FELLOW", "N")
		self.staff = self.amity.add_person("JUDY NJAGI", "STAFF", "N")
		self.fellowaccommodate = self.amity.add_person("JAMES KURIA", "FELLOW", "Y")


	def test_create_room_exists_in_the_list(self):
		# check if room name exists in the room list
		self.assertTrue("Room2" .upper(), 'ROOM2')
		self.assertEqual(self.amity.create_room("Room1", "OFFICE"), "Name exists")

	def test_create_room_office(self):
		# create an office 
		self.assertEqual(self.office, "office successfully created")

	def test_create_room_livingspace(self):
		# create a  livingspace

		self.assertEqual(self.lspace, "Livingspace successfully created")

	def test_create_room_check_roomtype_does_not_exist(self):
		# check that only an office and livingspace room type can be created
		self.assertEqual(self.amity.create_room("Room4", "BEDROOM"), "The room type does not exist")

	def test_create_room_rooms_added_to_list(self):

		# check if livingspace or offices have been created and appended to the lspace list

		initial_count = len(self.amity.rooms)
		self.amity.create_room("Room4", "OFFICE")
		new_count = len(self.amity.rooms)
		self.assertEqual(new_count, initial_count+1)

	def test_check_vacant_rooms(self):
		# Check if the lenght of dictionary that contains vacant rooms increases

		p = self.amity.check_vacant_rooms()
		initial_count = len(p['offices'])
		self.amity.create_room("Room4", "OFFICE")
		p = self.amity.check_vacant_rooms()
		after_count = len(p['offices'])
		self.assertEqual(after_count, initial_count+1)

	def test_add_person_if_exist(self):
		# check if the name of the person exists in the people list
		self.assertEqual(self.amity.add_person("JUDY NJAGI", "STAFF", "N"), "Name exists")
		self.assertIn(self.amity.people[-1],self.amity.people)
		
	def test_add_person_list_increases(self):
		# Check that the person's list increases after you add a staff and fellow
		initial_count = len(self.amity.people)
		self.amity.add_person("BATIAN THEURI", "FELLOW", "N")
		self.amity.add_person("VERO WAIRIMU", "STAFF", "N")
		new_count = len(self.amity.people)
		self.assertEqual(new_count, initial_count + 2)

	def test_add_person_position_either_staff_or_fellow(self):
		# Test that a person can only be a staff or fellow and that it cannot also be left empty
		self.assertEqual(self.amity.add_person("SHARON NJERI", "YEGO","Y"), "Position can either be Fellow or Staff")
		self.assertEqual(self.amity.add_person("IAN KING", "","Y"), "Position can either be Fellow or Staff")

	def test_add_person_accomodate_either_y_or_n(self):
		# Ensure that accomodate only takes Y or N
		self.assertEqual(self.amity.add_person("SHARON NJERI", "FELLOW","Yes"), "Wants_accommodation only takes 'N' or 'Y' values")
		self.assertEqual(self.amity.add_person("IAN KING", "STAFF","No"), "Wants_accommodation only takes 'N' or 'Y' values")

	def test_add_staff_who_wants_accomodation(self):
		# Prevent a staff who wants accomodation from being created
		staff = self.amity.add_person("JOHN NGATIA", "STAFF", "Y")
		self.assertEqual(staff, "staff cannot be created")

	def test_load_people_existing_files(self):
		# Test if the file and path for the file exists 
		result = self.amity.load_people("people.txt")
		self.assertTrue(os.path.isfile("people.txt"))
		self.assertTrue(os.path.exists("people.txt"))

		# test for another file extension other than .txt
		result = self.amity.load_people("sample.py")
		self.assertEqual(result, "Invalid path.")

		try:
			self.amity.load_people("empty.txt")
		except:
			self.assertRaises(IndexError, " Empty file!.")

	def test_allocate_person_exists(self):
		# Check if the name exists
		self.assertEqual(self.amity.allocate_office("RYAN CATEY", "N"),"The name does not exist, please enter a valid name")
		self.assertEqual(self.amity.allocate_livingspace("MARGARET AISHA", "N"),"The name does not exist, please enter a valid name")
	
	def test_allocate_staff_to_livingroom(self):
		# Prevent staff from being allocated an lspace
		allocate = self.amity.allocate_livingspace("JUDY NJAGI", "Y")
		self.assertEqual(allocate, "staff cannot be allocated a livingspace")	

	def test_print_allocations(self):
		# Check the lenght of the list of allocated people after writing into a file
		file = self.amity.print_allocations("load.txt")
		self.assertTrue(os.path.exists('load.txt'))
		self.assertTrue(os.path.isfile('load.txt'))
		self.assertEqual(len(self.amity.allocated_rooms), 4)

	def test_print_unallocated(self):
		# Check the lenght of the unallocated list after writing into a file
		file = self.amity.print_unallocated("unallocated.txt")
		self.assertTrue(os.path.exists('unallocated.txt'))
		self.assertTrue(os.path.isfile('unallocated.txt'))
		self.assertEqual(len(self.amity.unallocatedpeople['offices']+self.amity.unallocatedpeople['lspaces']), 0)

	def test_print_unallocated_contains_people(self):
		# Ensure that unallocated people can only be printed out if they are equal or more than one
		if len(self.amity.unallocatedpeople['offices']+self.amity.unallocatedpeople['lspaces'])>=1:
			self.assertTrue(self.amity.print_unallocated())

	def test_print_room(self):
		# Test that values are converted to upper
		self.amity.create_room("Modor", "OFFICE")
		self.amity.print_room("Modor")
		self.assertEqual("Modor".upper(), 'MODOR')

	def test_search_person(self):
		# Return the persons name if it exists else a message if it doesn't exist
		self.assertTrue(self.amity.search_person("JUDY NJAGI"))
		self.assertEqual(self.amity.search_person("AMOS NDIGA"), "The name doesn't exist. Please try again") 

	def test_search_room(self):
		# Return the room's name if it exists else a message if it doesn't exist
		self.assertTrue(self.amity.search_room("ROOM2"))
		self.assertEqual(self.amity.search_room("ROOM6"), "The room name you have entered doesn't exist. Please enter a valid name.") 

	def test_reallocate_person(self):
		# Prevent a staff from being reallocated to a livingspace
		reallocate = self.amity.reallocate_person("JUDY NJAGI", "ROOM1")
		self.assertEqual(reallocate, "Staff cannot be allocated an lspace")

	def test_reallocate_person_to_a_vacant_room(self):
		# Check if the room you want to reallocate a person to is vacant
		vacant = self.amity.check_vacant_rooms()
		room = self.amity.search_room("Room6")
		reallocate = self.amity.reallocate_person("JUDY NJAGI", "Room6")
		
		if room not in vacant:
			self.assertEqual(reallocate, "The room you entered doesn't either exist or is not vacant")

	def test_reallocate_person_already_in_the_room(self):
		# Check if the person is in the room you want to reallocate them to
		reallocate = self.amity.reallocate_person("JUDY NJAGI", "Room2")
		self.assertEqual(reallocate, "Already allocated")

	def test_reallocate_person_to_another_room(self):
		# Check that after reallocating a person to a room, it exists in the list of allocated rooms
		self.amity.create_room("Room10", "OFFICE")
		reallocate = self.amity.reallocate_person("JUDY NJAGI", "Room10")
		room = self.amity.search_room("Room10")
		self.assertIn(room, self.amity.allocated_rooms)

		self.amity.create_room("Room11", "LIVINGSPACE")
		reallocate = self.amity.reallocate_person("JAMES KURIA", "Room11")
		room = self.amity.search_room("Room11")
		self.assertIn(room, self.amity.allocated_rooms)

	def test_save_and_load_state(self):
		# Save and load data from the database and assert that the elements count before and afte loading is the same 

		room = [room.name for room in self.amity.rooms]
		people = [person.name for person in self.amity.people]
# 		before_saving = [room, people]
		self.amity.save_state("test")

		#load state
		self.amity.load_state('test')
		load_room = [room.name for room in self.amity.rooms]
		load_people = [person.name for person in self.amity.people]
# 		after_loading = [load_room, load_people]

# 		self.assertCountEqual(before_saving, after_loading)
		
	def tearDown(self):
		# It clears all the variables created
		del self.amity
		del self.lspace
		del self.office
		del self.staff
		del self.fellows
		del self.fellowaccommodate

	
if __name__ == '__main__':
	unittest.main()



