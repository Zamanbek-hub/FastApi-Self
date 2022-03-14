from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from blog import schemas
from .. import models, hashing

def get_by_id(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id==id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f'User with this id = {id} is not available')

    return user

def create(request: schemas.User, db: Session):
    new_user = models.User(
        name=request.name, 
        email=request.email, 
        password=hashing.Hash.bcrypt(request.password))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
