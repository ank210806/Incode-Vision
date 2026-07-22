# Task 02 – Exploratory Data Analysis (EDA)

## Overview
This project performs exploratory data analysis on a customer purchase dataset,
using statistics and visualizations to uncover patterns before any modeling work
begins.

## Dataset
- **File:** `eda_dataset.csv`
- **Shape:** 300 rows × 8 columns
- **Columns:** CustomerID, Age, Gender, City, ProductCategory, PurchaseAmount,
  Rating, SignupDate
- **Type:** Synthetic e-commerce customer dataset created to represent realistic
  purchasing behavior across cities, product categories, and demographics.

## Summary Statistics
| Metric | Age | PurchaseAmount ($) | Rating |
|---|---|---|---|
| Mean | 34.6 | 185.33 | 3.79 |
| Std Dev | 9.5 | 110.21 | 0.74 |
| Min | 18 | 10.00 | 1.7 |
| Median | 35 | 161.85 | 3.8 |
| Max | 70 | 562.25 | 5.0 |

No missing values were present in this dataset.

## Visualizations
| File | Description |
|---|---|
| `histograms.png` | Distribution of Age, PurchaseAmount, and Rating |
| `bar_charts.png` | Customer counts by Gender, City, and ProductCategory |
| `correlation_heatmap.png` | Correlation between Age, PurchaseAmount, and Rating |
| `avg_spend_by_category.png` | Average purchase amount per product category |

## Key Insights
1. **New York** has the largest customer base (83 of 300 customers), consistent
   with the city weighting used to generate the sample.
2. **Electronics** is the most purchased product category (59 purchases),
   followed closely by Clothing and Home & Kitchen.
3. **Age vs. PurchaseAmount** shows a weak positive correlation (r ≈ 0.15) —
   older customers spend only marginally more, not a strong driver.
4. **PurchaseAmount vs. Rating** shows
