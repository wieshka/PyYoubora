import logging
from swagger_handler import *
import time
import hashlib
import requests

logger = logging.getLogger(__name__)


def url_encoder(data):
    """
    Wraps & re-uses Python Requests handler for task
    :param data:
    :return:
    """
    for key, value in data.items():
        if type(value) == list and key != "filter":
            data[key] = ",".join(value)
        elif key == "filter":
            data[key] = str(value)

    encoded_url = requests.models.RequestEncodingMixin._encode_params(data)

    return encoded_url


class YouboraAPI(object):
    def __init__(self, secret, swagger, system_code, offset=3600):
        """
        Configures Youbora API client
        :param secret: Youbora API secret
        :param swagger: Swagger definition as dictionary
        :param system_code: Company name/system_code
        :param offset: Time offset in future for how long in future dateToken will be set
        """
        self.api_secret = secret
        self.swagger = swagger
        self.system_code = system_code
        self.offset = offset

    @staticmethod
    def future_time(offset):
        """
        Generates future timestamp
        :param offset: time in miliseconds for offset
        :return: time.time
        """
        future_time = int(round(time.time() * 1000) + offset)

        return future_time

    def sign_request(self, path_to_sign):
        """
        Takes URL and secret, generates token and adds it to query string
        :param path_to_sign:
        :return: str
        """
        # Add md5 token
        m = hashlib.new("md5")
        m.update(path_to_sign + self.api_secret)
        signed_path = "%s&token=%s" % (path_to_sign, m.hexdigest())

        return signed_path

    def validate_request(self, dict_to_validate, path=None):
        """
        Slightly dummy and lightweight validation aka basic one
        :param dict_to_validate:
        :param path: URL path_begin to validate against Swagger [paths]
        :return: boolean
        """
        if is_valid_request(dict_to_validate, path, swagger=self.swagger) is not False:
            is_valid = True
        else:
            is_valid = False

        return is_valid

    def make_request(self, path, query_dict):
        """
        Makes request to API
        :param path: Swagger matching valid path
        :param query_dict: query dictionary which will be converted to query string
        :param force_ssl:
        :return: Python Response object
        """
        schema = self.swagger["schemes"][0]

        if self.validate_request(query_dict, path):
            query_dict["dateToken"] = self.future_time(self.offset)
            if "{system_code}" in path:
                path = path.replace("{system_code}", self.system_code)

            encoded_query_string = url_encoder(query_dict)
            signing_input = "%s?%s" % (path, encoded_query_string)
            signed_url = self.sign_request(signing_input)
            logger.debug("Signed URL: %s" % signed_url)
            host = str(self.swagger["host"])
            request_url = "%s://%s%s" % (schema, host, signed_url)
            logging.debug("Request URL: %s" % request_url)

            response = requests.get(request_url)

            return response

    def __call__(self, path, query_dict, response_type=None):
        if response_type == "csv":
            query_dict["csvFormat"] = "true"
            result = self.make_request(path, query_dict).text
        elif response_type == "json":
            query_dict["csvFormat"] = "false"
            result = self.make_request(path, query_dict).json()
        elif response_type is None:
            result = self.make_request(path, query_dict)
        else:
            raise ValueError("Unsupported response type")

        return result
