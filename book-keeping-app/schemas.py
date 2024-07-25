from pydantic import BaseModel
from typing import List, Optional

class ReviewBase(BaseModel):
    user_id: int
    review_text: Optional[str] = None
    rating: int

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    book_id: int

    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str
    author: str
    genre: Optional[str] = None
    year_published: Optional[int] = None
    summary: Optional[str] = None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    reviews: List[Review] = []

    class Config:
        orm_mode = True
