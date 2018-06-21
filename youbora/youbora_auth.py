import hashlib
import logging
import time
from requests.auth import AuthBase
from urlparse import parse_qsl, urlsplit, urlunsplit
from urllib import urlencode

logger = logging.getLogger(__name__)


class YouboraAuth(AuthBase):
    def __init__(self, api_key, system_code, **kwargs):
        self.api_key = api_key
        self.system_code = system_code
        self.offset = kwargs.get("offset", 36000)

    def __call__(self, request):
        self._prepare(request)
        return request

    def _prepare(self, request):
        self.request = request
        self.original_url = request.url
        self.scheme, self.netloc, self.original_path, query_string, self.fragment = urlsplit(self.original_url)
        self.query_params = parse_qsl(query_string)
        self.path = self.original_path.replace(":system_code:", self.system_code)

        self._add_date_token()
        self._add_security_token()
        self._finalise(request)

    def _add_date_token(self):
        future_time = int(round(time.time() * 1000) + self.offset)
        self.query_params.append(('dateToken', future_time))

    def _add_security_token(self):
        m = hashlib.new("md5")
        qs_part = urlencode(self.query_params, doseq=True)
        m.update("{0}?{1}{2}".format(self.path, qs_part, self.api_key))
        token = m.hexdigest()
        self.query_params.append(('token', token))

    def _finalise(self, request):
        query_string = urlencode(self.query_params, doseq=True)
        final_url = urlunsplit((self.scheme, self.netloc, self.path.split("?")[0], query_string, self.fragment))
        request.url = final_url
