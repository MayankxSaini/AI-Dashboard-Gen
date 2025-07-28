import pandas as pd

def load_data(file):
    try:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        elif file.name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file)
        else:
            return None, "Unsupported file type. Please upload a CSV or Excel file."
        
        return df, None
    except Exception as e:
        return None, f"❌ Error reading file: {str(e)}"
