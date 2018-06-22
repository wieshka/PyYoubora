from config import API_SECRET, SYSTEM_CODE, OFFSET
import logging
import requests
from youbora import YouboraAuth

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

query_filter = [
    {
        "name": "api_query",
        "rules": {
            "country":
                [
                    "Germany",
                    "Italy"
                ]
        }
    }
]

query = {
    "granularity": "minute",
    "metrics": "views",
    "fromDate": "lasthour",
    "type": "LIVE",
    "filter": str(query_filter),
}

if __name__ == "__main__":
    response = requests.get('https://api.youbora.com/:system_code:/data',
                            params=query,
                            auth=YouboraAuth(API_SECRET, SYSTEM_CODE,
                                             offset=OFFSET))
    print response.text
