from config import API_SECRET, SYSTEM_CODE, OFFSET
import logging
import requests
from youbora import YouboraAuth

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

query = {
    "granularity": "minute",
    "metrics": "views",
    "fromDate": "lasthour",
    "type": "LIVE",
    "csvFormat": "true",
    "filter": str([
    {
        "name": "column_name",
        "rules": {
            "country":
                [
                    "Spain",
                    "Italy"
                ]
        }
    }
])
}

if __name__ == "__main__":
    response = requests.get('https://api.youbora.com/:system_code:/data',
                            params=query,
                            auth=YouboraAuth(API_SECRET, SYSTEM_CODE,
                                             offset=OFFSET))
    print response.text
