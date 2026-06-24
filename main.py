from fastapi import FastAPI
from schemas import CategoryCreate
from models import Category
from schemas import SupplierCreate
from models import Supplier

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Inventory Management System FASTAPI"
    }

#CREATE Product
from fastapi import HTTPException
from database import SessionLocal
from models import Product
from schemas import ProductCreate


@app.post("/products")
def create_product(product: ProductCreate):

    db = SessionLocal()

    existing = db.query(Product).filter(
        Product.id == product.id
    ).first()

    if existing:
        db.close()
        raise HTTPException(
            status_code=400,
            detail="Product already exists"
        )

    new_product = Product(
        id=product.id,
        name=product.name,
        price=product.price,
        quantity=product.quantity,
        category_id=product.category_id,
        supplier_id=product.supplier_id
    )

    db.add(new_product)
    db.commit()

    db.close()

    return {
        "message": "Product Added Successfully"
    }

#READ ALL Products
@app.get("/products")
def get_products():

    db = SessionLocal()

    products = db.query(Product).all()

    db.close()

    return products

#READ ONE Product
@app.get("/products/{product_id}")
def get_product(product_id: int):

    db = SessionLocal()

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    db.close()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product

#UPDATE Product
@app.put("/products/{product_id}")
def update_product(
    product_id: int,
    updated_data: ProductCreate
):

    db = SessionLocal()

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.name = updated_data.name
    product.price = updated_data.price
    product.quantity = updated_data.quantity
    product.category_id = updated_data.category_id
    product.supplier_id = updated_data.supplier_id

    db.commit()

    db.close()

    return {
        "message": "Product Updated Successfully"
    }

#DELETE Product
@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    db = SessionLocal()

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    db.close()

    return {
        "message": "Product Deleted Successfully"
    }

from sqlalchemy import text

@app.get("/debug")
def debug():

    db = SessionLocal()

    categories = db.execute(
        text("SELECT * FROM categories")
    ).fetchall()

    suppliers = db.execute(
        text("SELECT * FROM suppliers")
    ).fetchall()

    products = db.execute(
        text("SELECT * FROM products")
    ).fetchall()

    db.close()

    return {
        "categories": str(categories),
        "suppliers": str(suppliers),
        "products": str(products)
    }

#Create Category
@app.post("/categories")
def create_category(category: CategoryCreate):

    db = SessionLocal()

    existing = db.query(Category).filter(
        Category.id == category.id
    ).first()

    if existing:
        db.close()
        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )

    new_category = Category(
        id=category.id,
        name=category.name
    )

    db.add(new_category)
    db.commit()

    db.close()

    return {
        "message": "Category Created Successfully"
    }

#Get Categories
@app.get("/categories")
def get_categories():

    db = SessionLocal()

    categories = db.query(Category).all()

    db.close()

    return categories

#Create Supplier
@app.post("/suppliers")
def create_supplier(supplier: SupplierCreate):

    db = SessionLocal()

    existing = db.query(Supplier).filter(
        Supplier.id == supplier.id
    ).first()

    if existing:
        db.close()
        raise HTTPException(
            status_code=400,
            detail="Supplier already exists"
        )

    new_supplier = Supplier(
        id=supplier.id,
        supplier_name=supplier.supplier_name,
        phone=supplier.phone,
        email=supplier.email
    )

    db.add(new_supplier)
    db.commit()

    db.close()

    return {
        "message": "Supplier Created Successfully"
    }

#Get Suppliers

@app.get("/suppliers")
def get_suppliers():

    db = SessionLocal()

    suppliers = db.query(Supplier).all()

    db.close()

    return suppliers

@app.put("/categories/{category_id}")
def update_category(
    category_id: int,
    updated_data: CategoryCreate
):

    db = SessionLocal()

    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not category:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    category.name = updated_data.name

    db.commit()
    db.close()

    return {
        "message": "Category Updated Successfully"
    }

@app.delete("/categories/{category_id}")
def delete_category(category_id: int):

    db = SessionLocal()

    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not category:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    db.delete(category)
    db.commit()

    db.close()

    return {
        "message": "Category Deleted Successfully"
    }

@app.put("/suppliers/{supplier_id}")
def update_supplier(
    supplier_id: int,
    updated_data: SupplierCreate
):

    db = SessionLocal()

    supplier = db.query(Supplier).filter(
        Supplier.id == supplier_id
    ).first()

    if not supplier:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Supplier not found"
        )

    supplier.supplier_name = updated_data.supplier_name
    supplier.phone = updated_data.phone
    supplier.email = updated_data.email

    db.commit()
    db.close()

    return {
        "message": "Supplier Updated Successfully"
    }

@app.delete("/suppliers/{supplier_id}")
def delete_supplier(supplier_id: int):

    db = SessionLocal()

    supplier = db.query(Supplier).filter(
        Supplier.id == supplier_id
    ).first()

    if not supplier:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Supplier not found"
        )

    db.delete(supplier)
    db.commit()

    db.close()

    return {
        "message": "Supplier Deleted Successfully"
    }

