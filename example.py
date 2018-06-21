from youbora import YouboraAPI
from config import API_SECRET, SYSTEM_CODE, SWAGGER_DEFINITION, OFFSET
import logging

logging.basicConfig(level=logging.INFO)
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
    "metrics": ["views", "concurrent"],
    "fromDate": "lasthour",
    "type": "LIVE",
    "filter": query_filter,
}

client = YouboraAPI(secret=API_SECRET, swagger=SWAGGER_DEFINITION, system_code=SYSTEM_CODE, offset=OFFSET)

if __name__ == "__main__":
    response = client("/{system_code}/data", query, response_type="json")
    # response = client("/{system_code}/data", query, response_type="csv")
    # response = client("/{system_code}/data", query)
    print response
