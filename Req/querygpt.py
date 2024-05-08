from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from openai import OpenAI
import pandas as pd

client = OpenAI(api_key='sk-"YOUR_API_KEY')

app = FastAPI()

# Define your request model
class GPTRequest(BaseModel):
    prompt: str
    max_tokens: int

def fetch_data_from_api(gpt_url: str,) -> pd.DataFrame:
    """Fetch data from API and return it as a DataFrame."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {gpt_url}",}
    gpt_url: str = Query("https://api.openai.com/v1/completions", description="The endpoint"),

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


  
