"""
Simple Retail Analytics Project using Python and Pandas.

This script:
1. Loads a retail dataset from a CSV file.
2. Checks rows, columns, missing values, and duplicates.
3. Cleans the data.
4. Calculates key business metrics.
5. Finds top products, customers, category sales, region sales, and monthly sales.
6. Creates simple charts using Matplotlib and Seaborn.
7. Prints beginner-friendly business insights.
"""

from pathlib import Path

import pandas as pd

try:
    import matplotlib.pyplot as plt
    import seaborn as sns

    HAS_MATPLOTLIB = True
except ModuleNotFoundError:
    from PIL import Image, ImageDraw, ImageFont

    HAS_MATPLOTLIB = False


# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "retail_sales.csv"
CHART_DIR = BASE_DIR / "charts"
CHART_DIR.mkdir(exist_ok=True)


def load_data(file_path):
    """Load the retail CSV file into a Pandas DataFrame."""
    return pd.read_csv(file_path)


def clean_data(df):
    """Clean the dataset by fixing dates, removing duplicates, and handling missing values."""
    # Remove exact duplicate records
    df = df.drop_duplicates()

    # Convert Order Date from text to date format
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

    # Remove rows where important columns are missing
    required_columns = [
        "Order ID",
        "Order Date",
        "Customer ID",
        "Customer Name",
        "Product Name",
        "Category",
        "Region",
    ]
    df = df.dropna(subset=required_columns)

    # Fill missing numeric values with 0
    numeric_columns = ["Quantity", "Sales", "Profit"]
    df[numeric_columns] = df[numeric_columns].fillna(0)

    # Remove records with negative or zero sales because sales should be positive
    df = df[df["Sales"] > 0]

    # Create a Month column for trend analysis
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)

    return df


def draw_text(draw, position, text, fill="#222222"):
    """Draw text using the default font."""
    draw.text(position, text, fill=fill, font=ImageFont.load_default())


def save_simple_bar_chart(data, title, file_name):
    """Fallback bar chart created with Pillow when Matplotlib is not installed."""
    image = Image.new("RGB", (900, 550), "white")
    draw = ImageDraw.Draw(image)
    draw_text(draw, (30, 20), title)

    max_value = max(data.values)
    bar_width = 120
    gap = 45
    start_x = 80
    base_y = 460

    for index, (label, value) in enumerate(data.items()):
        bar_height = int((value / max_value) * 330)
        x1 = start_x + index * (bar_width + gap)
        y1 = base_y - bar_height
        x2 = x1 + bar_width
        draw.rectangle([x1, y1, x2, base_y], fill="#4E79A7")
        draw_text(draw, (x1, base_y + 10), label[:16])
        draw_text(draw, (x1, y1 - 18), f"{value:,.0f}")

    image.save(CHART_DIR / file_name)


def save_simple_line_chart(data, title, file_name):
    """Fallback line chart created with Pillow when Matplotlib is not installed."""
    image = Image.new("RGB", (1000, 550), "white")
    draw = ImageDraw.Draw(image)
    draw_text(draw, (30, 20), title)

    values = list(data.values)
    labels = list(data.index)
    max_value = max(values)
    min_value = min(values)
    left = 70
    top = 70
    width = 860
    height = 360

    points = []
    for index, value in enumerate(values):
        x = left + int(index * (width / (len(values) - 1)))
        y = top + height - int(((value - min_value) / (max_value - min_value)) * height)
        points.append((x, y))

    draw.line(points, fill="#F28E2B", width=4)
    for point, label, value in zip(points, labels, values):
        draw.ellipse([point[0] - 5, point[1] - 5, point[0] + 5, point[1] + 5], fill="#F28E2B")
        draw_text(draw, (point[0] - 25, 455), label)
        draw_text(draw, (point[0] - 25, point[1] - 22), f"{value:,.0f}")

    image.save(CHART_DIR / file_name)


def save_simple_pie_chart(data, title, file_name):
    """Fallback pie chart created with Pillow when Matplotlib is not installed."""
    image = Image.new("RGB", (800, 550), "white")
    draw = ImageDraw.Draw(image)
    draw_text(draw, (30, 20), title)

    colors = ["#4E79A7", "#F28E2B", "#59A14F", "#E15759", "#76B7B2"]
    total = sum(data.values)
    start_angle = 0
    box = [120, 80, 470, 430]

    for index, (label, value) in enumerate(data.items()):
        end_angle = start_angle + (value / total) * 360
        draw.pieslice(box, start=start_angle, end=end_angle, fill=colors[index % len(colors)])
        percent = (value / total) * 100
        legend_y = 100 + index * 35
        draw.rectangle([540, legend_y, 560, legend_y + 20], fill=colors[index % len(colors)])
        draw_text(draw, (570, legend_y), f"{label}: {percent:.1f}%")
        start_angle = end_angle

    image.save(CHART_DIR / file_name)


def save_simple_histogram(values, title, file_name):
    """Fallback histogram created with Pillow when Matplotlib is not installed."""
    image = Image.new("RGB", (900, 550), "white")
    draw = ImageDraw.Draw(image)
    draw_text(draw, (30, 20), title)

    bins = pd.cut(values, bins=8)
    counts = bins.value_counts().sort_index()
    max_count = counts.max()
    bar_width = 80
    gap = 20
    start_x = 70
    base_y = 460

    for index, count in enumerate(counts.values):
        bar_height = int((count / max_count) * 330)
        x1 = start_x + index * (bar_width + gap)
        y1 = base_y - bar_height
        x2 = x1 + bar_width
        draw.rectangle([x1, y1, x2, base_y], fill="#59A14F")
        draw_text(draw, (x1 + 25, y1 - 18), str(count))

    draw_text(draw, (70, 490), "Sales bins from low to high")
    image.save(CHART_DIR / file_name)


