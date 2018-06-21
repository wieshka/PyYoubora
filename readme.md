## PyYoubora

Lays the basic foundation to interact with Youbora API. Simple & lightweight. 

### Current feature list:
- Can return JSON/CSV formatted responses;
- Handles token and dateToken generation for API calls;
- Basic query validation against Youbora Swagger JSON spec;
- Basic path validation against Youbora Swagger JSON spec;
- Can return Python Requests object for custom response formatting;

### Future considerations (wish-list):
- Filter builder/validator as currently filter bypasses any validation;
- Deeper Swagger based validation;
- In-built extendable response formatter which would return data in less Youbora specific format,
for example, formats compatible with other graphing/visualization libraries or for custom reporting needs.


### Getting started:
1. use of `virtualenv` is highly recommended;
2. Obtain from NPAW developers portal your local copy of swagger definition;
3. copy/rename `config-example.py` to `config.py`
    - configure API_SECRET
    - configure SYSTEM_CODE
    - consider changing OFFSET to increase/decrease URL validity period
    - make sure SWAGGER_DEFINITION matches path to downloaded swagger.json
4. Head to `example.py` and go crazy from there further