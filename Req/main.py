from fastapi import FastAPI, HTTPException, Query
from constants import query_forta
import requests
import pandas as pd
from typing import List, Dict
from pydantic import BaseModel
from openai import OpenAI
import pandas as pd
 

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
    forta_api_key: str = Query("YOUR_API_KEY", description="API Key for authentication"),
): 

    try:
        df = fetch_data_from_api(forta_api_url, forta_api_key, query_forta)

        # Converting DataFrame to dictionary for JSON response
        return df.to_dict(orient="records")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
#gpt integration 

client = OpenAI(api_key='sk-"YOUR_API_KEY')


# Define your request model
class GPTRequest(BaseModel):
    prompt: str
    max_tokens: int

def fetch_data_from_gpt(gpt_url: str,) -> pd.DataFrame:
    """Fetch data from API and return it as a DataFrame."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {gpt_url}",}
    gpt_url: str = Query("https://api.openai.com/v1/completions", description="The openai endpoint"),

@app.post("/generate-text/")
async def generate_text(request: GPTRequest):

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  
            messages=[{"role": "system", "content": "You are a helpful assistant."}, 
                      {"role": "user", "content": request.prompt}],
            max_tokens=150
        )
          # Check if the response has any choices
        if not response.choices:
            return {"response": "No text was generated. Please check your prompt or try again later."}
        
        if response.choices:
            return {"response": response.choices[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
