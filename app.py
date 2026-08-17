import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Inventory Management System",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Inventory Management System")
st.write("Manage Products, Categories and Suppliers")


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_data(endpoint):
    """GET data from FastAPI."""
    try:
        response = requests.get(
            f"{API_URL}{endpoint}",
            timeout=5
        )

        if response.status_code == 200:
            return response.json()

        st.error(
            f"API Error {response.status_code}: {response.text}"
        )
        return []

    except requests.exceptions.ConnectionError:
        st.error(
            "❌ FastAPI backend is not running. "
            "Start it using: uvicorn main:app --reload"
        )
        return []

    except requests.exceptions.RequestException as e:
        st.error(f"Request error: {e}")
        return []


def post_data(endpoint, data):
    """POST data to FastAPI."""
    try:
        response = requests.post(
            f"{API_URL}{endpoint}",
            json=data,
            timeout=5
        )

        return response

    except requests.exceptions.ConnectionError:
        st.error(
            "❌ FastAPI backend is not running."
        )
        return None

    except requests.exceptions.RequestException as e:
        st.error(f"Request error: {e}")
        return None


def put_data(endpoint, data):
    """PUT data to FastAPI."""
    try:
        response = requests.put(
            f"{API_URL}{endpoint}",
            json=data,
            timeout=5
        )

        return response

    except requests.exceptions.ConnectionError:
        st.error(
            "❌ FastAPI backend is not running."
        )
        return None

    except requests.exceptions.RequestException as e:
        st.error(f"Request error: {e}")
        return None


def delete_data(endpoint):
    """DELETE data from FastAPI."""
    try:
        response = requests.delete(
            f"{API_URL}{endpoint}",
            timeout=5
        )

        return response

    except requests.exceptions.ConnectionError:
        st.error(
            "❌ FastAPI backend is not running."
        )
        return None

    except requests.exceptions.RequestException as e:
        st.error(f"Request error: {e}")
        return None


def show_response(response, success_message):
    """Display API response."""
    if response is None:
        return

    if 200 <= response.status_code < 300:
        try:
            result = response.json()

            if isinstance(result, dict) and "message" in result:
                st.success(result["message"])
            else:
                st.success(success_message)

        except ValueError:
            st.success(success_message)

    else:
        try:
            st.error(response.json())
        except ValueError:
            st.error(response.text)


# ============================================================
# SIDEBAR MENU
# ============================================================

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


# ============================================================
# DASHBOARD
# ============================================================

