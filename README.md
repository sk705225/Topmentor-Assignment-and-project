# Financial Analytics Project Using Python Pandas

This is a simple beginner-friendly Financial Analytics project. It loads a financial CSV dataset, cleans the data, calculates important financial metrics, analyzes trends, and creates charts.

## Project Files

- `data/financial_data.csv` - sample financial dataset
- `financial_analytics.py` - main Python analysis file
- `charts/` - generated chart images
- `power_bi_guide.md` - Power BI visual and DAX instructions
- `requirements.txt` - Python libraries needed

## How To Run

Install the required libraries:

```bash
pip install -r requirements.txt
```

Run the project:

```bash
python financial_analytics.py
```

The script uses Matplotlib and Seaborn for charts. If they are not installed, it creates simple fallback charts using Pillow.

## Python Tasks Covered

- Load dataset from CSV
- Display first 5 rows
- Check dataset information
- Check missing values
- Remove duplicate records
- Clean the dataset
- Calculate total revenue, total expenses, total profit, and profit margin
- Analyze monthly revenue
- Analyze monthly profit
- Analyze yearly trend
- Create bar chart, line chart, pie chart, and histogram
- Write business insights

## Business Insights

1. Total revenue is higher than total expenses, so the business is profitable.
2. The profit margin shows how much profit is earned from every rupee of revenue.
3. Revenue grows steadily across the months, showing positive business momentum.
4. Monthly profit also improves, which means expenses are being managed reasonably well.
5. Sales department generates the highest revenue compared with other departments.
6. Marketing has lower revenue, so campaign performance should be reviewed regularly.
7. Operations has steady performance and supports consistent profit generation.
8. Yearly revenue increased from 2024 to 2025, showing business growth.
9. Expense growth should be monitored so profit margin does not fall in future months.
10. The company can focus on high-revenue regions and departments to improve profitability.

## Charts Created

- Bar Chart: Revenue by Department
- Line Chart: Monthly Profit Trend
- Pie Chart: Expenses by Region
- Histogram: Revenue Distribution

