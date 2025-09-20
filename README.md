# EDA Dashboard

An interactive Streamlit dashboard to explore `financial_transactions.csv`.

## Quickstart

1. Create a virtual environment (recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

## Features
- Load and cache the dataset
- Interactive filters (date range, category, merchant, payment method, account type)
- KPIs (total amount, number of transactions, average amount)
- Visualizations: time series, category breakdown, merchant top N, payment method share, weekday-hour heatmap
- Optional: simple outlier detection

## File Structure
```
app.py
src/
  __init__.py
  data.py
  viz.py
  outliers.py
financial_transactions.csv
requirements.txt
```

## Notes
- Place `financial_transactions.csv` in the project root.
- Python 3.10+ recommended.

