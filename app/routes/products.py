from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.config.database import db
from bson import ObjectId
import shutil
import os

router = APIRouter(prefix="/products", tags=["products"])

UPLOAD_DIR = "uploads/"

# Create a product
@router.post("/", response_model=dict)
async def create_product(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    image: UploadFile = File(...),
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Save image to uploads folder
    image_path = os.path.join(UPLOAD_DIR, image.filename)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    product = {
        "name": name,
        "description": description,
        "price": price,
        "image_url": image_path,
    }
    result = db.products.insert_one(product)
    product["_id"] = str(result.inserted_id)
    return {"message": "Product created", "product": product}

# Get all products
@router.get("/", response_model=list[dict])
async def get_products():
    products = list(db.products.find())
    for p in products:
        p["id"] = str(p["_id"])
    return products

# Update a product
@router.put("/{product_id}", response_model=dict)
async def update_product(product_id: str, update: dict, current_user=Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    result = db.products.update_one({"_id": ObjectId(product_id)}, {"$set": update})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product updated"}

# Delete a product
@router.delete("/{product_id}", response_model=dict)
async def delete_product(product_id: str, current_user=Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    result = db.products.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}
