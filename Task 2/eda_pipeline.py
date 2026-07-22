"""
Exploratory Data Analysis (EDA) Pipeline
==========================================
Task 02 - Data Science Internship

This script performs a full exploratory data analysis on a customer dataset:
  1. Loads the dataset and prints summary statistics
  2. Checks for missing values and data types
  3. Generates visualizations:
       - Histograms for numeric distributions (Age, PurchaseAmount, Rating)
       - Bar charts for categorical breakdowns (Gender, City, ProductCategory)
       - A correlation heatmap for numeric features
  4. Saves all plots as PNG files
  5. Prints a written summary of the key insights found

Usage:
    python eda_pipeline.py <input_csv>
"""

import sys
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 110


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def basic_overview(df: pd.DataFrame):
    print("=" * 60)
    print("DATASET OVERVIEW")
    print("=" * 60)
    print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns\n")
    print("Data types:")
    print(df.dtypes)
    print("\nMissing values per column:")
    missing = df.isnull().sum()
    print(missing[missing > 0] if missing.sum() > 0 else "  None")
    print("\nSummary statistics (numeric columns):")
    print(df.describe().round(2))
    print("=" * 60 + "\n")


def plot_histograms(df: pd.DataFrame, cols, filename):
    fig, axes = plt.subplots(1, len(cols), figsize=(5 * len(cols), 4))
    for ax, col in zip(axes, cols):
        sns.histplot(df[col], kde=True, ax=ax, color="#2563eb")
        ax.set_title(f"Distribution of {col}")
    plt.tight_layout()
    plt.savefig(filename, bbox_inches="tight")
    plt.close()
    print(f"Saved: {filename}")


def plot_bar_charts(df: pd.DataFrame, cols, filename):
    fig, axes = plt.subplots(1, len(cols), figsize=(6 * len(cols), 4))
    if len(cols) == 1:
        axes = [axes]
    for ax, col in zip(axes, cols):
        counts = df[col].value_counts()
        sns.barplot(x=counts.values, y=counts.index, hue=counts.index, ax=ax, palette="viridis", legend=False)
        ax.set_title(f"Count by {col}")
        ax.set_xlabel("Count")
    plt.tight_layout()
    plt.savefig(filename, bbox_inches="tight")
    plt.close()
    print(f"Saved: {filename}")


def plot_correlation(df: pd.DataFrame, cols, filename):
    corr = df[cols].corr()
    plt.figure(figsize=(6, 5))
    sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, fmt=".2f")
    plt.title("Correlation Heatmap (Numeric Features)")
    plt.tight_layout()
    plt.savefig(filename, bbox_inches="tight")
    plt.close()
    print(f"Saved: {filename}")


def plot_avg_spend_by_category(df: pd.DataFrame, filename):
    avg_spend = df.groupby("ProductCategory")["PurchaseAmount"].mean().sort_values(ascending=False)
    plt.figure(figsize=(7, 4))
    sns.barplot(x=avg_spend.values, y=avg_spend.index, hue=avg_spend.index, palette="magma", legend=False)
    plt.title("Average Purchase Amount by Product Category")
    plt.xlabel("Average Purchase Amount ($)")
    plt.tight_layout()
    plt.savefig(filename, bbox_inches="tight")
    plt.close()
    print(f"Saved: {filename}")


def print_insights(df: pd.DataFrame):
    print("\n" + "=" * 60)
    print("KEY INSIGHTS")
    print("=" * 60)

    top_city = df["City"].value_counts().idxmax()
    top_category = df["ProductCategory"].value_counts().idxmax()
    corr_age_amount = df["Age"].corr(df["PurchaseAmount"])
    corr_amount_rating = df["PurchaseAmount"].corr(df["Rating"])
    avg_spend = df.groupby("ProductCategory")["PurchaseAmount"].mean().sort_values(ascending=False)

    print(f"1. Most customers are based in {top_city} "
          f"({df['City'].value_counts().max()} out of {len(df)}).")
    print(f"2. {top_category} is the most purchased product category "
          f"({df['ProductCategory'].value_counts().max()} purchases).")
    print(f"3. Age and PurchaseAmount have a correlation of {corr_age_amount:.2f}, "
          f"suggesting {'a weak' if abs(corr_age_amount) < 0.3 else 'a moderate'} "
          f"relationship between customer age and spend.")
    print(f"4. PurchaseAmount and Rating have a correlation of {corr_amount_rating:.2f}, "
          f"suggesting {'higher spenders tend to rate slightly higher' if corr_amount_rating > 0.3 else 'little relationship between spend and satisfaction'}.")
    print(f"5. Highest average spend is in '{avg_spend.index[0]}' "
          f"(${avg_spend.iloc[0]:.2f}), lowest is in '{avg_spend.index[-1]}' "
          f"(${avg_spend.iloc[-1]:.2f}).")
    print("=" * 60 + "\n")


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else "eda_dataset.csv"
    df = load_data(input_path)

    basic_overview(df)

    plot_histograms(df, ["Age", "PurchaseAmount", "Rating"], "histograms.png")
    plot_bar_charts(df, ["Gender", "City", "ProductCategory"], "bar_charts.png")
    plot_correlation(df, ["Age", "PurchaseAmount", "Rating"], "correlation_heatmap.png")
    plot_avg_spend_by_category(df, "avg_spend_by_category.png")

    print_insights(df)


if __name__ == "__main__":
    main()
