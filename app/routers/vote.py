from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, oauth2, models
from ..database import get_db

router = APIRouter(prefix="/vote", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {vote.post_id} does not exists",
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id
    )
    found_vote = vote_query.first()

    if vote:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"vote for user with id {current_user.id} and post with id {vote.post_id} already exists",
            )
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()

        return {"message": "successfully added post"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote does not exist",
            )

        vote_query.delete()
        db.commit()

        return {"message": "successfully deleted post"}
