from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.product import Product
from app.schemas.product import Product as ProductSchema, ProductCreate

router = APIRouter()

@router.get("/", response_model=List[ProductSchema])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Tüm ürünleri listele.
    """
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@router.get("/{barcode}", response_model=ProductSchema)
def read_product_by_barcode(barcode: str, db: Session = Depends(get_db)):
    """
    Barkoda göre ürün bul. Görüntü işleme sonrası bu endpoint çağrılacak.
    """
    product = db.query(Product).filter(Product.barcode == barcode).first()
    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    return product

@router.post("/", response_model=ProductSchema)
def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    """
    Yeni ürün ekle.
    """
    # Barkod kontrolü
    if product_in.barcode:
        existing_product = db.query(Product).filter(Product.barcode == product_in.barcode).first()
        if existing_product:
            raise HTTPException(status_code=400, detail="Bu barkod zaten kayıtlı")

    db_product = Product(**product_in.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
