"""
Data Cleaning and Preprocessing Pipeline
=========================================
Task 01 - Data Science Internship

This script builds a reusable pipeline that:
  1. Loads a raw CSV dataset
  2. Reports data quality issues (missing values, duplicates, inconsistent formats)
  3. Cleans the data:
       - Handles missing values (numeric -> median/mean, categorical -> mode, critical fields -> drop)
       - Removes duplicate rows
       - Standardizes text formatting (case, whitespace)
       - Standardizes date formats
       - Fixes inconsistent categorical labels (e.g. Male/M/male -> Male)
  4. Saves the cleaned dataset to a new CSV
  5. Prints a before/after summary report

Usage:
    python data_cleaning_pipeline.py <input_csv> <output_csv>
"""

import sys
import pandas as pd
import numpy as np
from datetime import datetime


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def report_issues(df: pd.DataFrame, stage: str = "BEFORE"):
    print(f"\n{'=' * 60}")
    print(f"DATA QUALITY REPORT ({stage} CLEANING)")
    print(f"{'=' * 60}")
    print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"\nMissing values per column:")
    missing = df.isnull().sum()
    print(missing[missing > 0] if missing.sum() > 0 else "  None")
    print(f"\nDuplicate rows: {df.duplicated().sum()}")
    print(f"{'=' * 60}\n")


def standardize_gender(value):
    if pd.isna(value):
        return np.nan
    v = str(value).strip().lower()
    if v in ("male", "m"):
        return "Male"
    if v in ("female", "f"):
        return "Female"
    return str(value).strip().title()


def standardize_text(value):
    if pd.isna(value):
        return np.nan
    return str(value).strip().title()


def standardize_date(value):
    """Parse dates that arrive in several different formats into ISO (YYYY-MM-DD)."""
    if pd.isna(value):
        return np.nan
    value = str(value).strip()
    formats = ["%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y", "%m-%d-%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return np.nan  # unparseable date -> treat as missing


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # --- 1. Strip whitespace from all string/object columns first ---
    obj_cols = df.select_dtypes(include=["object", "str"]).columns
    for col in obj_cols:
        df[col] = df[col].apply(lambda x: str(x).strip() if pd.notna(x) else x)
        # Convert literal "NaN"/"nan"/"" strings into real NaN
        df[col] = df[col].replace(
            {"NaN": np.nan, "nan": np.nan, "": np.nan, "None": np.nan}
        )

    # --- 2. Remove exact duplicate rows ---
    before = len(df)
    df = df.drop_duplicates()
    print(f"Removed {before - len(df)} duplicate row(s).")

    # --- 3. Drop rows missing a critical identifier (Name or CustomerID) ---
    before = len(df)
    df = df.dropna(subset=["CustomerID", "Name"])
    print(f"Dropped {before - len(df)} row(s) missing critical identifiers (CustomerID/Name).")

    # --- 4. Standardize text fields ---
    df["Name"] = df["Name"].apply(standardize_text)
    df["City"] = df["City"].apply(standardize_text)
    df["Gender"] = df["Gender"].apply(standardize_gender)
    df["Email"] = df["Email"].str.lower().str.strip()

    # --- 5. Standardize dates ---
    df["SignupDate"] = df["SignupDate"].apply(standardize_date)

    # --- 6. Handle missing numeric values ---
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
    age_median = df["Age"].median()
    df["Age"] = df["Age"].fillna(age_median).astype(int)

    df["PurchaseAmount"] = pd.to_numeric(df["PurchaseAmount"], errors="coerce")
    amount_mean = round(df["PurchaseAmount"].mean(), 2)
    df["PurchaseAmount"] = df["PurchaseAmount"].fillna(amount_mean)

    # --- 7. Handle missing categorical values ---
    gender_mode = df["Gender"].mode()[0]
    df["Gender"] = df["Gender"].fillna(gender_mode)

    # --- 8. Handle missing email (can't invent one - flag it clearly) ---
    df["Email"] = df["Email"].fillna("missing@unknown.com")

    # --- 9. Reset index after all the row drops ---
    df = df.reset_index(drop=True)

    return df


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else "raw_dataset.csv"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "cleaned_dataset.csv"

    df_raw = load_data(input_path)
    report_issues(df_raw, stage="BEFORE")

    df_clean = clean_data(df_raw)

    report_issues(df_clean, stage="AFTER")

    df_clean.to_csv(output_path, index=False)
    print(f"Cleaned dataset saved to: {output_path}")


if __name__ == "__main__":
    main()
