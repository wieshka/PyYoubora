import logging
logger = logging.getLogger(__name__)

managed_scope = ["system_code", "dateToken", "token"]

class ApiError(Exception):
    """
    Dummy Exception type
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


def is_valid_request(dict_to_validate, path, swagger=None):
    # First things first - validates if request path is correct
    for key, value in swagger["paths"].items():
        if path == key:
            this_call_path = path
            break
    else:
        raise ApiError("Wrong API path specified")

    # Let's make sure that all required params (except the ones listed in managed_scope) are specified within query
    for param in swagger["paths"][this_call_path]["get"]["parameters"]:
        if param["required"]:
            if param["name"] not in dict_to_validate.keys():
                if param["name"] not in managed_scope:
                    raise ApiError("Missing required param: %s" % param["name"])

    # If param contains enumeration values, validate it against enum list
    for key, value in dict_to_validate.items():
        for param in swagger["paths"][this_call_path]["get"]["parameters"]:
            if param["name"] == key:
                if "enum" in param.keys():
                    if type(value) == str:
                        if value not in param["enum"]:
                            raise ApiError('Swagger validation for "%s" failed. Value %s is not valid according '
                                           'to allowed values: %s' % (key, value, param["enum"]))
                        else:
                            pass
                    elif type(value) == list:
                        if key == "filter":
                            break
                        for item in value:
                            if item not in param["enum"]:
                                raise ApiError('Swagger validation for "%s" failed. Given list value %s '
                                               'is not valid according '
                                               'to allowed values in list: %s' % (key, value, param["enum"]))
                break
        else:
                raise ApiError("No such specified query param: %s found in Swagger definition" % key)

    return True
