# Sales Analysis Capstone

Data analysis project on a financial sales dataset — exploratory data analysis (EDA), a regression model to predict sales, and an interactive Power BI dashboard.

## Dataset

**Financial Sample** (`Sample_data.csv` / `clean_data.csv`) — 700 transactions from September 2013 to December 2014, covering 5 customer segments, 5 countries, and 6 products.

Columns: `Segment`, `Country`, `Product`, `Discount Band`, `Units Sold`, `Manufacturing Price`, `Sale Price`, `Gross Sales`, `Discounts`, `Sales`, `COGS`, `Profit`, `Date`, `Month Number`, `Month Name`, `Year`.

## Files in this repo

| File | Description |
|---|---|
| `Sample_data.csv` | Raw source data |
| `clean_data.csv` | Cleaned data (used by the notebook and the Power BI dashboard) |
| `Capstone_Analysis.ipynb` | Main EDA + regression analysis notebook |
| `eda.py` | EDA as a standalone script |
| `model.py` | Regression model as a standalone script |
| `sql_analysis.py` | SQL (SQLite) version of key queries |
| `power_bi_analysis.pbix` | Power BI dashboard |
| `Capstone_Report.pdf` | Findings & recommendations write-up |
| `Financial_Sample_Capstone_Report.xlsx` | Excel workbook (tables + charts) |
| `requirements.txt` | Python dependencies |

## Key results

- **Total sales:** $118.7M · **Total profit:** $16.9M · **Overall margin:** 14.2%
- **Government** is the largest segment — 44% of sales ($52.5M) at a 22% margin.
- **Enterprise** is loss-making overall: -$614K profit on $19.6M in sales (58 of its deals lost money).
- **Channel Partners** has the smallest volume but the best margin, at ~73%.
- Heavy discounting erodes profit: the High discount band averages ~12.5% off vs. ~2.4% for Low.
- Sales peak in October (both years), and again in June and December 2014.
- **Paseo** is the top-selling product ($33.0M); **Amarilla** has the best product margin (15.9%).

### Regression model — predicting Sales

Predicts `Sales` from variables known before a deal closes (units, price, segment, country, product, discount band, month). `Gross Sales`, `Discounts` and `COGS` are deliberately excluded as predictors because they are algebraically derived from `Sales` and would leak the answer.

| Model | R² | MAE | RMSE |
|---|---|---|---|
| Linear Regression | 0.76 | $82,989 | $114,708 |
| **Random Forest** | **0.98** | **$11,154** | **$30,031** |

## How to run

1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Open `Capstone_Analysis.ipynb` and run all cells (it reads `Sample_data.csv` from the same folder).
3. To view the dashboard, open `power_bi_analysis.pbix` in Power BI Desktop.

## How the Power BI dashboard was built

1. Power BI Desktop > Get data > Text/CSV > `clean_data.csv` > Load.
2. Add Card visuals: Sales (Sum), Profit (Sum), Units Sold (Sum).
3. New measure: `Profit Margin = DIVIDE(SUM(clean_data[Profit]), SUM(clean_data[Sales]))`. Add as a Card, formatted as a percentage.
4. Line chart: X-axis = Year, then Month Number (in that order). Values = Sales and Profit.
5. Clustered bar charts: Y-axis = Segment (then repeat for Country and Product), X-axis = Sales.
6. Column chart: X-axis = Discount Band, Y-axis = Discount Rate (set to Average, not Sum).
7. Slicers for Year, Segment and Country.
8. Text box titled "Key Insights" with the findings below.

## Recommendations

1. Protect and grow the Government relationship — it's the revenue anchor.
2. Investigate Enterprise pricing/discounting to fix its negative margin.
3. Consider scaling Channel Partners — its margin suggests an efficient, under-invested channel.
4. Require approval for discounts above the Medium band.
5. Plan inventory, staffing and marketing around the October/June/December peaks.
6. Use the Random Forest model for pipeline revenue forecasting from planned units and pricing.

## Author

Data Analyst Course — Week 4 Capstone Project
