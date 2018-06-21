import base64
import datetime
import dateutil.tz
import hashlib
from hashlib import sha256
import logging
import time
from requests.auth import AuthBase
from urlparse import parse_qsl, urlsplit, urlunsplit
from urllib import urlencode
logger = logging.getLogger(__name__)


class YouboraAuth(AuthBase):
    def __init__(self, *args, **kwargs):
        self.system_code = args[1]
        self.api_key = args[0]

    def __call__(self, request):
        self._encode(request)
        return request

    @staticmethod
    def _add_date_token(request, offset=36000):
        # Add the API key as a query parameter
        url = request.url
        scheme, netloc, path, query_string, fragment = urlsplit(url)
        query_params = parse_qsl(query_string)

        future_time = int(round(time.time() * 1000) + offset)
        query_params.append(('dateToken', future_time))

        new_query_string = urlencode(query_params, doseq=True)
        new_url = urlunsplit((scheme, netloc, path.split("?")[0], new_query_string, fragment))
        request.url = new_url

    def _add_token(self, request):
        url = request.url
        scheme, netloc, path, query_string, fragment = urlsplit(url)
        query_params = parse_qsl(query_string)

        m = hashlib.new("md5")
        path = request.path_url
        logger.debug("Signing path: {0}".format(path))

        m.update(path + self.api_key)
        token = m.hexdigest()
        query_params.append(('token', token))

        new_query_string = urlencode(query_params, doseq=True)
        new_url = urlunsplit((scheme, netloc, path.split("?")[0], new_query_string, fragment))
        request.url = new_url

    def _prepare(self, request):
        url = request.url
        scheme, netloc, path, query_string, fragment = urlsplit(url)

        new_path = path.replace(":system_code:", self.system_code)
        print new_path

        new_url = urlunsplit((scheme, netloc, new_path, query_string, fragment))
        request.url = new_url

    def _encode(self, request):
        self._prepare(request)
        self._add_date_token(request, offset=3600)
        self._add_token(request)
        logger.debug(request.url)