if menu == "Dashboard":

    st.subheader("📊 Dashboard")

    products = get_data("/products")
    categories = get_data("/categories")
    suppliers = get_data("/suppliers")

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    total_products = len(products)
    total_categories = len(categories)
    total_suppliers = len(suppliers)

    total_stock = sum(
        product.get("quantity", 0)
        for product in products
    )

    inventory_value = sum(
        product.get("price", 0) * product.get("quantity", 0)
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

    # --------------------------------------------------------
    # LOW STOCK ALERT
    # --------------------------------------------------------

    st.divider()

    st.subheader("⚠️ Low Stock Products")

    low_stock = [
        product
        for product in products
        if product.get("quantity", 0) < 5
    ]

    if low_stock:

        st.dataframe(
            pd.DataFrame(low_stock),
            use_container_width=True
        )

    else:

        st.success(
            "All products have sufficient stock."
        )

    # --------------------------------------------------------
    # INVENTORY CHART
    # --------------------------------------------------------

    st.divider()

    st.subheader("📊 Inventory Stock Chart")

    if products:

        df = pd.DataFrame(products)

        # Check required columns
        if "name" in df.columns and "quantity" in df.columns:

            fig = px.bar(
                df,
                x="name",
                y="quantity",
                title="Current Inventory Stock",
                labels={
                    "name": "Product",
                    "quantity": "Stock Quantity"
                }
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.warning(
                "Product data does not contain "
                "'name' and 'quantity' columns."
            )

    else:

        df = pd.DataFrame()

        st.info(
            "No products available. "
            "Add products to view the inventory chart."
        )

    # --------------------------------------------------------
    # CSV DOWNLOAD
    # --------------------------------------------------------

    st.divider()

    st.subheader("📥 Export Products")

    if not df.empty:

        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download Products CSV",
            data=csv,
            file_name="products.csv",
            mime="text/csv"
        )

    else:

        st.info(
            "No product data available for download."
        )

    # --------------------------------------------------------
    # PRODUCT TABLE
    # --------------------------------------------------------

    st.divider()

    st.subheader("📋 Product Inventory")

    if not df.empty:

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.info(
            "No products available."
        )


# ============================================================
# PRODUCTS
# ============================================================

elif menu == "Products":

    st.subheader("➕ Add Product")

    product_id = st.number_input(
        "Product ID",
        min_value=1,
        step=1,
        key="pid"
    )

    name = st.text_input(
        "Product Name",
        key="product_name"
    )

    price = st.number_input(
        "Price",
        min_value=0.0,
        step=0.01,
        key="product_price"
    )

    quantity = st.number_input(
        "Quantity",
        min_value=0,
        step=1,
        key="product_quantity"
    )

    category_id = st.number_input(
        "Category ID",
        min_value=1,
        step=1,
        key="product_category_id"
    )

    supplier_id = st.number_input(
        "Supplier ID",
        min_value=1,
        step=1,
        key="product_supplier_id"
    )

    if st.button(
        "Add Product",
        key="add_product"
    ):

        if not name.strip():

            st.warning(
                "Please enter a product name."
            )

        else:

            data = {
                "id": product_id,
                "name": name,
                "price": price,
                "quantity": quantity,
                "category_id": category_id,
                "supplier_id": supplier_id
            }

            response = post_data(
                "/products",
                data
            )

            show_response(
                response,
                "Product added successfully."
            )

    # --------------------------------------------------------
    # SEARCH PRODUCTS
    # --------------------------------------------------------

    st.divider()

    st.subheader("🔍 Search Product")

    products = get_data("/products")

    search = st.text_input(
        "Enter Product Name"
    )

    if products:

        if search:

            filtered = [
                product
                for product in products
                if search.lower()
                in product.get("name", "").lower()
            ]

            if filtered:

                st.dataframe(
                    pd.DataFrame(filtered),
                    use_container_width=True
                )

            else:

                st.info(
                    "No matching products found."
                )

        else:

            st.dataframe(
                pd.DataFrame(products),
                use_container_width=True
            )

    else:

        st.info(
            "No products available."
        )


# ============================================================
# CATEGORIES
# ============================================================

elif menu == "Categories":

    st.subheader("➕ Add Category")

    category_id = st.number_input(
        "Category ID",
        min_value=1,
        step=1,
        key="catid"
    )

    category_name = st.text_input(
        "Category Name",
        key="category_name"
    )

    if st.button(
        "Add Category",
        key="add_category"
    ):

        if not category_name.strip():

            st.warning(
                "Please enter a category name."
            )

        else:

            data = {
                "id": category_id,
                "name": category_name
            }

            response = post_data(
                "/categories",
                data
            )

            show_response(
                response,
                "Category added successfully."
            )

    # --------------------------------------------------------
    # CATEGORY LIST
    # --------------------------------------------------------

    st.divider()

    st.subheader("📋 Categories List")

    categories = get_data("/categories")

    if categories:

        st.dataframe(
            pd.DataFrame(categories),
            use_container_width=True
        )

    else:

        st.info(
            "No categories available."
        )


# ============================================================
# SUPPLIERS
# ============================================================

elif menu == "Suppliers":

    st.subheader("➕ Add Supplier")

    supplier_id = st.number_input(
        "Supplier ID",
        min_value=1,
        step=1,
        key="sid"
    )

    supplier_name = st.text_input(
        "Supplier Name",
        key="supplier_name"
    )

    phone = st.text_input(
        "Phone",
        key="supplier_phone"
    )

    email = st.text_input(
        "Email",
        key="supplier_email"
    )

    if st.button(
        "Add Supplier",
        key="add_supplier"
    ):

        if not supplier_name.strip():

            st.warning(
                "Please enter a supplier name."
            )

        else:

            data = {
                "id": supplier_id,
                "supplier_name": supplier_name,
                "phone": phone,
                "email": email
            }

            response = post_data(
                "/suppliers",
                data
            )

            show_response(
                response,
                "Supplier added successfully."
            )

    # --------------------------------------------------------
    # SUPPLIER LIST
    # --------------------------------------------------------

    st.divider()

    st.subheader("📋 Suppliers List")

    suppliers = get_data("/suppliers")

    if suppliers:

        st.dataframe(
            pd.DataFrame(suppliers),
            use_container_width=True
        )

    else:

        st.info(
            "No suppliers available."
        )


# ============================================================
# UPDATE PRODUCT
# ============================================================

elif menu == "Update Product":

    st.subheader("✏️ Update Product")

    product_id = st.number_input(
        "Product ID",
        min_value=1,
        step=1,
        key="update_id"
    )

    name = st.text_input(
        "Name",
        key="update_product_name"
    )

    price = st.number_input(
        "Price",
        min_value=0.0,
        step=0.01,
        key="update_product_price"
    )

    quantity = st.number_input(
        "Quantity",
        min_value=0,
        step=1,
        key="update_product_quantity"
    )

    category_id = st.number_input(
        "Category ID",
        min_value=1,
        step=1,
        key="update_product_category"
    )

    supplier_id = st.number_input(
        "Supplier ID",
        min_value=1,
        step=1,
        key="update_product_supplier"
    )

    if st.button(
        "Update Product",
        key="update_product_btn"
    ):

        data = {
            "id": product_id,
            "name": name,
            "price": price,
            "quantity": quantity,
            "category_id": category_id,
            "supplier_id": supplier_id
        }

        response = put_data(
            f"/products/{product_id}",
            data
        )

        show_response(
            response,
            "Product updated successfully."
        )


# ============================================================
# DELETE PRODUCT
# ============================================================

elif menu == "Delete Product":

    st.subheader("🗑️ Delete Product")

    product_id = st.number_input(
        "Product ID",
        min_value=1,
        step=1,
        key="delete_id"
    )

    if st.button(
        "Delete Product",
        key="delete_product_btn"
    ):

        response = delete_data(
            f"/products/{product_id}"
        )

        show_response(
            response,
            "Product deleted successfully."
        )


# ============================================================
# UPDATE CATEGORY
# ============================================================

elif menu == "Update Category":

    st.subheader("✏️ Update Category")

    category_id = st.number_input(
        "Category ID",
        min_value=1,
        step=1,
        key="update_cat_id"
    )

    category_name = st.text_input(
        "New Category Name",
        key="update_category_name"
    )

    if st.button(
        "Update Category",
        key="update_category_btn"
    ):

        data = {
            "id": category_id,
            "name": category_name
        }

        response = put_data(
            f"/categories/{category_id}",
            data
        )

        show_response(
            response,
            "Category updated successfully."
        )


# ============================================================
# DELETE CATEGORY
# ============================================================

elif menu == "Delete Category":

    st.subheader("🗑️ Delete Category")

    category_id = st.number_input(
        "Category ID",
        min_value=1,
        step=1,
        key="delete_cat_id"
    )

    if st.button(
        "Delete Category",
        key="delete_category_btn"
    ):

        response = delete_data(
            f"/categories/{category_id}"
        )

        show_response(
            response,
            "Category deleted successfully."
        )


# ============================================================
# UPDATE SUPPLIER
# ============================================================

elif menu == "Update Supplier":

    st.subheader("✏️ Update Supplier")

    supplier_id = st.number_input(
        "Supplier ID",
        min_value=1,
        step=1,
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

        response = put_data(
            f"/suppliers/{supplier_id}",
            data
        )

        show_response(
            response,
            "Supplier updated successfully."
        )


# ============================================================
# DELETE SUPPLIER
# ============================================================

elif menu == "Delete Supplier":

    st.subheader("🗑️ Delete Supplier")

    supplier_id = st.number_input(
        "Supplier ID",
        min_value=1,
        step=1,
        key="delete_supplier_id"
    )

    if st.button(
        "Delete Supplier",
        key="delete_supplier_btn"
    ):

        response = delete_data(
            f"/suppliers/{supplier_id}"
        )

        show_response(
            response,
            "Supplier deleted successfully."
        )