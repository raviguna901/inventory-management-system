import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Inventory Management System",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Inventory Management System")
st.write("Manage Products, Categories and Suppliers")

menu = st.sidebar.selectbox(
    "Select Option",
    [
        
    "Dashboard",
    "Products",
    "Categories",
    "Suppliers",
    "Update Product",
    "Delete Product",
    "Update Category",
    "Delete Category",
    "Update Supplier",
    "Delete Supplier"

    ]
)

# ---------------- DASHBOARD ---------------- #

if menu == "Dashboard":

    st.subheader("📊 Dashboard")

    products = requests.get(
        f"{API_URL}/products"
    ).json()

    categories = requests.get(
        f"{API_URL}/categories"
    ).json()

    suppliers = requests.get(
        f"{API_URL}/suppliers"
    ).json()

    total_products = len(products)

    total_categories = len(categories)

    total_suppliers = len(suppliers)

    total_stock = sum(
        product["quantity"]
        for product in products
    )

    inventory_value = sum(
        product["price"] * product["quantity"]
        for product in products
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Products",
        total_products
    )

    col2.metric(
        "Categories",
        total_categories
    )

    col3.metric(
        "Suppliers",
        total_suppliers
    )

    col4.metric(
        "Total Stock",
        total_stock
    )

    col5.metric(
        "Inventory Value",
        f"₹{inventory_value:,.0f}"
    )

    # ---------------- LOW STOCK ALERT ---------------- #

    st.divider()

    st.subheader("⚠️ Low Stock Products")

    low_stock = [
        product
        for product in products
        if product["quantity"] < 5
    ]

    if low_stock:
        st.dataframe(low_stock)
    else:
        st.success(
            "All products have sufficient stock"
        )

    # ---------------- INVENTORY CHART ---------------- #

    st.divider()

    st.subheader("📊 Inventory Stock Chart")

    df = pd.DataFrame(products)

    fig = px.bar(
        df,
        x="name",
        y="quantity",
        title="Current Inventory Stock"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ---------------- CSV DOWNLOAD ---------------- #

    st.divider()

    st.subheader("📥 Export Products")

    csv = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Products CSV",
        data=csv,
        file_name="products.csv",
        mime="text/csv"
    )

    # ---------------- PRODUCTS TABLE ---------------- #

    st.divider()

    st.subheader("📋 Product Inventory")

    st.dataframe(df)

# ---------------- PRODUCTS ---------------- #

elif menu == "Products":

    st.subheader("➕ Add Product")

    product_id = st.number_input(
        "Product ID",
        min_value=1,
        key="pid"
    )

    name = st.text_input(
        "Product Name"
    )

    price = st.number_input(
        "Price",
        min_value=0.0
    )

    quantity = st.number_input(
        "Quantity",
        min_value=0
    )

    category_id = st.number_input(
        "Category ID",
        min_value=1
    )

    supplier_id = st.number_input(
        "Supplier ID",
        min_value=1
    )

    if st.button(
        "Add Product",
        key="add_product"
    ):

        data = {
            "id": product_id,
            "name": name,
            "price": price,
            "quantity": quantity,
            "category_id": category_id,
            "supplier_id": supplier_id
        }

        response = requests.post(
            f"{API_URL}/products",
            json=data
        )

        st.success(response.json())

    st.divider()

    st.subheader("🔍 Search Product")

    products = requests.get(
        f"{API_URL}/products"
    ).json()

    search = st.text_input(
        "Enter Product Name"
    )

    if search:

        filtered = [
            product
            for product in products
            if search.lower()
            in product["name"].lower()
        ]

        st.dataframe(
            pd.DataFrame(filtered)
        )

    else:

        st.dataframe(
            pd.DataFrame(products)
        )

# ---------------- CATEGORIES ---------------- #

elif menu == "Categories":

    st.subheader("➕ Add Category")

    category_id = st.number_input(
        "Category ID",
        min_value=1,
        key="catid"
    )

    category_name = st.text_input(
        "Category Name"
    )

    if st.button(
        "Add Category",
        key="add_category"
    ):

        data = {
            "id": category_id,
            "name": category_name
        }

        response = requests.post(
            f"{API_URL}/categories",
            json=data
        )

        st.success(response.json())

    st.divider()

    st.subheader("📋 Categories List")

    categories = requests.get(
        f"{API_URL}/categories"
    ).json()

    st.dataframe(
        pd.DataFrame(categories)
    )

# ---------------- SUPPLIERS ---------------- #

