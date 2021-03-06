from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from blog import schemas
from .. import models

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(request: schemas.Blog, db: Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

def get_by_id(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()

    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f'Blog with this id = {id} is not available')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with this id = {id} is not available'}

    return blog

def update_by_id(id: int, request: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f'Blog with this id = {id} is not available')

    blog.update(request.dict())
    db.commit()

    return "updated"

def delete_by_id(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id==id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f'Blog with this id = {id} is not available')

    blog.delete(synchronize_session=False)
    db.commit()

    return "done"