from fastapi import APIRouter
from app.api.v1.endpoints import products

api_router = APIRouter()

# Router'ları buraya ekleyeceğiz
api_router.include_router(products.router, prefix="/products", tags=["products"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
