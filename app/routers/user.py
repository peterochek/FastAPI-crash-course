from typing import List

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import models, schemas, utils
from app.database import get_db

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash_(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/', response_model=List[schemas.UserOut])
def get_post(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'users were not found')
    return users


@router.get('/{id_}', response_model=schemas.UserOut)
def get_post(id_: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id_).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id = {id_} was not found')
    return user
