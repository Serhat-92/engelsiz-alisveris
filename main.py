from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
import shutil
import os

# --- VERİTABANI KÜTÜPHANELERİ ---
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI()

# --- AYARLAR ---
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- 1. VERİTABANI BAĞLANTISI (SQLITE) ---
# Bu komut, klasöründe 'market.db' adında bir dosya oluşturur.
SQLALCHEMY_DATABASE_URL = "sqlite:///./market.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- 2. VERİTABANI TABLO MODELLERİ (TASARIMA UYGUN) ---
class ProductDB(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    barcode = Column(String, unique=True, index=True)
    name = Column(String)
    price = Column(Float)
    weight = Column(String)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)

class FavoriteDB(Base):
    __tablename__ = "favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    product_barcode = Column(String) # Basitlik için direkt barkodu tutuyoruz

# Veritabanını oluştur (Tabloları yarat)
Base.metadata.create_all(bind=engine)

# --- 3. PYDANTIC MODELLERİ (VERİ ALIŞVERİŞİ İÇİN) ---
class ProductCreate(BaseModel):
    name: str
    price: float
    barcode: str
    weight: str
    description: Optional[str] = None
    image_url: Optional[str] = None

class ProductResponse(ProductCreate):
    id: int
    class Config:
        orm_mode = True

# --- YARDIMCI: Veritabanı Oturumu Açma ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Engelsiz Market - SQL Veritabanlı Sürüm 🗄️"}

# --- 4. YENİ ÜRÜN EKLEME (Admin Paneli İçin) ---
@app.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # Barkod var mı kontrol et
    existing_product = db.query(ProductDB).filter(ProductDB.barcode == product.barcode).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Bu barkod zaten kayıtlı!")
    
    # Yeni ürünü veritabanına kaydet
    db_product = ProductDB(
        name=product.name, 
        price=product.price, 
        barcode=product.barcode, 
        weight=product.weight,
        description=product.description,
        image_url=product.image_url
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# --- 5. ÜRÜN SORGULAMA ---
@app.get("/product/{barcode_id}")
def get_product(barcode_id: str, db: Session = Depends(get_db)):
    product = db.query(ProductDB).filter(ProductDB.barcode == barcode_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    return product

# --- 6. SEPET SİSTEMİ DÜZELTİLMİŞ HALİ ---
shopping_cart = []

@app.post("/cart/add/{barcode_id}")
def add_to_cart(barcode_id: str, db: Session = Depends(get_db)):
    product = db.query(ProductDB).filter(ProductDB.barcode == barcode_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Ürün yok")
    
    
    cart_item = {
        "name": product.name,
        "price": product.price,
        "barcode": product.barcode,
        "image_url": product.image_url
    }
    
    shopping_cart.append(cart_item)
    return {"message": f"{product.name} sepete eklendi", "cart_size": len(shopping_cart)}

@app.get("/cart")
def view_cart():
    total = sum(item["price"] for item in shopping_cart)
    return {"items": shopping_cart, "total": total}

# --- 7. FAVORİLER (VERİTABANINA KAYITLI) ---
@app.post("/favorites/add/{barcode_id}")
def add_favorite(barcode_id: str, db: Session = Depends(get_db)):
    # Ürün geçerli mi?
    product = db.query(ProductDB).filter(ProductDB.barcode == barcode_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    
    # Zaten favoride mi?
    exists = db.query(FavoriteDB).filter(FavoriteDB.product_barcode == barcode_id).first()
    if exists:
        return {"message": "Zaten favorilerde ekli"}

    new_fav = FavoriteDB(product_barcode=barcode_id)
    db.add(new_fav)
    db.commit()
    return {"message": f"{product.name} veritabanına favori olarak kaydedildi ❤️"}

@app.get("/favorites")
def get_favorites(db: Session = Depends(get_db)):
    favs = db.query(FavoriteDB).all()
    results = []
    for fav in favs:
        prod = db.query(ProductDB).filter(ProductDB.barcode == fav.product_barcode).first()
        if prod:
            results.append(prod)
    
    return results  

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    file_location = f"static/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    return {"info": "Resim yüklendi", "url": f"http://127.0.0.1:8000/static/{file.filename}"}