from pydantic import BaseModel

class ProductCreate(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    category_id: int
    supplier_id: int

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    id: int
    name: str

class SupplierCreate(BaseModel):
    id: int
    supplier_name: str
    phone: str
    email: str