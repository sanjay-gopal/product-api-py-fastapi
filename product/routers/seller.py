
from passlib.context import CryptContext
from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi.params import Depends
from .. import schemas, models
from ..database import get_db
router = APIRouter(
    tags=["Sellers"],
    prefix="/seller"
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/", response_model=schemas.DisplaySeller)
def create_seller(request: schemas.Seller, db: Session = Depends(get_db)):
    hash_password = pwd_context.hash(request.password)
    new_seller = models.Seller(username=request.username, email=request.email, password=hash_password)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return request