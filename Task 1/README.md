# Task 01 – Data Cleaning and Preprocessing Pipeline

## Overview
This project builds a reusable data cleaning and preprocessing pipeline for a customer
dataset. The goal is to take a raw, messy CSV and turn it into a clean, consistent
dataset that is ready for analysis or modeling.

## Dataset
- **File:** `raw_dataset.csv`
- **Shape:** 15 rows × 8 columns
- **Columns:** CustomerID, Name, Age, Gender, City, SignupDate, PurchaseAmount, Email
- **Type:** Sample customer dataset created to represent common real-world data
  quality problems.

## Issues Identified
| Issue | Details |
|---|---|
| Missing values | Name (1), Age (3), PurchaseAmount (2), Email (1) |
| Duplicate rows | 2 exact duplicate rows |
| Inconsistent date formats | Mixed `YYYY-MM-DD`, `MM/DD/YYYY`, `YYYY/MM/DD`, `MM-DD-YYYY` |
| Inconsistent categorical labels | Gender stored as `Male`/`male`/`M`, `Female`/`female`/`F` |
| Inconsistent text formatting | Extra whitespace and mixed casing in Name/City |
| Fake null values | Missing values stored as the literal string `"NaN"` |

## Cleaning Steps
1. **Whitespace & fake nulls** – Stripped leading/trailing whitespace from all text
   fields and converted placeholder strings (`"NaN"`, `""`, `"None"`) into real
   missing values.
2. **Duplicates** – Removed exact duplicate rows.
3. **Critical fields** – Dropped rows missing a critical identifier (CustomerID or
   Name), since these can't be reliably imputed.
4. **Text standardization** – Converted Name and City to consistent Title Case;
   lowercased email addresses.
5. **Gender standardization** – Mapped all variants (`M`, `male`) to `Male` and
   (`F`, `female`) to `Female`.
6. **Date standardization** – Parsed all four date formats and converted every
   date to a single ISO format (`YYYY-MM-DD`).
7. **Missing numeric values** – Filled missing `Age` with the column median and
   missing `PurchaseAmount` with the column mean.
8. **Missing categorical values** – Filled missing `Gender` with the column mode.
9. **Missing email** – Filled missing emails with a clear placeholder
   (`missing@unknown.com`) rather than inventing a real one.

## Before / After Summary
| Metric | Before | After |
|---|---|---|
| Rows | 15 | 12 |
| Duplicate rows | 2 | 0 |
| Missing values (total) | 7 | 0 |
| Date formats in use | 4 (mixed) | 1 (ISO, standardized) |

## How to Run
​```bash
python data_cleaning_pipeline.py raw_dataset.csv cleaned_dataset.csv
​```
This prints a before/after data quality report to the console and saves the
cleaned dataset to `cleaned_dataset.csv`.

## Key Takeaway
Cleaning raw data is often the most time-consuming but highest-leverage step in a
data science workflow — a model is only as reliable as the data it's trained on.
