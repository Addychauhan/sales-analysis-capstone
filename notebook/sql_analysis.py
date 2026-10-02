import sqlite3, pandas as pd
df = pd.read_csv('../data/Sample_data.csv'); df.columns=[c.strip() for c in df.columns]
con = sqlite3.connect(':memory:'); df.to_sql('sales', con, index=False)
q = {
 'By segment': 'SELECT Segment, ROUND(SUM(Sales)) sales, ROUND(SUM(Profit)) profit, ROUND(SUM(Profit)/SUM(Sales),3) margin FROM sales GROUP BY Segment ORDER BY sales DESC',
 'By product': 'SELECT Product, ROUND(SUM(Sales)) sales, ROUND(SUM(Profit)) profit FROM sales GROUP BY Product ORDER BY sales DESC',
 'Loss-making deals by segment': 'SELECT Segment, COUNT(*) loss_deals FROM sales WHERE Profit<0 GROUP BY Segment',
}
for k,v in q.items(): print('\n==',k); print(pd.read_sql(v,con))
