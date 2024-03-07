from fastapi import APIRouter, Depends, status, HTTPException
from ..database import get_db
from .. import schemas, database, models
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from . import seller
SECRET_KEY = "fe0f4062f0f1193c19b068b370a8ba86138189d340bc9bee7e15b6c35822cb03"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter(
    tags=["Login"]
)

def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    seller = db.query(models.Seller).filter(models.Seller.username == request.username).first()
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    
    if not pwd_context.verify(request.password, seller.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Password", header={"WWW-Authenticate": "Bearer"})
    # Generate JWT Token for the User
    access_token = generate_token(
        data = {"sub": seller.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}
    # return request

def get_current_user(token: str = Depends(oauth2_scheme)):
    cred_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            pass
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise cred_exception