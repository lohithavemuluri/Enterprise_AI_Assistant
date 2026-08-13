import sqlite3
import pandas as pd
import streamlit as st


DATABASE = "enterprise.db"


def load_data():

    connection = sqlite3.connect(DATABASE)

    sales = pd.read_sql_query(
        """
        SELECT
            sales.id,
            products.product_name,
            employees.name AS employee_name,
            employees.department,
            sales.quantity,
            sales.sale_amount,
            sales.sale_date
        FROM sales
        JOIN products
            ON sales.product_id = products.id
        JOIN employees
            ON sales.employee_id = employees.id
        """,
        connection
    )

    connection.close()

    return sales


def show_dashboard():

    st.header("📊 Enterprise Dashboard")

    data = load_data()

    # -----------------------------------------
    # KPI VALUES
    # -----------------------------------------

    total_sales = data["sale_amount"].sum()

    total_quantity = data["quantity"].sum()

    total_employees = data["employee_name"].nunique()

    total_products = data["product_name"].nunique()


    # -----------------------------------------
    # KPI CARDS
    # -----------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💰 Total Sales",
            f"₹{total_sales:,.0f}"
        )

    with col2:
        st.metric(
            "📦 Units Sold",
            f"{total_quantity:,}"
        )

    with col3:
        st.metric(
            "👥 Employees",
            total_employees
        )

    with col4:
        st.metric(
            "🛍️ Products",
            total_products
        )


    st.divider()


    # -----------------------------------------
    # SALES BY PRODUCT
    # -----------------------------------------

    st.subheader("📈 Sales by Product")

    product_sales = (
        data
        .groupby("product_name")["sale_amount"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(product_sales)


    # -----------------------------------------
    # SALES BY DEPARTMENT
    # -----------------------------------------

    st.subheader("🏢 Sales by Department")

    department_sales = (
        data
        .groupby("department")["sale_amount"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(department_sales)


    # -----------------------------------------
    # SALES TREND
    # -----------------------------------------

    st.subheader("📅 Sales Trend")

    data["sale_date"] = pd.to_datetime(
        data["sale_date"]
    )

    daily_sales = (
        data
        .groupby("sale_date")["sale_amount"]
        .sum()
    )

    st.line_chart(daily_sales)


    # -----------------------------------------
    # SALES DATA
    # -----------------------------------------

    st.subheader("📋 Sales Data")

    st.dataframe(
        data,
        use_container_width=True
    )