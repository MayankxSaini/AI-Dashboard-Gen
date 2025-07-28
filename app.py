import streamlit as st
from helpers.file_handler import load_data
from helpers.utils import apply_filters
from helpers.insights import generate_kpis, generate_basic_insights
from helpers import dashboard
from helpers.ai_api_handler import request_cleaning_code, request_chart_code
import pandas as pd
import traceback
import re

st.set_page_config(page_title="AI Dashboard Generator", layout="wide")
st.title("📊 AI-Powered Dashboard Generator")
st.markdown("Upload your dataset and generate dashboards powered by AI.")

uploaded_file = st.file_uploader("📁 Upload CSV or Excel file", type=["csv", "xlsx", "xls"])

# Utility function to sanitize and execute AI-generated code
def safe_exec(code, local_vars):
    if not isinstance(code, str):
        return None, f"❌ Invalid code format received."

    try:
        # Remove any import statements (especially for 'pd')
        code = re.sub(r"(?i)^import .*", "", code, flags=re.MULTILINE).strip()

        # Inject pandas as 'pd'
        local_vars["pd"] = pd

        exec(code, {}, local_vars)

        if "df" in local_vars and isinstance(local_vars["df"], pd.DataFrame):
            return local_vars["df"], None
        return None, "⚠️ AI-generated code did not return a valid DataFrame named `df`."
    except Exception as e:
        tb = traceback.format_exc()
        return None, f"⚠️ Error executing code:\n{e}\n\nTraceback:\n{tb}"

if uploaded_file:
    df, error = load_data(uploaded_file)

    if error:
        st.error(error)
    else:
        st.success(f"✅ Successfully loaded `{uploaded_file.name}`")

        cleaning_mode = st.radio("🧹 Choose Cleaning Method:", ["Auto Clean", "Manual Clean"], horizontal=True)

        if cleaning_mode == "Auto Clean":
            with st.spinner("Auto-cleaning the dataset using AI..."):
                instruction = "Clean this dataset by handling missing values, fixing data types, and removing outliers."
                code, err = request_cleaning_code(df, instruction)

                if err:
                    st.error(f"❌ Cleaning failed: {err}")
                else:
                    with st.expander("🧾 Cleaning Code", expanded=False):
                        st.code(code, language="python")
                    df_cleaned, exec_error = safe_exec(code, {"df": df.copy()})
                    if exec_error:
                        st.error(exec_error)
                    else:
                        st.success("✅ Auto-cleaning complete.")

        else:
            user_instruction = st.text_input("✏️ Enter your cleaning instruction")
            if user_instruction:
                with st.spinner("Processing your custom cleaning..."):
                    code, err = request_cleaning_code(df, user_instruction)
                    if err:
                        st.error(f"❌ Error: {err}")
                    else:
                        with st.expander("🧾 Custom Cleaning Code", expanded=False):
                            st.code(code, language="python")
                        df_cleaned, exec_error = safe_exec(code, {"df": df.copy()})
                        if exec_error:
                            st.error(exec_error)
                        else:
                            st.success("✅ Custom cleaning applied.")

        if 'df_cleaned' in locals() and isinstance(df_cleaned, pd.DataFrame):
            st.write("### 📌 Preview of Cleaned Data")
            st.dataframe(df_cleaned.head(50), use_container_width=True)

            st.write("### 🧮 Key Stats")
            kpis = generate_kpis(df_cleaned)
            col1, col2, col3, col4, col5 = st.columns(5)
            for idx, (label, value) in enumerate(kpis.items()):
                with [col1, col2, col3, col4, col5][idx]:
                    st.metric(label=label, value=value)

            st.write("### 🧠 Smart Insights")
            insights = generate_basic_insights(df_cleaned)
            if insights:
                for insight in insights:
                    st.markdown(f"- {insight}")
            else:
                st.success("✅ No major issues or unusual patterns detected.")

            st.write("## 📊 Automated Dashboard")
            with st.expander("📍 Numeric Columns"):
                dashboard.plot_numeric_columns(df_cleaned)

            with st.expander("📍 Categorical Columns"):
                dashboard.plot_categorical_columns(df_cleaned)

            with st.expander("📍 Correlation Matrix"):
                dashboard.plot_correlation_heatmap(df_cleaned)

            st.markdown("## 💬 Ask AI to Create Custom Charts")
            user_prompt = st.chat_input("Type a chart request like 'create pie chart for Category'")

            if user_prompt:
                st.chat_message("user").markdown(user_prompt)
                with st.spinner("Thinking..."):
                    code, error = request_chart_code(df_cleaned, user_prompt)
                    if error:
                        st.chat_message("assistant").error(error)
                    else:
                        with st.expander("🧾 Chart Code", expanded=False):
                            st.chat_message("assistant").code(code, language="python")
                        try:
                            local_vars = {"df": df_cleaned.copy(), "pd": pd}
                            exec(code, {}, local_vars)
                            chart_rendered = False
                            for val in local_vars.values():
                                if hasattr(val, "to_plotly_json"):
                                    st.plotly_chart(val, use_container_width=True)
                                    chart_rendered = True
                                    break
                            if not chart_rendered:
                                st.chat_message("assistant").warning("⚠️ No chart was rendered.")
                        except Exception as e:
                            tb = traceback.format_exc()
                            st.chat_message("assistant").error(f"⚠️ Error in code:\n{e}\n\nTraceback:\n{tb}")
