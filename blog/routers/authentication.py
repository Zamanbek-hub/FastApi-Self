from datetime import timedelta

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, models, hashing, token

get_db = database.get_db

router = APIRouter(
    tags=["Authentication"]
)

@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email==request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f'Incorrect username')

    if not hashing.Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f'Incorrect password')
 
    access_token = token.create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}