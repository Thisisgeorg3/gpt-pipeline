from fastapi import FastAPI, HTTPException, Query
from constants import query_forta
import requests
import pandas as pd
from typing import List, Dict
 

app = FastAPI() 

def fetch_data_from_api(forta_api_url: str, forta_api_key: str, query: str) -> pd.DataFrame:
    """Fetch data from an external API and return it as a DataFrame."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {forta_api_key}",
    }

    params = {"query": query}  # Or any other parameters needed

    response = requests.post(forta_api_url, headers=headers, json=params)
    if response.status_code != 200:
        # print(response.text)
        raise HTTPException(status_code=500, detail="Failed to retrieve data")
    data = response.json()  
    labels = data["data"]["labels"]["labels"]
    return pd.DataFrame(labels)

@app.get("/analyze",) 
def analyze_data(
    forta_api_url: str = Query("https://api.forta.network/graphql", description="The Forta API endpoint"),
    forta_api_key: str = Query("your-api-key", description="API Key for authentication"),
): 

    try:
        df = fetch_data_from_api(forta_api_url, forta_api_key, query_forta)

        # Converting DataFrame to dictionary for JSON response
        return df.to_dict(orient="records")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
