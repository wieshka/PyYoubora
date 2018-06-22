## PyYoubora

Authentication library and wrapper for NPAW Youbora API.
 
This module contains:
- `YouboraAuth` - custom authorisation provider for Python Requests, check `example_auth.py`
- `YouboraClient` - Wrapper which utilises Swagger definition to validate requests
 against NPAW Youbora before executing Request, check `example_client.py`
 
## Getting started:
- check out included `example_auth.py` and `example_client.py`
- but, basically this gives you:

```python
import requests
from youbora import YouboraAuth

query = {}

response = requests.get('https://api.youbora.com/:system_code:/data',
                        params=query,
                        auth=YouboraAuth("secret", "system_code")
```

## Future considerations (wish list):
- to extend library with _helpers_ such as:
    - More Swagger API validations;
    - Youbora Query Builder, interactive perhaps ?
    - Youbora Filter Builder, interactive perhaps ?
    - Response formatter for quick report/graph generations in various formats