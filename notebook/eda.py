import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')

df = pd.read_csv('/mnt/user-data/uploads/Sample_data__1__xlsx_-_Sheet1.csv')
df.columns = [c.strip() for c in df.columns]

# Clean
df['Discount Band'] = df['Discount Band'].fillna('None')
df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y')
df['Discount Rate'] = np.where(df['Gross Sales'] > 0, df['Discounts'] / df['Gross Sales'], 0)
df['Profit Margin'] = np.where(df['Sales'] > 0, df['Profit'] / df['Sales'], 0)

# ---- Summary tables ----
seg_summary = df.groupby('Segment').agg(
    Total_Sales=('Sales', 'sum'),
    Total_Profit=('Profit', 'sum'),
    Avg_Margin=('Profit Margin', 'mean'),
    Units_Sold=('Units Sold', 'sum'),
    Orders=('Sales', 'count')
).sort_values('Total_Sales', ascending=False)

country_summary = df.groupby('Country').agg(
    Total_Sales=('Sales', 'sum'),
    Total_Profit=('Profit', 'sum'),
    Avg_Margin=('Profit Margin', 'mean')
).sort_values('Total_Sales', ascending=False)

product_summary = df.groupby('Product').agg(
    Total_Sales=('Sales', 'sum'),
    Total_Profit=('Profit', 'sum'),
    Units_Sold=('Units Sold', 'sum'),
    Avg_Margin=('Profit Margin', 'mean')
).sort_values('Total_Sales', ascending=False)

discount_summary = df.groupby('Discount Band').agg(
    Total_Sales=('Sales', 'sum'),
    Total_Profit=('Profit', 'sum'),
    Avg_Discount_Rate=('Discount Rate', 'mean')
).sort_values('Total_Sales', ascending=False)

monthly = df.groupby(df['Date'].dt.to_period('M')).agg(
    Total_Sales=('Sales', 'sum'),
    Total_Profit=('Profit', 'sum')
).reset_index()
monthly['Date'] = monthly['Date'].astype(str)

print("=== SEGMENT SUMMARY ===")
print(seg_summary)
print("\n=== COUNTRY SUMMARY ===")
print(country_summary)
print("\n=== PRODUCT SUMMARY ===")
print(product_summary)
print("\n=== DISCOUNT BAND SUMMARY ===")
print(discount_summary)
print("\nOverall Total Sales:", df['Sales'].sum())
print("Overall Total Profit:", df['Profit'].sum())
print("Overall Avg Margin:", df['Profit Margin'].mean())
print("Correlation with Sales:")
num_cols = ['Units Sold','Manufacturing Price','Sale Price','Gross Sales','Discounts','Sales','COGS','Profit','Discount Rate']
print(df[num_cols].corr()['Sales'].sort_values(ascending=False))

# Save tables for later use (Excel + report)
seg_summary.to_csv('/home/claude/work/seg_summary.csv')
country_summary.to_csv('/home/claude/work/country_summary.csv')
product_summary.to_csv('/home/claude/work/product_summary.csv')
discount_summary.to_csv('/home/claude/work/discount_summary.csv')
monthly.to_csv('/home/claude/work/monthly.csv', index=False)
df.to_csv('/home/claude/work/clean_data.csv', index=False)

# ---- Charts ----
# 1. Sales by segment
plt.figure(figsize=(7,4.5))
seg_summary['Total_Sales'].sort_values().plot(kind='barh', color='#2E5B8A')
plt.title('Total Sales by Segment')
plt.xlabel('Sales ($)')
plt.tight_layout()
plt.savefig('/home/claude/work/figs/sales_by_segment.png', dpi=140)
plt.close()

# 2. Sales by country
plt.figure(figsize=(7,4.5))
country_summary['Total_Sales'].sort_values().plot(kind='barh', color='#3F8F5E')
plt.title('Total Sales by Country')
plt.xlabel('Sales ($)')
plt.tight_layout()
plt.savefig('/home/claude/work/figs/sales_by_country.png', dpi=140)
plt.close()

# 3. Sales by product
plt.figure(figsize=(7,4.5))
product_summary['Total_Sales'].sort_values().plot(kind='barh', color='#B8860B')
plt.title('Total Sales by Product')
plt.xlabel('Sales ($)')
plt.tight_layout()
plt.savefig('/home/claude/work/figs/sales_by_product.png', dpi=140)
plt.close()

# 4. Monthly trend
plt.figure(figsize=(8,4.5))
plt.plot(monthly['Date'], monthly['Total_Sales'], marker='o', color='#2E5B8A', label='Sales')
plt.plot(monthly['Date'], monthly['Total_Profit'], marker='o', color='#B8860B', label='Profit')
plt.xticks(rotation=60)
plt.title('Monthly Sales & Profit Trend')
plt.ylabel('$')
plt.legend()
plt.tight_layout()
plt.savefig('/home/claude/work/figs/monthly_trend.png', dpi=140)
plt.close()

# 5. Discount band impact on margin
plt.figure(figsize=(6,4.5))
discount_summary['Avg_Discount_Rate'].plot(kind='bar', color='#8A2E2E')
plt.title('Average Discount Rate by Discount Band')
plt.ylabel('Discount Rate')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('/home/claude/work/figs/discount_rate.png', dpi=140)
plt.close()

# 6. Correlation heatmap
plt.figure(figsize=(7,5.5))
sns.heatmap(df[num_cols].corr(), annot=True, fmt='.2f', cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.savefig('/home/claude/work/figs/correlation_heatmap.png', dpi=140)
plt.close()

# 7. Units Sold vs Sales scatter
plt.figure(figsize=(6,4.5))
plt.scatter(df['Units Sold'], df['Sales'], alpha=0.4, color='#2E5B8A')
plt.title('Units Sold vs Sales')
plt.xlabel('Units Sold')
plt.ylabel('Sales ($)')
plt.tight_layout()
plt.savefig('/home/claude/work/figs/units_vs_sales.png', dpi=140)
plt.close()

print("\nCharts saved.")