elif menu == "Suppliers":

    st.subheader("➕ Add Supplier")

    supplier_id = st.number_input(
        "Supplier ID",
        min_value=1,
        key="sid"
    )

    supplier_name = st.text_input(
        "Supplier Name"
    )

    phone = st.text_input(
        "Phone"
    )

    email = st.text_input(
        "Email"
    )

    if st.button(
        "Add Supplier",
        key="add_supplier"
    ):

        data = {
            "id": supplier_id,
            "supplier_name": supplier_name,
            "phone": phone,
            "email": email
        }

        response = requests.post(
            f"{API_URL}/suppliers",
            json=data
        )

        if response.status_code == 200:
            st.success("Operation Successful")
        else:
            st.error(response.text)

    st.divider()

    st.subheader("📋 Suppliers List")

    suppliers = requests.get(
        f"{API_URL}/suppliers"
    ).json()

    st.dataframe(
        pd.DataFrame(suppliers)
    )
elif menu == "Delete Product":

    st.subheader("🗑️ Delete Product")

    product_id = st.number_input(
        "Product ID",
        min_value=1,
        key="delete_id"
    )

    if st.button("Delete Product"):

        response = requests.delete(
            f"{API_URL}/products/{product_id}"
        )

        st.success(response.json())

elif menu == "Update Product":

    st.subheader("✏️ Update Product")

    product_id = st.number_input(
        "Product ID",
        min_value=1,
        key="update_id"
    )

    name = st.text_input("Name")
    price = st.number_input(
        "Price",
        min_value=0.0
    )

    quantity = st.number_input(
        "Quantity",
        min_value=0
    )

    category_id = st.number_input(
        "Category ID",
        min_value=1
    )

    supplier_id = st.number_input(
        "Supplier ID",
        min_value=1
    )

    if st.button(
        "Update Product"
    ):

        data = {
            "id": product_id,
            "name": name,
            "price": price,
            "quantity": quantity,
            "category_id": category_id,
            "supplier_id": supplier_id
        }

        response = requests.put(
            f"{API_URL}/products/{product_id}",
            json=data
        )

        st.success(
            response.json()
        )

# ---------------- UPDATE CATEGORY ---------------- #

elif menu == "Update Category":

    st.subheader("✏️ Update Category")

    category_id = st.number_input(
        "Category ID",
        min_value=1,
        key="update_cat_id"
    )

    category_name = st.text_input(
        "New Category Name"
    )

    if st.button(
        "Update Category",
        key="update_category_btn"
    ):

        data = {
            "id": category_id,
            "name": category_name
        }

        response = requests.put(
            f"{API_URL}/categories/{category_id}",
            json=data
        )

        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error(response.json())

# ---------------- DELETE CATEGORY ---------------- #

elif menu == "Delete Category":

    st.subheader("🗑️ Delete Category")

    category_id = st.number_input(
        "Category ID",
        min_value=1,
        key="delete_cat_id"
    )

    if st.button(
        "Delete Category",
        key="delete_category_btn"
    ):

        response = requests.delete(
            f"{API_URL}/categories/{category_id}"
        )

        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error(response.json())

# ---------------- UPDATE SUPPLIER ---------------- #

elif menu == "Update Supplier":

    st.subheader("✏️ Update Supplier")

    supplier_id = st.number_input(
        "Supplier ID",
        min_value=1,
        key="update_supplier_id"
    )

    supplier_name = st.text_input(
        "Supplier Name",
        key="update_supplier_name"
    )

    phone = st.text_input(
        "Phone",
        key="update_supplier_phone"
    )

    email = st.text_input(
        "Email",
        key="update_supplier_email"
    )

    if st.button(
        "Update Supplier",
        key="update_supplier_btn"
    ):

        data = {
            "id": supplier_id,
            "supplier_name": supplier_name,
            "phone": phone,
            "email": email
        }

        response = requests.put(
            f"{API_URL}/suppliers/{supplier_id}",
            json=data
        )

        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error(response.json())

# ---------------- DELETE SUPPLIER ---------------- #

elif menu == "Delete Supplier":

    st.subheader("🗑️ Delete Supplier")

    supplier_id = st.number_input(
        "Supplier ID",
        min_value=1,
        key="delete_supplier_id"
    )

    if st.button(
        "Delete Supplier",
        key="delete_supplier_btn"
    ):

        response = requests.delete(
            f"{API_URL}/suppliers/{supplier_id}"
        )

        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error(response.json())