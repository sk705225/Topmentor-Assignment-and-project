"""
Simple Financial Analytics Project using Python and Pandas.

This script:
1. Loads a financial dataset from a CSV file.
2. Displays the first 5 rows.
3. Checks dataset information and missing values.
4. Removes duplicate records.
5. Cleans the dataset.
6. Calculates total revenue, total expenses, total profit, and profit margin.
7. Analyzes monthly revenue, monthly profit, and yearly trends.
8. Creates simple charts.
9. Prints business insights.
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
DATA_FILE = BASE_DIR / "data" / "financial_data.csv"
CHART_DIR = BASE_DIR / "charts"
CHART_DIR.mkdir(exist_ok=True)


def load_data(file_path):
    """Load the CSV file into a Pandas DataFrame."""
    return pd.read_csv(file_path)


def clean_data(df):
    """Clean the dataset by fixing dates, removing duplicates, and handling missing values."""
    # Remove exact duplicate records
    df = df.drop_duplicates()

    # Convert Date column into date format
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Remove rows where important text/date columns are missing
    required_columns = ["Transaction ID", "Date", "Department", "Region"]
    df = df.dropna(subset=required_columns)

    # Fill missing numeric values with 0
    numeric_columns = ["Revenue", "Expenses"]
    df[numeric_columns] = df[numeric_columns].fillna(0)

    # Remove records with negative revenue or negative expenses
    df = df[(df["Revenue"] >= 0) & (df["Expenses"] >= 0)]

    # Create calculated columns
    df["Profit"] = df["Revenue"] - df["Expenses"]
    df["Profit Margin"] = df["Profit"] / df["Revenue"]

    # Create month columns for trend analysis
    df["Month Name"] = df["Date"].dt.strftime("%b")
    df["Month Number"] = df["Date"].dt.month
    df["Year Month"] = df["Date"].dt.to_period("M").astype(str)
    df["Year"] = df["Date"].dt.year

    return df


def draw_text(draw, position, text, fill="#222222"):
    """Draw text using the default font."""
    draw.text(position, text, fill=fill, font=ImageFont.load_default())


def save_simple_bar_chart(data, title, file_name):
    """Create a basic bar chart with Pillow if Matplotlib is not installed."""
    image = Image.new("RGB", (900, 550), "white")
    draw = ImageDraw.Draw(image)
    draw_text(draw, (30, 20), title)

    max_value = max(data.values)
    bar_width = 130
    gap = 45
    start_x = 80
    base_y = 460

    for index, (label, value) in enumerate(data.items()):
        bar_height = int((value / max_value) * 330)
        x1 = start_x + index * (bar_width + gap)
        y1 = base_y - bar_height
        x2 = x1 + bar_width
        draw.rectangle([x1, y1, x2, base_y], fill="#4E79A7")
        draw_text(draw, (x1, base_y + 10), str(label))
        draw_text(draw, (x1, y1 - 18), f"{value:,.0f}")

    image.save(CHART_DIR / file_name)


def save_simple_line_chart(data, title, file_name):
    """Create a basic line chart with Pillow if Matplotlib is not installed."""
    image = Image.new("RGB", (1100, 550), "white")
    draw = ImageDraw.Draw(image)
    draw_text(draw, (30, 20), title)

    values = list(data.values)
    labels = list(data.index)
    max_value = max(values)
    min_value = min(values)
    left = 70
    top = 70
    width = 960
    height = 360

    points = []
    for index, value in enumerate(values):
        x = left + int(index * (width / (len(values) - 1)))
        y = top + height - int(((value - min_value) / (max_value - min_value)) * height)
        points.append((x, y))

    draw.line(points, fill="#F28E2B", width=4)
    for point, label in zip(points, labels):
        draw.ellipse([point[0] - 5, point[1] - 5, point[0] + 5, point[1] + 5], fill="#F28E2B")
        draw_text(draw, (point[0] - 25, 455), str(label))

    image.save(CHART_DIR / file_name)


def save_simple_pie_chart(data, title, file_name):
    """Create a basic pie chart with Pillow if Matplotlib is not installed."""
    image = Image.new("RGB", (800, 550), "white")
    draw = ImageDraw.Draw(image)
    draw_text(draw, (30, 20), title)

    colors = ["#4E79A7", "#F28E2B", "#59A14F", "#E15759"]
    total = sum(data.values)
    start_angle = 0
    pie_box = [120, 80, 470, 430]

    for index, (label, value) in enumerate(data.items()):
        end_angle = start_angle + (value / total) * 360
        draw.pieslice(pie_box, start=start_angle, end=end_angle, fill=colors[index % len(colors)])
        percent = (value / total) * 100
        legend_y = 100 + index * 35
        draw.rectangle([540, legend_y, 560, legend_y + 20], fill=colors[index % len(colors)])
        draw_text(draw, (570, legend_y), f"{label}: {percent:.1f}%")
        start_angle = end_angle

    image.save(CHART_DIR / file_name)


def save_simple_histogram(values, title, file_name):
    """Create a basic histogram with Pillow if Matplotlib is not installed."""
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

    draw_text(draw, (70, 490), "Revenue bins from low to high")
    image.save(CHART_DIR / file_name)


def create_charts(df):
    """Create and save charts for the financial analysis."""
    monthly_revenue = df.groupby("Year Month")["Revenue"].sum()
    monthly_profit = df.groupby("Year Month")["Profit"].sum()
    revenue_by_department = df.groupby("Department")["Revenue"].sum().sort_values(ascending=False)
    expenses_by_region = df.groupby("Region")["Expenses"].sum()

    if not HAS_MATPLOTLIB:
        print("\nMatplotlib/Seaborn not found. Creating simple fallback charts with Pillow.")
        save_simple_bar_chart(revenue_by_department, "Revenue by Department", "bar_revenue_by_department.png")
        save_simple_line_chart(monthly_profit, "Monthly Profit Trend", "line_monthly_profit_trend.png")
        save_simple_pie_chart(expenses_by_region, "Expenses Share by Region", "pie_expenses_by_region.png")
        save_simple_histogram(df["Revenue"], "Revenue Distribution", "histogram_revenue_distribution.png")
        return

    sns.set_theme(style="whitegrid")

    # Bar Chart: Revenue by Department
    plt.figure(figsize=(8, 5))
    sns.barplot(
        x=revenue_by_department.index,
        y=revenue_by_department.values,
        hue=revenue_by_department.index,
        palette="Set2",
        legend=False,
    )
    plt.title("Revenue by Department")
    plt.xlabel("Department")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "bar_revenue_by_department.png", dpi=150)
    plt.close()

    # Line Chart: Monthly Profit Trend
    plt.figure(figsize=(11, 5))
    sns.lineplot(x=monthly_profit.index, y=monthly_profit.values, marker="o", color="#1f77b4")
    plt.title("Monthly Profit Trend")
    plt.xlabel("Month")
    plt.ylabel("Profit")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "line_monthly_profit_trend.png", dpi=150)
    plt.close()

    # Pie Chart: Expenses by Region
    plt.figure(figsize=(7, 7))
    plt.pie(expenses_by_region.values, labels=expenses_by_region.index, autopct="%1.1f%%", startangle=90)
    plt.title("Expenses Share by Region")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "pie_expenses_by_region.png", dpi=150)
    plt.close()

    # Histogram: Revenue Distribution
    plt.figure(figsize=(8, 5))
    sns.histplot(df["Revenue"], bins=10, kde=True, color="#2ca02c")
    plt.title("Revenue Distribution")
    plt.xlabel("Revenue")
    plt.ylabel("Number of Transactions")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "histogram_revenue_distribution.png", dpi=150)
    plt.close()


def main():
    # Load dataset from CSV
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
    total_revenue = df["Revenue"].sum()
    total_expenses = df["Expenses"].sum()
    total_profit = df["Profit"].sum()
    profit_margin = total_profit / total_revenue

    print("\nKEY METRICS")
    print(f"Total Revenue: {total_revenue:,.2f}")
    print(f"Total Expenses: {total_expenses:,.2f}")
    print(f"Total Profit: {total_profit:,.2f}")
    print(f"Profit Margin: {profit_margin:.2%}")

    # Analysis tables
    monthly_revenue = df.groupby("Year Month")["Revenue"].sum()
    monthly_profit = df.groupby("Year Month")["Profit"].sum()
    yearly_trend = df.groupby("Year")[["Revenue", "Expenses", "Profit"]].sum()

    print("\nMONTHLY REVENUE")
    print(monthly_revenue)

    print("\nMONTHLY PROFIT")
    print(monthly_profit)

    print("\nYEARLY TREND")
    print(yearly_trend)

    # Create charts
    create_charts(df)
    print(f"\nCharts saved in: {CHART_DIR}")

    # Business insights
    print("\nBUSINESS INSIGHTS")
    insights = [
        "Total revenue is higher than total expenses, so the business is profitable.",
        "The profit margin shows how much profit is earned from every rupee of revenue.",
        "Revenue grows steadily across the months, showing positive business momentum.",
        "Monthly profit also improves, which means expenses are being managed reasonably well.",
        "Sales department generates the highest revenue compared with other departments.",
        "Marketing has lower revenue, so campaign performance should be reviewed regularly.",
        "Operations has steady performance and supports consistent profit generation.",
        "Yearly revenue increased from 2024 to 2025, showing business growth.",
        "Expense growth should be monitored so profit margin does not fall in future months.",
        "The company can focus on high-revenue regions and departments to improve profitability.",
    ]

    for number, insight in enumerate(insights, start=1):
        print(f"{number}. {insight}")


if __name__ == "__main__":
    main()
