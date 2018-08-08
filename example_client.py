from config import API_SECRET, SYSTEM_CODE, OFFSET, SWAGGER_DEFINITION
import logging
from youbora import YouboraClient

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

config = {
    "swagger_definition": SWAGGER_DEFINITION,
    "api_secret": API_SECRET,
    "system_code": SYSTEM_CODE,
    "time_offset": OFFSET
}

# query_filter = [n
#     {
#         "name": "api_query",
#         "rules": {
#             "country":
#                 [
#                     "Germany",
#                     "Italy"
#                 ]
#         }
#     }
# ]

query_filter = [{
    "name": "Android+Android 7.0",
    "rules": {
        "os": ["Android"]
    },
    "exclusion": "include",
    "color": "primary"
}, {
    "name": "iOS",
    "color": "primary",
    "rules": {
        "os": ["iOS"]
    }
}]

query = {
    # "granularity": "minute",
    "metrics": "views",
    "fromDate": "lasthour",
    "type": "LIVE",
    # "filter": str(query_filter),
    # "csvFormat": "true",
    "groupBy": ["os", "os_version"],
    "orderBy": "views",
    "limit": 1000,
    "orderDirection": "desc",
    "operation": "reducedisjoin",
}


client = YouboraClient(config)

if __name__ == "__main__":
    r = client.request("/:system_code:/data", query)
    print r.json()
