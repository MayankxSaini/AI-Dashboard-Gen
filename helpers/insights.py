import pandas as pd

def generate_kpis(df: pd.DataFrame) -> dict:
    kpis = {}

    try:
        if "Revenue" in df.columns:
            kpis["Total Revenue"] = f"${df['Revenue'].sum():,.2f}"

        if "Units_Sold" in df.columns:
            kpis["Total Units Sold"] = int(df["Units_Sold"].sum())
            kpis["Average Units per Sale"] = f"{df['Units_Sold'].mean():.2f}"

        if "Rating" in df.columns and pd.api.types.is_numeric_dtype(df["Rating"]):
            avg_rating = df["Rating"].mean()
            kpis["Average Rating"] = f"{avg_rating:.2f}"

        if "Product" in df.columns:
            kpis["Unique Products"] = df["Product"].nunique()

        if "Region" in df.columns:
            kpis["Regions Covered"] = df["Region"].nunique()

        if "Customer_ID" in df.columns:
            kpis["Unique Customers"] = df["Customer_ID"].nunique()

        # Fallback if nothing matched
        if not kpis:
            kpis["Total Rows"] = df.shape[0]
            kpis["Total Columns"] = df.shape[1]

    except Exception as e:
        kpis["Error"] = f"Failed to compute KPIs: {str(e)}"

    return kpis


def generate_basic_insights(df):
    """
    Generate a list of text-based insights from the DataFrame.
    """
    insights = []

    if df.isnull().sum().sum() > 0:
        insights.append("⚠️ Dataset contains missing values.")

    if df.duplicated().sum() > 0:
        insights.append("⚠️ There are duplicate rows present.")

    if len(df.select_dtypes(include="object").columns) > 0:
        insights.append("🔁 Consider encoding categorical features.")

    if len(df.columns[df.nunique() == 1]) > 0:
        insights.append("ℹ️ Some columns have only one unique value and may not be useful.")

    if df.shape[0] < 10:
        insights.append("⚠️ Too few rows for meaningful statistical analysis.")

    return insights
