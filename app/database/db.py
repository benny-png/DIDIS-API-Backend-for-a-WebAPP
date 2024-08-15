from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    bank_account_name = Column(String)
    bank_account_number = Column(String)
    email = Column(String)
    institution = Column(String)
    registration_number = Column(String)
    last_yos = Column(String)
    photo_path = Column(String)

Base.metadata.create_all(bind=engine)