from sqlalchemy import Column, Integer, String, DateTime

from .db import engine, Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    birthday = Column(DateTime)
    additional_data = Column(String, nullable=True)


Base.metadata.create_all(bind=engine)
