from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, models
from ..repository import blog as blog_repository
import blog

get_db = database.get_db

router = APIRouter(
    prefix='/blogs',
    tags=['Blogs']
)

@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    return blog_repository.get_all(db)

@router.get('/{id}', response_model=schemas.ShowBlog)
def get(id: int, db: Session = Depends(get_db)):
    return blog_repository.get_by_id(id, db)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    return blog_repository.create(request, db)

@router.put('/', status_code=status.HTTP_202_ACCEPTED)  
def put(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    return blog_repository.update_by_id(id, request, db)

@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)  
def delete(id: int, db: Session = Depends(get_db)):
    return blog_repository.delete_by_id(id, db)

