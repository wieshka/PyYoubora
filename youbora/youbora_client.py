import logging
from youbora_auth import YouboraAuth
import requests

logger = logging.getLogger(__name__)


class ClientValidationError(Exception):
    """
    Dummy Exception type
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


class YouboraClient(object):
    def __init__(self, config):
        self.path = None
        self.safe_path = None
        self.managed_scope = ["system_code", "dateToken", "token"]
        self.swagger_definition = config.get("swagger_definition")
        self.api_secret = config.get("api_secret")
        self.system_code = config["system_code"]
        self.time_offset = config.get("time_offset", 36000)

    def __call__(self, config):
        self.path = None
        self.safe_path = None
        self.managed_scope = ["system_code", "dateToken", "token"]
        self.swagger_definition = config.get("swagger_definition")
        self.api_secret = config.get("api_secret")
        self.system_code = config["system_code"]
        self.time_offset = config.get("time_offset", 36000)

    def _validate_path(self):
        for key, value in self.swagger_definition["paths"].items():
            if self.path == key:
                logger.debug("Request path validation passed")
                break
        else:
            raise ClientValidationError("Specified path: {0} does not match valid paths".format(self.path))

    def _validate_required_fields(self, query_dict):
        # TODO dirty approach, requires, but hey, it works.
        for param in self.swagger_definition["paths"][self.path]["get"]["parameters"]:
            if param["required"]:
                if param["name"] not in query_dict.keys():
                    if param["name"] not in self.managed_scope:
                        raise ClientValidationError("Missing required param: %s" % param["name"])
        else:
            logger.debug("All required fields are specified")

    def _validate_enums(self, query_dict):
        for key, value in query_dict.items():
            for param in self.swagger_definition["paths"][self.path]["get"]["parameters"]:
                if param["name"] == key:
                    if "enum" in param.keys():
                        if type(value) == str:
                            if value not in param["enum"]:
                                raise ClientValidationError("Value specified "
                                                            "for field {0} "
                                                            "does not match "
                                                            "allowed values: {1}".format(key, ", ".join(param["enum"])))
                            else:
                                logger.debug("Value {0} for {1} passed enum check".format(value, key))
                        elif type(value) == list:
                            if key == "filter":
                                logger.debug("Skipping filter check")
                                break
                            for item in value:
                                if item not in param["enum"]:
                                    raise ClientValidationError("Value specified "
                                                                "for field {0} "
                                                                "does not match "
                                                                "allowed values: {1}".format(key, ", ".join(param["enum"])))
                    break
            else:
                raise ClientValidationError("No such specified query "
                                            "param: {0} found in Swagger definition".format(key))

    def _request(self, query_dict):
        url = "https://{0}{1}".format(self.swagger_definition["host"], self.safe_path)
        response = requests.get(url,
                                params=query_dict,
                                auth=YouboraAuth(self.api_secret, self.system_code,
                                                 offset=self.time_offset))
        return response

    def request(self, path, query_dict):
        self.safe_path = path
        self.path = path.replace(":system_code:", "{system_code}")
        self._validate_path()
        self._validate_required_fields(query_dict)
        self._validate_enums(query_dict)
        return self._request(query_dict)
