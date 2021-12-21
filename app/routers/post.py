from typing import Optional

from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app import models, schemas, oauth2
from app.database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('/', response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              current_user: schemas.UserOut = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')). \
        join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id). \
        filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


@router.get('/latest', response_model=schemas.PostOut)
def get_latest_post(db: Session = Depends(get_db)):
    latest = db.query(models.Post, func.count(models.Vote.post_id).label('votes')). \
        join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id). \
        order_by(desc(models.Post.created_at)).first()
    return latest


@router.get('/{id_}', response_model=schemas.PostOut)
def get_post(id_: int, db: Session = Depends(get_db),
             current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')). \
        join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id). \
        filter(models.Post.id == id_).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id = {id_} was not found')
    return post


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete('/{id_}')
def delete_post(id_: int, db: Session = Depends(get_db),
                current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id_)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'no post for deleting with id = {id_}')
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized to perform this operation',
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id_}', response_model=schemas.Post)
def update_post(id_: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id_)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'no post for updating with id = {id_}')
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized to perform this operation',
        )

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
