from sqlalchemy import Column, Integer, String, Text, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Подключение к базе данных
engine = create_engine('postgresql://postgres:s4v77Am@localhost/movies')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    imdb_rating = Column(Float)
    year = Column(Integer)
    poster_url = Column(String, nullable=False)
    local_image_path = Column(String, nullable=True)

# Создание таблиц
Base.metadata.create_all(bind=engine)
