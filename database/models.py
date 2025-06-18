import os
from sqlalchemy import create_engine, FLOAT, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())


engine = create_engine(url=os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Books(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=True)
    author: Mapped[str] = mapped_column(String(128), nullable=True)
    rating: Mapped[float] = mapped_column(FLOAT, nullable=True, default=0)
    publisher: Mapped[str] = mapped_column(String(32), nullable=True)
    publication_year: Mapped[int]  = mapped_column(Integer, nullable=True)
    isbn: Mapped[str] = mapped_column(String(64), nullable=True)

Base.metadata.create_all(bind=engine)