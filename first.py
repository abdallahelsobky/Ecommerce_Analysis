import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


df = pd.read_excel(r"ecommerce_orders.xlsx")
pd.set_option('display.max_rows',None )
pd.set_option('display.max_columns',None)
pd.set_option('display.width' , None)

print(df.shape)
print(df.info())

print(df.describe(include='all').T)
print(df.nunique())

df.columns = df.columns.str.strip().str.lower()
print(df['product'])

text_cols = [
    "customer_name", "order_id", "product","category","payment_method", "status"
]

for col in text_cols:
    df[col] = df[col].astype(str).str.strip()
    df[col] = df[col].replace(["nan", "None", ""], np.nan)
    df[col] = df[col].str.title()
    print(df)

df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
#print(df["order_date"])

df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").astype("Int64")
#print(df["quantity"])


df["category"] = df["category"].astype(str).str.strip()
df["category"].replace(["", "nan", "None"], np.nan, inplace=True)
df = df.dropna(subset=["category"])


df['price'] = pd.to_numeric(df['price'], errors='coerce')

df['price'] = df.groupby("product")["price"].transform( lambda x: x.fillna(x.median()))
df['price'] = df["price"].fillna(df["price"].median())
df= df.dropna(subset=['order_date', 'quantity'])
print(df)


############### total sales column إجمالي المبيعات كلها 
df["total"] = (df["price"] * df["quantity"]).round(2)
#print(df)





############## top products  أفضل المنتجات مبيعا حسب عدد القطع
print(df.groupby("product")["quantity"].sum().sort_values(ascending=False).head())


####################### top revenue أعلى المنتجات تحقيقا للربح
print(df.groupby("product")["total"].sum().sort_values(ascending=False).head())


############ daily sales
daily_sales = df.groupby("order_date")["total"].sum()
daily_sales.plot()
plt.title("Daily Sales")
plt.show()


######## monthly sales
monthly_sales = df.groupby(df["order_date"].dt.to_period("M"))["total"].sum()
monthly_sales.plot()
plt.title("Monthly Sales")
plt.show()

############ category sales
df.groupby("category")["total"].sum().plot(kind="bar")
plt.title("Category Sales ")
plt.show()

