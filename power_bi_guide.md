# Power BI Guide For Retail Analytics

Use this guide to recreate the same visuals in Power BI.

## Load Data

1. Open Power BI Desktop.
2. Click `Get Data`.
3. Select `Text/CSV`.
4. Choose `data/retail_sales.csv`.
5. Click `Load`.

## Data Cleaning In Power Query

1. Open `Transform Data`.
2. Check that `Order Date` is a Date column.
3. Check that `Quantity`, `Sales`, and `Profit` are numeric columns.
4. Remove duplicate rows from the table.
5. Remove rows where important fields like `Order ID`, `Customer ID`, or `Product Name` are blank.
6. Click `Close & Apply`.

## DAX Measures

Create these measures in Power BI:

```DAX
Total Sales = SUM(retail_sales[Sales])
```

```DAX
Total Profit = SUM(retail_sales[Profit])
```

```DAX
Total Orders = DISTINCTCOUNT(retail_sales[Order ID])
```

```DAX
Average Sales = AVERAGE(retail_sales[Sales])
```

You can also create:

```DAX
Total Customers = DISTINCTCOUNT(retail_sales[Customer ID])
```

## Recreate The Visuals

### 1. Bar Chart: Sales By Category

- Visual: Clustered bar chart
- Axis: `Category`
- Values: `Total Sales`
- Sort: Total Sales descending

### 2. Line Chart: Monthly Sales Trend

- Visual: Line chart
- X-axis: `Order Date`
- Y-axis: `Total Sales`
- Date level: Month

### 3. Pie Chart: Sales By Region

- Visual: Pie chart
- Legend: `Region`
- Values: `Total Sales`

### 4. Histogram: Sales Distribution

Power BI does not have a default histogram in all versions, so use one of these options:

- Use a column chart with grouped sales bins.
- Or install a histogram visual from AppSource.

Simple bin method:

1. Right-click the `Sales` column.
2. Select `New group`.
3. Choose bin size, such as `10000`.
4. Create a column chart.
5. Axis: `Sales (bins)`.
6. Values: Count of `Order ID`.

## Suggested Dashboard Cards

Create card visuals for:

- Total Sales
- Total Profit
- Total Orders
- Average Sales
- Total Customers

## Suggested Dashboard Layout

- Top row: KPI cards
- Middle row: Sales by Category and Sales by Region
- Bottom row: Monthly Sales Trend and Sales Distribution

