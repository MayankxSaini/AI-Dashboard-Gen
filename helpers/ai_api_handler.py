import requests
import pandas as pd

API_BASE_URL = "http://localhost:8000"

def request_chart_code(df, user_prompt):
    try:
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        files = {"file": ("data.csv", csv_bytes, "text/csv")}
        data = {"prompt": user_prompt}

        response = requests.post(f"{API_BASE_URL}/generate-chart-code", files=files, data=data)
        response.raise_for_status()

        json_data = response.json()
        code = json_data.get("code")

        if code is None or not isinstance(code, str) or not code.strip():
            print("⚠️ Invalid chart code received from API:")
            print(json_data)  # 👈 Full response for debugging
            return None, "❌ Invalid code returned from chart API."

        return code, None

    except Exception as e:
        return None, f"Chart API Error: {str(e)}"


def request_cleaning_code(df, user_instruction):
    try:
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        files = {"file": ("data.csv", csv_bytes, "text/csv")}
        data = {"instruction": user_instruction}

        response = requests.post(f"{API_BASE_URL}/generate-cleaning-code", files=files, data=data)
        response.raise_for_status()

        json_data = response.json()
        code = json_data.get("code")

        if code is None or not isinstance(code, str) or not code.strip():
            print("⚠️ Invalid cleaning code received from API:")
            print(json_data)  # 👈 Full response for debugging
            return None, "❌ Invalid code returned from cleaning API."

        return code, None

    except Exception as e:
        return None, f"Cleaning API Error: {str(e)}"
