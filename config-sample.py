import json

API_SECRET = "your-api-secret"
SYSTEM_CODE = "your-system-code"
OFFSET = 36000

# This assumes that swagger.json file exists in the same path, modify to actual source.
SWAGGER_DEFINITION = json.loads(open("swagger.json").read())