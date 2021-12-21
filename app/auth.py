from fastapi import status, Depends, APIRouter, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, oauth2, schemas
from app.database import get_db
from app.utils import verify

router = APIRouter(
    prefix='/login',
    tags=['Auth']
)


@router.post('/', response_model=schemas.Token)
def create_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Incorrect Credentials')

    if not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Incorrect Credentials',
        )

    access_token = oauth2.create_access_token(data={'user_id': user.id})

    return {'access_token': access_token, 'token_type': 'bearer'}
