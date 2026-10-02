import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

df = pd.read_csv('/home/claude/work/clean_data.csv')

# Features that are legitimately known BEFORE a sale happens (no leakage from Sales itself)
cat_features = ['Segment', 'Country', 'Product', 'Discount Band']
num_features = ['Units Sold', 'Sale Price', 'Manufacturing Price', 'Month Number']
target = 'Sales'

X = df[cat_features + num_features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

preprocess = ColumnTransformer([
    ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features),
], remainder='passthrough')

results = {}

for name, model in [('Linear Regression', LinearRegression()),
                     ('Random Forest', RandomForestRegressor(n_estimators=200, random_state=42))]:
    pipe = Pipeline([('prep', preprocess), ('model', model)])
    pipe.fit(X_train, y_train)
    pred = pipe.predict(X_test)
    r2 = r2_score(y_test, pred)
    mae = mean_absolute_error(y_test, pred)
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    results[name] = {'r2': r2, 'mae': mae, 'rmse': rmse, 'pipe': pipe, 'pred': pred}
    print(f"{name}: R2={r2:.4f}  MAE={mae:,.0f}  RMSE={rmse:,.0f}")

# Pick best model by R2
best_name = max(results, key=lambda k: results[k]['r2'])
best = results[best_name]
print(f"\nBest model: {best_name}")

# Actual vs Predicted plot
plt.figure(figsize=(6,6))
plt.scatter(y_test, best['pred'], alpha=0.5, color='#2E5B8A')
lims = [0, max(y_test.max(), best['pred'].max())]
plt.plot(lims, lims, 'r--')
plt.xlabel('Actual Sales')
plt.ylabel('Predicted Sales')
plt.title(f'Actual vs Predicted Sales ({best_name})')
plt.tight_layout()
plt.savefig('/home/claude/work/figs/actual_vs_predicted.png', dpi=140)
plt.close()

# Feature importance (Random Forest) if applicable
if 'Random Forest' in results:
    rf_pipe = results['Random Forest']['pipe']
    ohe = rf_pipe.named_steps['prep'].named_transformers_['cat']
    cat_names = list(ohe.get_feature_names_out(cat_features))
    all_names = cat_names + num_features
    importances = rf_pipe.named_steps['model'].feature_importances_
    imp_df = pd.DataFrame({'feature': all_names, 'importance': importances}).sort_values('importance', ascending=False).head(12)
    plt.figure(figsize=(7,5))
    plt.barh(imp_df['feature'][::-1], imp_df['importance'][::-1], color='#B8860B')
    plt.title('Top Feature Importances (Random Forest)')
    plt.tight_layout()
    plt.savefig('/home/claude/work/figs/feature_importance.png', dpi=140)
    plt.close()
    imp_df.to_csv('/home/claude/work/feature_importance.csv', index=False)

# Save model results summary
summary_rows = []
for name, r in results.items():
    summary_rows.append({'Model': name, 'R2': r['r2'], 'MAE': r['mae'], 'RMSE': r['rmse']})
pd.DataFrame(summary_rows).to_csv('/home/claude/work/model_results.csv', index=False)

# Save predictions sample for report
sample = X_test.copy()
sample['Actual Sales'] = y_test.values
sample['Predicted Sales'] = best['pred']
sample.head(20).to_csv('/home/claude/work/predictions_sample.csv', index=False)

print("\nDone.")
