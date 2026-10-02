# Week 4 Capstone: Sales Analysis
Files: Capstone_Report.pdf (explanation report), Financial_Sample_Capstone_Report.xlsx (Excel), code/ (notebook, scripts, SQL), data/, figures/, powerbi_data/.
Run: put Sample_data.csv beside the notebook (or use ../data), then run all cells in code/Capstone_Analysis.ipynb.

## Build the Power BI dashboard (about 10 minutes)
1. Power BI Desktop > Get data > Text/CSV > powerbi_data/clean_data.csv > Load.
2. Add a Card visual: Sales (Sum), then another for Profit (Sum).
3. Add New measure: Profit Margin = DIVIDE(SUM(clean_data[Profit]), SUM(clean_data[Sales])). Add as a Card.
4. Line chart: Axis = Date, Values = Sales and Profit.
5. Clustered bar chart: Axis = Segment, Values = Sales. Repeat with Country and Product.
6. Column chart: Axis = Discount Band, Values = Discount Rate (Average).
7. Add Slicers for Year, Segment and Country (these are the filters the course asks for).
8. Add a text box titled "Key insights" with the findings from the report. File > Save as Capstone.pbix.
