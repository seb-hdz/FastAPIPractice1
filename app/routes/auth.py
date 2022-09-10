from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from ..database import get_db
from .. import schemas, models, utils, oauth2

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
# // def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        # // .filter(models.User.email == user_credentials.email)
        .filter(models.User.email == user_credentials.username).first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid credentials",
        )

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid credentials",
        )

    token = oauth2.create_token(data={"user_id": user.id})

    return {"token": token, "token_type": "bearer"}
