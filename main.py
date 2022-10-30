
#importing required libraries fro fast api , databse and models

from ctypes import addressof
from typing import Counter
from uuid import UUID
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from uuid import UUID
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

#creating a class for our address book so we can execute it ======

class address_book(BaseModel):
    name: str = Field(min_length=1)
    father_name: str = Field(min_length=1)
    contact: str = Field(min_length=10)
    address: str = Field(min_length=1, max_length=100)

BOOKS = []

#creating read table in our address book==========

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    return db.query(models.Books).all()

# creating post table in our address book=========

@app.post("/")
def create_book(book: address_book, db: Session = Depends(get_db)):
    book_model = models.Books()
    book_model.name = book.name
    book_model.father_name = book.father_name
    book_model.concat = book.contact
    book_model.address = book.address

    db.add(book_model)
    db.commit()
    return book

# coding for updating of our address book databse

@app.put("/{book_id}")
def update_book(book_id: int, book: address_book, db: Session = Depends(get_db)):
    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()

    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {book_id} : Does not exist"
        )

    book_model.name = book.name
    book_model.father_name = book.father_name
    book_model.concat = book.contact
    book_model.address = book.address

    db.add(book_model)
    db.commit()

    return book

# coding for deleting specific data from our data base of address book====

@app.delete("/{book_id}")
def delete_book(book_id: int, db:Session = Depends(get_db)):

    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()

    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {book_id} : does bot exist"
        )

    db.query(models.Books).filter(models.Books.id == book_id).delete()

    db.commit()