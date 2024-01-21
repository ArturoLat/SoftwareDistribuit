from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic.tools import lru_cache
from sqlalchemy.orm import Session

from src import utils, models, repository
from jose import jwt
from pydantic import ValidationError

from src.database import get_db
from src.schemas import TokenPayload, SystemAccount


@lru_cache()
def get_settings():
    return utils.Settings()


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


def get_user_by_username(db: Session, username: str):
    user = db.query(models.Account).filter(models.Account.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


async def get_current_user(token: str = Depends(reuseable_oauth), db: Session = Depends(get_db),
                           settings: utils.Settings = Depends(get_settings)) -> SystemAccount:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.algorithm]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username: str = token_data.sub
    # get user from database
    db_account = repository.get_account_by_name(db, username)
    # if user does not exist, raise an exception
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    # if user exist, return user Schema with password hashed
    else:
        return db_account
