from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(String(8), primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String)
    year_published = Column(Integer)
    summary = Column(Text)
    reviews = relationship("Review", back_populates="book")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    review_text = Column(Text)
    rating = Column(Integer)
    book = relationship("Book", back_populates="reviews")
