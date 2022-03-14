from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, database
from ..repository import user as user_repository

get_db = database.get_db

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return user_repository.get_by_id(id, db)
 
@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user_repository.create(request, db)