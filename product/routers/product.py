from fastapi import APIRouter, status, Response, HTTPException
from sqlalchemy.orm import Session
from fastapi.params import Depends
from typing import List
from ..database import get_db
from ..import models
from ..import schemas, models
from .login import get_current_user
router = APIRouter(
    tags=["Products"],
    prefix="/product"
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def add(request: schemas.Product, db: Session = Depends(get_db)):
    add_product = models.Product(name=request.name, description=request.description, price=request.price, seller_id=1)
    db.add(add_product)
    db.commit()
    db.refresh(add_product)
    return request

@router.get("/", response_model=List[schemas.DisplayProduct])
def get_products(db: Session = Depends(get_db), current_user: schemas.Seller = Depends(get_current_user)):
    products = db.query(models.Product).all()
    return products

@router.get("/{id}", response_model=schemas.DisplayProduct)
def get_product_by_id(id, response: Response, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found!")
        # response.status_code = status.HTTP_404_NOT_FOUND
    return product

@router.delete("/{id}")
def delete_product(id, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return db

@router.put("/{id}")
def update_product(id, request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        pass
    product.update(request.dict())
    db.commit()
    # return product
    return {"response": "Product update successfully!"}