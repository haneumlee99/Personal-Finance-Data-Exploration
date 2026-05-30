# Run "python -m streamlit run streamlit_app.py" in terminal

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Dataset load & clean
df = pd.read_csv("synthetic_personal_finance_dataset.csv")
df["record_date"] = pd.to_datetime(df["record_date"])


# Page Setup
st.set_page_config(page_title="Personal Finance Explorer", layout="wide")
st.title("Personal Finance Data")

# Data Description & Purpose
st.write(
    """
    Data: a synthetic personal finance dataset created based on real-world distributions from Kaggle (https://www.kaggle.com/datasets/miadul/personal-finance-ml-dataset).
    \n
    Purpose: Exploratory dashboard with user interactive features including filter perosnal finance records by region, credit score, and loan status along with key insights.
    """
)

# Explore view
st.header("Explore Data")

## Filters

# Employment status - Dropdown
employment_options = ["All"] + sorted(df["employment_status"].dropna().unique().tolist())
selected_employment = st.selectbox("Employment Status:", employment_options)

# Region - Dropdown
regions = ["All"] + sorted(df["region"].dropna().unique().tolist())
selected_region = st.selectbox("Region:", regions)

# Loan - Checkbox
show_only_loans = st.checkbox("Show only people with a loan")

# Credit score - Slider
min_score = int(df["credit_score"].min())
max_score = int(df["credit_score"].max())
credit_score_range = st.slider(
    "Credit Score Range:",
    min_value=min_score,
    max_value=max_score,
    value=(min_score, max_score)
)


## Filter Application
filtered_df = df.copy()

if selected_employment != "All":
    filtered_df = filtered_df[filtered_df["employment_status"] == selected_employment]

if selected_region != "All":
    filtered_df = filtered_df[filtered_df["region"] == selected_region]

if show_only_loans:
    filtered_df = filtered_df[filtered_df["has_loan"] == "Yes"]

filtered_df = filtered_df[
    (filtered_df["credit_score"] >= credit_score_range[0]) &
    (filtered_df["credit_score"] <= credit_score_range[1])
]

st.write(f"{len(filtered_df)} records of {len(df)}")
st.dataframe(filtered_df)


## Insights Summary
st.header("Insights Summary")

if len(filtered_df) > 0: ## error handler for no records

    # Cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Average Monthly Income", f"${filtered_df['monthly_income_usd'].mean():,.2f}")
    col2.metric("Average Monthly Expenses", f"${filtered_df['monthly_expenses_usd'].mean():,.2f}")
    col3.metric("Average Savings", f"${filtered_df['savings_usd'].mean():,.2f}")


    st.write("Average Monthly Income by Job:")
    income_by_job_title = (
        filtered_df
        .groupby("job_title")["monthly_income_usd"]
        .mean()
        .sort_values()
    )
    st.bar_chart(income_by_job_title)

    st.write("Average Monthly Expense by Job:")
    expense_by_job_title = (
        filtered_df
        .groupby("job_title")["monthly_expenses_usd"]
        .mean()
        .sort_values()
    )
    st.bar_chart(expense_by_job_title)

else:
    st.warning("No records returned.")