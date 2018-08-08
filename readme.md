## PyYoubora

Authentication library and wrapper for NPAW Youbora API.
 
This module contains:
- `YouboraAuth` - custom authorisation provider for Python Requests, check `example_auth.py`
- `YouboraClient` - Wrapper which utilises Swagger definition to validate requests
 against NPAW Youbora before executing Request, check `example_client.py`
 
## Getting started:
- install latest package with `pip install PyYoubora`
- check out included `example_auth.py` and `example_client.py` to get understanding how to use
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
    
## Good to know
- as Youbora Swagger definition is available only via closed access Developers portal,
 it is not included in this repository in order to respect NPAW approach to their documentation.
- This code base (examples and config-sample.py) assumes that swagger is available within base directory as swagger.json
- both example_x.py assumes that you have copied config-sample.py to config.py and have provided details there.
- you can very easy use any other config approach - sysarg, env, AWS KMS, etc.