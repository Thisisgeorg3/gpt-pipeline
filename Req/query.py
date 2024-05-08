import pandas as pd
import requests
import json
from datetime import datetime

forta_api = "https://api.forta.network/graphql"
headers = {"content-type": "application/json"}

# start and end date needs to be in the format: YYYY-MM-DD
START_DATE = "2024-01-10"
END_DATE = "2024-04-20"

# Convert the date range to datetime objects for comparison
start_date = datetime.strptime(START_DATE, "%Y-%m-%d")
end_date = datetime.strptime(END_DATE, "%Y-%m-%d")

query = """
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


