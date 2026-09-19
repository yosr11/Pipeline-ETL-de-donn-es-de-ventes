import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

engine = create_engine(f"postgresql+psycopg2://postgres:{os.getenv('PG_PASSWORD', 'postgres')}@localhost:5432/sales_dw")
st.title("Dashboard des ventes")

monthly = pd.read_sql("SELECT make_date(year, month, 1) AS mois, total_sales FROM kpi_monthly_sales ORDER BY mois", engine)
st.subheader("Chiffre d'affaires par mois")
st.line_chart(monthly, x="mois", y="total_sales")

top = pd.read_sql("""SELECT p.product_name, SUM(f.sales) AS ca
                     FROM fact_sales f JOIN dim_product p USING (product_id)
                     GROUP BY p.product_name ORDER BY ca DESC LIMIT 10""", engine)
st.subheader("Top 10 produits")
st.bar_chart(top, x="product_name", y="ca")

region = pd.read_sql("SELECT region, SUM(sales) AS ca FROM fact_sales GROUP BY region ORDER BY ca DESC", engine)
st.subheader("Ventes par région")
st.bar_chart(region, x="region", y="ca")