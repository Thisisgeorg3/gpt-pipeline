from fastapi import FastAPI, HTTPException, Query
from constants import query
import requests
import pandas as pd
from typing import List, Dict
 

app = FastAPI() 

def fetch_data_from_api(forta_api_url: str, forta_api_key: str, query: str) -> pd.DataFrame:
    """Fetch data from an external API and return it as a DataFrame."""
    headers = {
        "Authorization": f"Bearer {forta_api_key}",
    }

    params = {"query": query}  # Or any other parameters needed

    response = requests.get(forta_api_url, headers=headers, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to retrieve data")

    data = response.json()  
    return pd.DataFrame(data)

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Process data by extracting necessary fields."""
    df = df[['sourceIds', 'state']]  # Keep only specific columns
    # Additional processing as needed
    return df

@app.get("/analyze", response_model=List[Dict[str, str]])
def analyze_data(
    query: str = Query(query, description="Query for data extraction"),
    forta_api_url: str = Query("https://api.forta.network/graphql", description="The Forta API endpoint"),
    forta_api_key: str = Query("f4322c61a16efe17:9ffee3e5623f75a61d62f5a4a7fa4da7af8e6d4bb1963d91fd2486f9b88c3107", description="API Key for authentication"),
):
    
    @app.get("/")
    def root(): 
        """Endpoint to fetch and process data from an external API."""
    try:
        df = fetch_data_from_api(forta_api_url, forta_api_key, query)
        df = process_data(df)


        # Converting DataFrame to dictionary for JSON response
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

