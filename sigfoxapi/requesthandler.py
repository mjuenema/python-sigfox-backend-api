"""
Custom drest.RequestHandler that works around
https://github.com/datafolklabs/drest/issues/35

"""

import os
import sys

if sys.version_info[0] < 3:
    import httplib # pragma: no cover
    from urllib import urlencode # pragma: no cover
    from urllib2 import urlopen # pragma: no cover
else:
    from http import client as httplib # pragma: no cover
    from urllib.parse import urlencode # pragma: no cover
    from urllib.request import urlopen # pragma: no cover

import socket
from httplib2 import Http, ServerNotFoundError

from drest import exc, interface, meta, serialization, response, request

class RequestHandler(request.RequestHandler):


    def make_request(self, method, url, params=None, headers=None):
        """
        Make a call to a resource based on path, and parameters.

        Required Arguments:

            method
                One of HEAD, GET, POST, PUT, PATCH, DELETE, etc.

            url
                The full url of the request (without any parameters).  Any
                params (with GET method) and self.extra_url_params will be
                added to this url.

        Optional Arguments:

            params
                Dictionary or list (POST only) of additional (one-time)
                keyword arguments for the request.

            headers
                Dictionary of additional (one-time) headers of the request.

        """
        if params is None:
            params = {}
        if headers is None:
            headers = {}

        # ---------------------------------------------------------------------
        # Only mixin self._extra_params if params is a dict.
        # This is different from the default drest RequestHandler.
        if isinstance(params, dict):
            params = dict(self._extra_params, **params)
        # ---------------------------------------------------------------------

        headers = dict(self._extra_headers, **headers)
        url = self._get_complete_url(method, url, params)

        if self._meta.debug:
            print('DREST_DEBUG: method=%s url=%s params=%s headers=%s' % \
                   (method, url, params, headers))

        if self._meta.serialize: 
            payload = self._serialize(params)
        else:
            payload = urlencode(params)

        if method is 'GET' and not self._meta.allow_get_body:
            payload = ''
            if self._meta.debug:
                print("DREST_DEBUG: supressing body for GET request")

        res_headers, data = self._make_request(url, method, payload,
                                               headers=headers)
        unserialized_data = data
        serialized_data = None
        if self._meta.deserialize:
            serialized_data = data
            data = self._deserialize(data)

        return_response = response.ResponseHandler(
            int(res_headers['status']), data, res_headers,
            )

        return self.handle_response(return_response)
