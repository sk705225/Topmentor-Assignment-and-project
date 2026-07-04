# Retail Analytics Project Using Python Pandas

This is a beginner-friendly Retail Analytics project. It loads a retail CSV dataset, cleans the data, calculates important business metrics, finds top products/customers, and creates simple charts.

## Project Files

- `data/retail_sales.csv` - sample retail dataset
- `retail_analytics.py` - main Python analysis file
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
python retail_analytics.py
```

The script uses Matplotlib and Seaborn for charts. If they are not installed, it creates simple fallback charts using Pillow.

## Python Tasks Covered

- Load dataset from CSV
- Display first 5 rows
- Check dataset information
- Check missing values
- Remove duplicate records
- Clean the data
- Calculate total sales, total profit, total orders, and total customers
- Find top 10 selling products
- Find top 10 customers
- Calculate sales by category
- Calculate sales by region
- Calculate monthly sales trend
- Create bar chart, line chart, pie chart, and histogram
- Write business insights

## Business Insights

1. Technology is the highest revenue category, mainly because laptops and smartphones have high order values.
2. Furniture gives steady sales, but its profit is lower than Technology.
3. Office Supplies has high quantity sold, but lower revenue because individual item prices are small.
4. Laptop and Smartphone are among the top selling products by sales value.
5. The North and East regions are strong contributors to total sales.
6. A few repeat customers generate high sales, so loyalty programs can help retain them.
7. Sales increase in the last quarter, showing possible festive or year-end demand.
8. High-value products create most of the profit, so stock planning should focus on those items.
9. Low-cost items like notebooks and pens help increase order volume and customer engagement.
10. Regional sales comparison can help the company plan targeted marketing campaigns.

## Charts Created

- Bar Chart: Sales by Category
- Line Chart: Monthly Sales Trend
- Pie Chart: Sales by Region
- Histogram: Sales Distribution
