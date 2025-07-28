import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

def plot_numeric_columns(df):
    """
    Plot histograms for numeric columns using Plotly.
    """
    numeric_cols = df.select_dtypes(include="number").columns
    if len(numeric_cols) == 0:
        st.info("No numeric columns found.")
        return

    for col in numeric_cols:
        fig = px.histogram(df, x=col, nbins=30, title=f"Distribution of {col}")
        st.plotly_chart(fig, use_container_width=True)

def plot_categorical_columns(df):
    """
    Plot bar charts for categorical columns using Plotly.
    """
    cat_cols = df.select_dtypes(exclude="number").columns
    if len(cat_cols) == 0:
        st.info("No categorical columns found.")
        return

    for col in cat_cols:
        data = df[col].value_counts().reset_index()
        data.columns = [col, "Count"]
        fig = px.bar(data, x=col, y="Count", title=f"Count of {col}")
        st.plotly_chart(fig, use_container_width=True)

def plot_correlation_heatmap(df):
    """
    Plot a correlation heatmap using seaborn for numeric columns.
    """
    num_df = df.select_dtypes(include="number")
    if num_df.empty:
        st.info("No numeric data to display correlation heatmap.")
        return

    corr = num_df.corr()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)
