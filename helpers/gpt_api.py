import requests
import pandas as pd
import io

API_BASE_URL = "http://localhost:8000"  # FastAPI running locally

def call_cleaning_api(df: pd.DataFrame, instruction: str):
    try:
        # Convert DataFrame to CSV in memory
        csv_bytes = df.to_csv(index=False).encode()
        files = {"file": ("temp.csv", csv_bytes, "text/csv")}
        data = {"instruction": instruction}

        response = requests.post(f"{API_BASE_URL}/generate-cleaning-code", files=files, data=data)
        res = response.json()

        if response.status_code == 200 and "code" in res:
            return res["code"], None
        elif "error" in res:
            return None, res["error"]
        else:
            return None, "Unexpected API response."
    except Exception as e:
        return None, str(e)


def call_chart_code_api(df: pd.DataFrame, prompt: str):
    try:
        csv_bytes = df.to_csv(index=False).encode()
        files = {"file": ("temp.csv", csv_bytes, "text/csv")}
        data = {"prompt": prompt}

        response = requests.post(f"{API_BASE_URL}/generate-chart-code", files=files, data=data)
        res = response.json()

        if response.status_code == 200 and "code" in res:
            return res["code"], None
        elif "error" in res:
            return None, res["error"]
        else:
            return None, "Unexpected API response."
    except Exception as e:
        return None, str(e)
    
def call_cleaning_api(df: pd.DataFrame, instruction: str):
    try:
        csv_bytes = df.to_csv(index=False).encode()
        files = {"file": ("temp.csv", csv_bytes, "text/csv")}
        data = {"instruction": instruction}

        response = requests.post(f"{API_BASE_URL}/generate-cleaning-code", files=files, data=data)
        res = response.json()

        print("🧪 CLEANING API RESPONSE:", res)  # <-- Add this line

        if response.status_code == 200 and "code" in res:
            return res["code"], None
        elif "error" in res:
            return None, res["error"]
        else:
            return None, "Unexpected API response."
    except Exception as e:
        return None, str(e)

