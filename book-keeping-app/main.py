from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import engine, get_db
from models import Base, Book as BookModel, Review as ReviewModel
from schemas import BookCreate, Book, ReviewCreate, Review
from util import generate_random_id
import logging

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def default_route():
    return "Hello, Welcome to Intelligent Book Management System"

@app.post("/books", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    book_id = generate_random_id()
    db_book = BookModel(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books", response_model=List[Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = db.query(BookModel).offset(skip).limit(limit).all()
    return books

@app.get("/books/{id}", response_model=Book)
def read_book(id: int, db: Session = Depends(get_db)):
    book = db.query(BookModel).filter(BookModel.id == id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{id}", response_model=Book)
def update_book(id: int, book: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(BookModel).filter(BookModel.id == id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.delete("/books/{id}", response_model=Book)
def delete_book(id: int, db: Session = Depends(get_db)):
    db_book = db.query(BookModel).filter(BookModel.id == id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return db_book

@app.post("/books/{id}/reviews", response_model=Review)
def create_review(id: int, review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = ReviewModel(**review.dict(), book_id=id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@app.get("/books/{id}/reviews", response_model=List[Review])
def read_reviews(id: int, db: Session = Depends(get_db)):
    reviews = db.query(ReviewModel).filter(ReviewModel.book_id == id).all()
    return reviews

@app.get("/books/{id}/summary")
def get_book_summary(id: int, db: Session = Depends(get_db)):
    book = db.query(BookModel).filter(BookModel.id == id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    reviews = db.query(ReviewModel).filter(ReviewModel.book_id == id).all()
    rating_sum = sum(review.rating for review in reviews)
    rating_count = len(reviews)
    avg_rating = rating_sum / rating_count if rating_count > 0 else None
    return {"summary": book.summary, "average_rating": avg_rating}