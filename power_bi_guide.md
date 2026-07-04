# Power BI Guide For Financial Analytics

Use this guide to recreate the same visuals in Power BI.

## Load Data

1. Open Power BI Desktop.
2. Click `Get Data`.
3. Select `Text/CSV`.
4. Choose `data/financial_data.csv`.
5. Click `Load`.

## Data Cleaning In Power Query

1. Open `Transform Data`.
2. Check that `Date` is a Date column.
3. Check that `Revenue` and `Expenses` are numeric columns.
4. Remove duplicate rows.
5. Remove rows where important fields like `Transaction ID`, `Department`, or `Region` are blank.
6. Add a calculated column if needed:

```DAX
Profit = financial_data[Revenue] - financial_data[Expenses]
```

7. Click `Close & Apply`.

## DAX Measures

Create these measures in Power BI:

```DAX
Total Revenue = SUM(financial_data[Revenue])
```

```DAX
Total Expenses = SUM(financial_data[Expenses])
```

```DAX
Total Profit = [Total Revenue] - [Total Expenses]
```

```DAX
Profit Margin = DIVIDE([Total Profit], [Total Revenue])
```

Optional:

```DAX
Average Revenue = AVERAGE(financial_data[Revenue])
```

## Recreate The Visuals

### 1. Bar Chart: Revenue By Department

- Visual: Clustered bar chart
- Axis: `Department`
- Values: `Total Revenue`
- Sort: Total Revenue descending

### 2. Line Chart: Monthly Profit Trend

- Visual: Line chart
- X-axis: `Date`
- Y-axis: `Total Profit`
- Date level: Month

### 3. Pie Chart: Expenses By Region

- Visual: Pie chart
- Legend: `Region`
- Values: `Total Expenses`

### 4. Histogram: Revenue Distribution

Power BI does not always include a default histogram visual, so use a grouped column chart:

1. Right-click the `Revenue` column.
2. Select `New group`.
3. Choose bin size, such as `20000`.
4. Add a column chart.
5. Axis: `Revenue (bins)`.
6. Values: Count of `Transaction ID`.

## Suggested Dashboard Cards

Create card visuals for:

- Total Revenue
- Total Expenses
- Total Profit
- Profit Margin

## Suggested Dashboard Layout

- Top row: KPI cards
- Middle row: Revenue by Department and Expenses by Region
- Bottom row: Monthly Profit Trend and Revenue Distribution

