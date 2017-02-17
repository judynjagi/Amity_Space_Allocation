from sqlalchemy import Column,Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class PeopleModel(Base):
	__tablename__ = 'people'
	# id = Column(Integer, , autoincrement = True)
	name = Column(String(250), primary_key = True, nullable=False)
	role = Column(String(250), nullable=False)
	accomodate = Column(String(250), nullable=False)
	living_space = Column(Integer(), ForeignKey('living_space.lspace_name'))
	office = Column(Integer(), ForeignKey('offices.office_name'))

class LivingSpaceModel(Base):
	__tablename__ = 'living_space'
	lspace_name = Column(String(250), primary_key = True)
	occupants = Column(String(250))
	room_type = Column(String(100), nullable=False)
	max_capacity =Column(Integer)

class OfficeModel(Base):
	__tablename__ = 'offices'
	office_name = Column(String(250), primary_key = True)
	occupants = Column(String(250))
	room_type = Column(String(100), nullable=False)
	max_capacity =Column(Integer)

def create_db(db_name):
	directory = 'databases/'
	engine = create_engine('sqlite:///' + directory + db_name)
	Base.metadata.create_all(engine)
	return engine