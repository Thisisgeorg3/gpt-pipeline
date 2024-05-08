import pandas as pd
import requests
import json
from datetime import datetime
from dateutil.parser import parse



forta_api = "https://api.forta.network/graphql"
forta_api_key = "YOUR_API_KEY"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {forta_api_key}",  
}


# start and end date needs to be in the format: YYYY-MM-DD
START_DATE = "2024-04-20"
END_DATE = "2024-05-05"

# Convert the date range to datetime objects for comparison
start_date = datetime.strptime(START_DATE, "%Y-%m-%d")
end_date = datetime.strptime(END_DATE, "%Y-%m-%d")

def parse_date(date_str):
    return parse(date_str)

query_forta = """
query Query {
  labels(
    input: {
      sourceIds: "0x1d646c4045189991fdfd24a66b192a294158b839a6ec121d740474bdacb3ab23",
      state: false,
      first: 100,
      labels: "scammer"
    }
  ) {
    labels {
      id
      label {
        label
        confidence
        entity
        entityType
        remove
        metadata
      }
      source {
        alertId
      }
      createdAt
    }
    pageInfo {
      endCursor {
        pageToken
      }
    }
  }
}
"""

#send the request
response = requests.post(forta_api, json={"query": query_forta}, headers=headers)

if response.status_code == 200:
    data = response.json()
    labels = data["data"]["labels"]["labels"]

 # Define a function to parse the date strings
    from dateutil.parser import parse

    def parse_date(date_str):
        return parse(date_str)
    
    print(data)

else:
    print(f"Query failed with status code {response.status_code}: {response.text}")