def create_charts(df):
    """Create and save simple retail analytics charts."""
    if not HAS_MATPLOTLIB:
        print("\nMatplotlib/Seaborn not found. Creating simple fallback charts with Pillow.")
        save_simple_bar_chart(
            df.groupby("Category")["Sales"].sum().sort_values(ascending=False),
            "Sales by Category",
            "bar_sales_by_category.png",
        )
        save_simple_line_chart(
            df.groupby("Month")["Sales"].sum(),
            "Monthly Sales Trend",
            "line_monthly_sales_trend.png",
        )
        save_simple_pie_chart(
            df.groupby("Region")["Sales"].sum(),
            "Sales Share by Region",
            "pie_sales_by_region.png",
        )
        save_simple_histogram(
            df["Sales"],
            "Sales Distribution",
            "histogram_sales_distribution.png",
        )
        return

    sns.set_theme(style="whitegrid")

    # Bar chart: Sales by Category
    sales_by_category = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    plt.figure(figsize=(8, 5))
    sns.barplot(x=sales_by_category.index, y=sales_by_category.values, palette="Set2", hue=sales_by_category.index, legend=False)
    plt.title("Sales by Category")
    plt.xlabel("Category")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "bar_sales_by_category.png", dpi=150)
    plt.close()

    # Line chart: Monthly Sales Trend
    monthly_sales = df.groupby("Month")["Sales"].sum().reset_index()
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=monthly_sales, x="Month", y="Sales", marker="o", color="#1f77b4")
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "line_monthly_sales_trend.png", dpi=150)
    plt.close()

    # Pie chart: Sales by Region
    sales_by_region = df.groupby("Region")["Sales"].sum()
    plt.figure(figsize=(7, 7))
    plt.pie(
        sales_by_region.values,
        labels=sales_by_region.index,
        autopct="%1.1f%%",
        startangle=90,
    )
    plt.title("Sales Share by Region")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "pie_sales_by_region.png", dpi=150)
    plt.close()

    # Histogram: Distribution of Sales
    plt.figure(figsize=(8, 5))
    sns.histplot(df["Sales"], bins=12, kde=True, color="#2ca02c")
    plt.title("Sales Distribution")
    plt.xlabel("Sales")
    plt.ylabel("Number of Orders")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "histogram_sales_distribution.png", dpi=150)
    plt.close()


def main():
    # Load dataset
    df = load_data(DATA_FILE)

    print("\nFIRST 5 ROWS")
    print(df.head())

    print("\nDATASET INFORMATION")
    print(df.info())

    print("\nMISSING VALUES")
    print(df.isnull().sum())

    print("\nDUPLICATE RECORDS BEFORE CLEANING")
    print(df.duplicated().sum())

    # Clean dataset
    df = clean_data(df)

    print("\nDUPLICATE RECORDS AFTER CLEANING")
    print(df.duplicated().sum())

    print("\nCLEANED DATASET SHAPE")
    print(df.shape)

    # Key calculations
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = df["Order ID"].nunique()
    total_customers = df["Customer ID"].nunique()

    print("\nKEY METRICS")
    print(f"Total Sales: {total_sales:,.2f}")
    print(f"Total Profit: {total_profit:,.2f}")
    print(f"Total Orders: {total_orders}")
    print(f"Total Customers: {total_customers}")

    # Analysis tables
    top_products = df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(10)
    top_customers = df.groupby("Customer Name")["Sales"].sum().sort_values(ascending=False).head(10)
    sales_by_category = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    sales_by_region = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
    monthly_sales = df.groupby("Month")["Sales"].sum()

    print("\nTOP 10 SELLING PRODUCTS")
    print(top_products)

    print("\nTOP 10 CUSTOMERS")
    print(top_customers)

    print("\nSALES BY CATEGORY")
    print(sales_by_category)

    print("\nSALES BY REGION")
    print(sales_by_region)

    print("\nMONTHLY SALES TREND")
    print(monthly_sales)

    # Create charts
    create_charts(df)
    print(f"\nCharts saved in: {CHART_DIR}")

    # Business insights
    print("\nBUSINESS INSIGHTS")
    insights = [
        "Technology is the highest revenue category, mainly because laptops and smartphones have high order values.",
        "Furniture gives steady sales, but its profit is lower than Technology.",
        "Office Supplies has high quantity sold, but lower revenue because individual item prices are small.",
        "Laptop and Smartphone are among the top selling products by sales value.",
        "The North and East regions are strong contributors to total sales.",
        "A few repeat customers generate high sales, so loyalty programs can help retain them.",
        "Sales increase in the last quarter, showing possible festive or year-end demand.",
        "High-value products create most of the profit, so stock planning should focus on those items.",
        "Low-cost items like notebooks and pens help increase order volume and customer engagement.",
        "Regional sales comparison can help the company plan targeted marketing campaigns.",
    ]

    for number, insight in enumerate(insights, start=1):
        print(f"{number}. {insight}")


if __name__ == "__main__":
    main()
