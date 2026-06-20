# 📦 Inventory Management System

## 🚀 Project Overview

The Inventory Management System is a full-stack web application built using FastAPI, Streamlit, PostgreSQL, SQLAlchemy, and Pydantic.

This project helps businesses manage:

- Products
- Categories
- Suppliers
- Inventory Stock

Users can perform CRUD operations, monitor inventory levels, visualize stock data, and export inventory information.

---

# 🎯 Features

## Product Management

- Add Product
- View Products
- Search Product by Name
- Update Product
- Delete Product

## Category Management

- Add Category
- View Categories
- Update Category
- Delete Category

## Supplier Management

- Add Supplier
- View Suppliers
- Update Supplier
- Delete Supplier

## Dashboard

- Total Products
- Total Categories
- Total Suppliers
- Total Stock
- Inventory Value

## Inventory Monitoring

- Low Stock Alerts
- Inventory Stock Visualization
- CSV Export

---

# 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| FastAPI | Backend API |
| Streamlit | Frontend UI |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Pydantic | Data Validation |
| Swagger UI | API Testing |
| Pandas | Data Analysis |
| Plotly | Data Visualization |
| Requests | API Communication |

---

# 🏗️ Project Architecture

```text
User
 ↓
Streamlit Frontend
 ↓
Requests Library
 ↓
FastAPI Backend
 ↓
Pydantic Validation
 ↓
SQLAlchemy ORM
 ↓
PostgreSQL Database
```

---

# 📂 Project Structure

```text
inventory-management-system/
│
├── app.py
├── main.py
├── database.py
├── models.py
├── schemas.py
├── requirements.txt
├── README.md
│
└── screenshots/
```

---

# 🗄️ Database Design

## Categories Table

| Column | Type |
|----------|------|
| id | Integer |
| name | String |

---

## Suppliers Table

| Column | Type |
|----------|------|
| id | Integer |
| supplier_name | String |
| phone | String |
| email | String |

---

## Products Table

| Column | Type |
|----------|------|
| id | Integer |
| name | String |
| price | Float |
| quantity | Integer |
| category_id | Foreign Key |
| supplier_id | Foreign Key |

---

# 🔗 Database Relationships

```text
Category
   |
   └── Products

Supplier
   |
   └── Products
```

A Product belongs to:

- One Category
- One Supplier

---

# ⚙️ Step-by-Step Development Process

## Phase 1: Database Setup

Created PostgreSQL database:

```sql
CREATE DATABASE inventory_db;
```

Connected PostgreSQL with FastAPI using SQLAlchemy.

---

## Phase 2: Database Models

Created:

- Product Model
- Category Model
- Supplier Model

Implemented Foreign Key relationships.

---

## Phase 3: Pydantic Schemas

Created validation schemas:

- ProductCreate
- CategoryCreate
- SupplierCreate

Used for request validation.

---

## Phase 4: FastAPI Backend

Implemented Product CRUD APIs.

### Product Endpoints

```http
POST    /products
GET     /products
GET     /products/{id}
PUT     /products/{id}
DELETE  /products/{id}
```

---

Implemented Category CRUD APIs.

### Category Endpoints

```http
POST    /categories
GET     /categories
PUT     /categories/{id}
DELETE  /categories/{id}
```

---

Implemented Supplier CRUD APIs.

### Supplier Endpoints

```http
POST    /suppliers
GET     /suppliers
PUT     /suppliers/{id}
DELETE  /suppliers/{id}
```

---

## Phase 5: Swagger Testing

Used Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Tested all APIs.

Verified:

- Product CRUD
- Category CRUD
- Supplier CRUD

---

## Phase 6: Streamlit Frontend

Created user-friendly interface.

Pages:

- Dashboard
- Products
- Categories
- Suppliers
- Update Product
- Delete Product
- Update Category
- Delete Category
- Update Supplier
- Delete Supplier

---

## Phase 7: Dashboard Development

Implemented:

### Metrics

- Total Products
- Total Categories
- Total Suppliers
- Total Stock
- Inventory Value

---

### Low Stock Alert

Displays products with quantity less than 5.

---

### Inventory Chart

Used Plotly bar charts to visualize stock levels.

---

### CSV Export

Allows downloading inventory data.

---

## Phase 8: Search Functionality

Implemented product search by name.

Example:

```text
Mobile
Laptop
Keyboard
```

Search results update dynamically.

---

# ▶️ Installation Guide

## Clone Repository

```bash
git clone https://github.com/your-username/inventory-management-system.git
```

---

## Create Virtual Environment

```bash
python -m venv project
```

Activate:

### Windows

```bash
project\Scripts\activate
```

### Mac/Linux

```bash
source project/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Start PostgreSQL

Ensure PostgreSQL server is running.

---

## Run FastAPI

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

## Run Streamlit

```bash
streamlit run app.py
```

---

# 📊 Sample Dashboard Metrics

```text
Products          : 3
Categories        : 3
Suppliers         : 3
Total Stock       : 92
Inventory Value   : ₹90,00,600
```

---

# 🔮 Future Enhancements

- User Authentication
- Role-Based Access Control
- Purchase Orders
- Sales Tracking
- Inventory Forecasting
- Email Notifications
- Cloud Deployment

---

# 👨‍💻 Author

Ravi Guna

Built using:

FastAPI + Streamlit + PostgreSQL + SQLAlchemy + Pydantic