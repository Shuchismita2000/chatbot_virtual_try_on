from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Define the database engine (SQLite for this example)
engine = create_engine('sqlite:///whatsapp_bot.db', echo=True)

# Define the base class for declarative models
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    phone_number = Column(String, unique=True, nullable=False)
    current_step = Column(String, default="start")
    person_image_url = Column(String, nullable=True)
    garment_image_url = Column(String, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create the tables in the database
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)

def get_session():
    """Return a new session instance."""
    return Session()
