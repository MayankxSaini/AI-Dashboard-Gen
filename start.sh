#!/bin/bash

# Start FastAPI backend in background
uvicorn api_server:app --host 0.0.0.0 --port 8000 &

# Wait a few seconds to ensure backend starts
sleep 5

# Start Streamlit frontend
streamlit run app.py --server.port 10000 --server.address 0.0.0.0
