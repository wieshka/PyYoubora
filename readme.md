## PyYoubora

Authentication library for [amazing Python requests library](https://github.com/requests/requests)
 against NPAW Youbora API.
 

 
## Getting started:
- check out included `example.py`
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
    - Swagger API validation;
    - Youbora Query Builder
    - Youbora Filter Builder
    - Response formatters for quick report/graph/dataset generations