"""
Python wrapper for the Sigfox backend REST API.

Inspired by https://pypi.python.org/pypi/pySigfox.

(c) 2017 Markus Juenemann

"""

import copy
import urllib.parse
import functools

import drest
import drest.exc
import drest.serialization

import sigfoxapi.requesthandler

__author__ = 'Markus Juenemann <markus@juenemann.net>'
__version__ = '0.3.0'
__license__ = 'BSD 2-clause "Simplified" License'

SIGFOX_API_URL = 'https://backend.sigfox.com/api/'

IGNORE_SSL_VALIDATION = False
"""Set to ``True`` to ignore SSL validation problems."""

DEBUG = False
"""Set to ``True`` to enable debugging."""

RETURN_OBJECTS = False
"""Change to ``True`` to return objects instead of dictionaries. Returning
   objects allows to access fields in the ``object.field`` syntax instead
   of ``dict['field']`` which some people may prefer.

   >>> sigfoxapi.RETURN_OJECTS = False
   >>> group = s.group_info('489b848ee4b0ca4786945614')
   >>> group['name']
   Group 1
   >>> sigfoxapi.RETURN_OJECTS = True
   >>> group = s.group_info('489b848ee4b0ca4786945614')
   >>> group.name
   Group 1
"""


class SigfoxApiError(Exception):
    """Base exception for all errors.

       >>> try:
       ...     s.group_info('does_not_exist')
       ... except SigfoxApiNotFound:
       ...     print('Not found')
       ... except SigfoxApiError:
       ...     print('Other Sigfox error')

    """

    pass


class SigfoxApiBadRequest(SigfoxApiError):
    """Exception for HTTP error 400 (Bad Request).


       .. important:: This exception will also be raised if the `before` or
           `since` arguments to some methods are set in a way that
           no results would be returned. For example I didn't send
           any messages before 01-May-2017 so searching for any
           will raise `SigfoxApiBadRequest` instead of returning
           an empty list!

           >>> t = 1493560800    # Unix timestamp 01-May-2017 00:00:00
           >>> try:
           ...     s.device_messages(SIGFOX_DEVICE_ID, before=t)
           ... except SigfoxApiBadRequest:
           ...     print("No Sigfox messages found before 01-May-2017")

    """
    pass


class SigfoxApiAuthError(SigfoxApiError):
    """Exception for HTTP error 401 (Authentication Error)."""
    pass


class SigfoxApiAccessDenied(SigfoxApiError):
    """Exception for HTTP error 403 (Access Denied)."""
    pass


class SigfoxApiServerError(SigfoxApiError):
    """Exception for HTTP error 500 (Internal Server Error)."""
    pass


class SigfoxApiNotFound(SigfoxApiError):
    """Exception for HTTP error 404 (Not Found).

       >>> try:
       ...     s.group_info('123456789012345678901234')
       ... except SigfoxApiNotFound:
       ...     print('Not found')

    """
    pass


class Object(object):
    """Convert a dictionary to an object.

       `Object` is used internally to implement the
       ``sigfoxapi.RETURN_OBJECTS=True`` functionality.

       All attributes are read-only.

       This class works in the context of this module
       but may fail elsewhere.

    """

    def __init__(self, _data):
        self._data = _data

    def __getattr__(self, name):
        try:
            if isinstance(self._data[name], dict):
                return Object(self._data[name])
            elif isinstance(self._data[name], list):
                return Object(self._data[name])
            else:
                return self._data[name]
        except KeyError:
            raise AttributeError(name)

    def __getitem__(self,  key):
        value = self._data[key]
        if isinstance(value, dict):
            return Object(value)
        elif isinstance(value, list):
            return Object(value)
        else:
            return value

    def __len__(self):
        return len(self._data)

    def __add__(self, other):
        """Implement ``sigfoxapi.Object + sigfoxapi.Object``."""
        return Object(self._data + other._data)

    def __iadd__(self, other):
        self._data += other._data
        return self

class Sigfox(object):
    """Interact with the Sigfox backend API.

       :param login: Login as shown on the *Group* - *REST API* pacge of the
                     Sigfox backend web interface.
       :param password: Password as shown on the *Group* - *REST API* pacge of the
                     Sigfox backend web interface.

       >>> s = Sigfox('1234567890abcdef', 'fedcba09876543221')

       .. note:: Response paging has not been implemented yet, i.e. currently
                 at most 100 results (the backend default) will be returned.

    """

    def next(self, *args, **kwargs):
        """Fetch the next page of results for some methods.

           Call this method whenever another method has returned only
           a subset of the results. 

           >>> messages = s.device_messages('4d3091a05ee16b3cc86699ab')
           >>> while s.next:
           ...     messages += s.next()
           >>> len(messages)
           310
           >>> devices = s.device_list('4d3091a05ee16b3cc86699ab')
           >>> while s.next:
           ...     devices += s.next()
           >>> len(devices)
           22

           .. warning:: Be mindful that this may return a huge number of
                        results if used exactly as in the example above.

        """

        # `Sigfox.next()` will be set in `Sigfox.request()` to ``None`` or
        # a `functool.partial(...)` method matching the original method.
        # The code here is only for documentation purposes.
        pass


    def __init__(self, login, password):
        self.api = drest.API(SIGFOX_API_URL, debug=DEBUG,
                             serialization_handler=drest.serialization.JsonSerializationHandler,
                             serialize=True,
                             deserialize=True,
                             ignore_ssl_validation=IGNORE_SSL_VALIDATION,
                             trailing_slash=False,
                             request_handler = sigfoxapi.requesthandler.RequestHandler
                             )
        self.api.auth(login, password)


    def request(self, method, path, params=None, headers=None):
        """Perform HTTP(S) request and return response data.

           The response data will already have been serialized to a dictionary because
           of ``serialization_handler=drest.serialization.JsonSerializationHandler``.

           :param method: The HTTP method to use.
           :param params: Any parameters to be send to the resource.
           :param headers: Any headers to be send to the resource.

        """

        try:
            resp = self.api.make_request(method, path, params=params, headers=headers)
        except (drest.exc.dRestRequestError) as e:
            if e.response.status == 400:
                raise SigfoxApiBadRequest(str(e))
            elif e.response.status == 401:
                raise SigfoxApiAuthError(str(e))
            elif e.response.status == 403:
                raise SigfoxApiAccessDenied(str(e))
            elif e.response.status == 404:
                raise SigfoxApiNotFound(str(e))
            elif e.response.status == 500:
                raise SigfoxApiServerError(str(e))
            else:
                raise SigfoxApiError(str(e))

        try:
            data = resp.data['data']
        except (KeyError, TypeError):
            data = resp.data

        # Set Sigfox.next()`by extracting the parameters from the 'next' URL and
        # currying the self.request().
        try:
            next_params = dict(urllib.parse.parse_qsl(resp.data['paging']['next'].split('?')[1]))
            if next_params:
                try:
                    params.update(next_params)
                except AttributeError:
                    params = next_params
                self.next = functools.partial(self.request,method, path, params, headers)
            else:
                self.next = None
        except (KeyError, TypeError):
            self.next = None

        if RETURN_OBJECTS:  # and isinstance(data, dict):
            return Object(data)
        else:
            return data


    def group_info(self, groupid):
        """Get the description of a particular group.

           :param groupid: The group identifier.

           :Example:

           >>> s.group_info('489b848ee4b0ca4786945614')
           {
               "id":"489b848ee4b0ca4786945614",
               "name":"Group 1",
               "nameCI":"group 1",
               "description":"Group 1 description text",
               "path":[
                   "51f13454bc54518c7bae7d4d",
                   "50f13484b846618c7bae77b7"
               ],
               "billable":true,
               "bssId": "bss-48631656321"
           }

        """

        return self.request('GET', '/groups/' + groupid)


    def group_list(self, **kwargs):
        """Lists all children groups of your group.


           :param \**kwargs: Optional keyword arguments as described in the official
               documentation (`limit`, `offset`, `parentId`).

           >>> s.group_list()
           [
               {
                   "id":"510b848ee4b0ca47869752b5",
                   "name":"Group 1",
                   "nameCI":"group 1",
                   "description":"Group 1 description text",
                   "path":[
                        "51f13454bc54518c7bae7d4d",
                        "50f13484b846618c7bae77b7"
                   ],
                   "billable":true,
                   "bssId": "bss-48631656321"
                   },
                   { ... }
           ]

        """

        return self.request('GET', '/groups', params=kwargs)


    def devicetype_info(self,  devicetypeid):
        """Get the description of a particular device type.

           :param devicetypeid: The device type identifier.

           >>> s.devicetype_info('4d3091a05ee16b3cc86699ab')
           {
               "id" : "4d3091a05ee16b3cc86699ab",
               "name" : "Sigfox test device",
               "group" : "4d39a4c9e03e6b3c430e2188",
               "description" : "Little things in the black boxes",
               "keepAlive" : 0,
               "payloadType" : "Geolocation",
               "contract" : "523b1d10d777d3f5ae038a02"
           }

        """

        return self.request('GET', '/devicetypes/' + devicetypeid)


    def devicetype_edit(self, devicetypeid, changes):
        """Edit a device type.

           :param params: Dictionary of the format described in the
               official documentation

           >>> changes = {
           ...     "name" : "dtname",
           ...     "description" : "the description",
           ...     "keepAlive" : 3000,
           ...     "alertEmail" : "alert@email.com",
           ...     "payloadType" : "None",
           ...     "downlinkMode" : 0,
           ...     "downlinkDataString" : "deadbeefcafebabe",
           ... }
           >>> s.devicetype_edit(changes)

           .. note:: The `changes` parameter may already contain the
                     devicetype identifier (``id``) but it will be overridden
                     by `devicetypeid`.

        """

        changes.update({'id': devicetypeid})
        return self.request('POST', '/devicetypes/edit', params=changes)


    def devicetype_list(self):
        """Lists all device types available to your group.

           ..note:: ``includeSubGroups`` and ``contractInfoId`` are currently not supported.

           >>> s.devicetype_list()
           [
               {
                   "id" : "4d3091a05ee16b3cc86699ab",
                   "name" : "Sigfox test device",
                   "group" : "4d39a4c9e03e6b3c430e2188",
                   "description" : "Little things in the black boxes",
                   "keepAlive" : 7200,
                   "payloadType" : "None",
                   "contract" : "523b1d10d777d3f5ae038a02"
               },
               { ... }
           ]

        """

        return self.request('GET', '/devicetypes')


    def devicetype_errors(self, devicetypeid, **kwargs):
        """Get the communication down events for devices belonging to a device type.

           :param devicetypeid: The device type identifier.
           :param \**kwargs: Optional keyword arguments as described in the official
               documentation (`limit`, `offset`, `since` and `before`)

           >>> s.devicetype_errors('5256c4d6c9a871b80f5a2e50')
           [
               {
                   "deviceId" : "0235",
                   "time" : 1381410600026,
                   "message" : "No message received since 2013-10-08 15:36:21",
                   "severity" : "ERROR",
                   "deviceTypeId" : "5256c4d6c9a871b80f5a2e50",
                   "callbacks" : [
                       {
                           "url" : "http://host/path?id=0235&time=1381410600",
                           "status" : 600,
                           "info" : "Connection refused: host/path"
                       },
                       {
                           "subject" : "some subject",
                           "message" : "some messages",
                           "status" : 200
                       }
                   ]
               },
               { ... }
           ]

        """

        return self.request('GET', '/devicetypes/%s/status/error' % (devicetypeid),
                            params=kwargs)


    def devicetype_warnings(self, devicetypeid, **kwargs):
        """Get the network issues events that were sent for devices
           belonging to a device type.

           :param devicetypeid: The device type identifier.
           :param \**kwargs: Optional keyword arguments as described in the official
               documentation (`limit`, `offset`, `since` and `before`)

           See `Sigfox.devicetype_errors()` for example output.

        """

        return self.request('GET', '/devicetypes/%s/status/warn' % (devicetypeid),
                            params=kwargs)


#    def devicetype_gelocsconfig(self, groupid):
#        return self.request('GET', '/devicetypes/geolocs-config', params=groupid)

    def devicetype_messages(self, devicetypeid, **kwargs):
        """Get the messages that were sent by all the devices of a device type.

           :param devicetypeid: The device type identifier.
           :param \**kwargs: Optional keyword arguments as described in the official
               documentation (`limit`, `offset`, `since` and `before`)

           >>> s.devicetype_messages('5256c4d6c9a871b80f5a2e50')
           [
               {
                   "device" : "002C",
                   "time" : 1343321977,
                   "data" : "3235353843fc",
                   "snr" : "38.2",
                   "computedLocation": {
                     "lat" : 43.45,
                     "lng" : 6.54,
                     "radius": 500
                   },
                   "linkQuality" : "GOOD",
                   "downlinkAnswerStatus" : {
                       "data" : "1511000a00007894"
                    }
               },
               { ... }
           ]

           .. note:: The ``snr`` field is a string and not a float. This is what
                     the REST-API returns.

        """

        return self.request('GET', '/devicetypes/%s/messages' % (devicetypeid),
                            params=kwargs)


    def devicetype_disengage(self, devicetypeid):
        """Disengage sequence number check for next message of each device
           of the device type.

           :param devicetypeid: The device type identifier.

           >>> s.devicetype_disengage('5256c4d6c9a871b80f5a2e50')
           None

        """
        return self.request('GET', '/devicetypes/%s/disengage' % (devicetypeid))


    def callback_new(self, devicetypeid, callbacks):
        """Create new callbacks.

           :param callbacks: List of dictionaries as described in the official
               documentation.

           :Example:

           >>> new_callbacks = [
           ...     {
           ...         "channel" : "URL",
           ...         "callbackType" : 0,
           ...         "callbackSubtype" : 2,
           ...         "url" : "http://myserver.com/sigfox/callback",
           ...         "httpMethod" : "POST",
           ...         "enabled" : true,
           ...         "sendDuplicate" : false,
           ...         "sendSni": false,
           ...         "payloadConfig" : "var1::bool:1",
           ...         "bodyTemplate" : "device : {device} / {customData#var1}",
           ...         "headers" : {
           ...          "time" : "{time}"
           ...         },
           ...         "contentType" : "text/plain"
           ...     },
           ...     {
           ...         "channel" : "BATCH_URL",
           ...         "callbackType" : 0,
           ...         "callbackSubtype" : 2,
           ...         "url" : "http://myserver.com/sigfox/callback/batch",
           ...         "linePattern" : "{device};{data};",
           ...         "enabled" : true,
           ...         "sendDuplicate" : false,
           ...         "sendSni": false
           ...     }
           ... ]
           >>> s.callback_new('5256c4d6c9a871b80f5a2e50', new_callbacks)

        """

        return self.request('POST', '/devicetypes/%s/callbacks/new' % (devicetypeid),
                            params=callbacks)


    def callback_list(self, devicetypeid):
        """List the callbacks for a device type.

           :param devicetypeid: The device type identifier.

           >>> s.callback_list('5256c4d6c9a871b80f5a2e50')
           [
               {
                   "id" : "deadbeeffacecafebabecafe"
                   "channel" : "URL",
                   "callbackType" : 0,
                   "payloadConfig" : "int1::uint:8 int2::uint:8",
                   "callbackSubtype" : 0,
                   "urlPattern" : "http://myserver.com/sigfox/callback",
                   "httpMethod" : "POST",
                   "headers" : { "key1" : "value1",
                                 "key2" : "value2" },
                   "enabled" : true,
                   "sendDuplicate" : false,
                   "dead":false,
                   "downlinkHook":false
               },
               { ... }
           ]

        """

        return self.request('GET', '/devicetypes/%s/callbacks' % (devicetypeid))


    def callback_delete(self, devicetypeid, callbackid):
        """Delete a callback.

           :param devicetypeid: The device type identifier.
           :param callbackid: The callback identifier.

           >>> s.callback_delete('5256c4d6c9a871b80f5a2e50', 'deadbeeffacecafebabecafe')

        """

        return self.request('POST', '/devicetypes/%s/callbacks/%s/delete' %
                            (devicetypeid, callbackid))


    def callback_enable(self, devicetypeid, callbackid):
        """Enable a callback.

           :param devicetypeid: The device type identifier.
           :param callbackid: The callback identifier.

           >>> s.callback_enable('5256c4d6c9a871b80f5a2e50', 'deadbeeffacecafebabecafe')

        """

        return self.request('POST', '/devicetypes/%s/callbacks/%s/enable?enabled=true' %
                            (devicetypeid, callbackid))


    def callback_disable(self, devicetypeid, callbackid):
        """Disable a callback.

           :param devicetypeid: The device type identifier.
           :param callbackid: The callback identifier.

           >>> s.callback_disable('5256c4d6c9a871b80f5a2e50', 'deadbeeffacecafebabecafe')

        """

        return self.request('POST', '/devicetypes/%s/callbacks/%s/enable?enabled=false' %
                            (devicetypeid, callbackid))


    def callback_downlink(self, devicetypeid, callbackid):
        """Select a downlink callback.

           :param devicetypeid: The device type identifier.
           :param callbackid: The callback identifier.

           >>> s.callback_downlink('5256c4d6c9a871b80f5a2e50', 'deadbeeffacecafebabecafe')

        """

        return self.request('POST', '/devicetypes/%s/callbacks/%s/downlink' % (devicetypeid, callbackid))


    def callback_errors(self, **kwargs):
        """Returns device messages where at least one callback has failed.

           :param \**kwargs: Optional keyword arguments as described in the official
               documentation (`limit`, `offset`, `since`, `before`, `hexId`,
               `deviceTypeId`, `groupId`).

        """

        return self.request('GET', '/callbacks/messages/error', params=kwargs)


    def device_list(self, devicetypeid, **kwargs):
        """Lists the devices associated to a specific device type.

           :param devicetypeid: The device type identifier.
           :param \**kwargs: Optional keyword arguments as described in the official
               documentation (`snr`, `limit`, `offset`).

           >>> s.device_list('4d3091a05ee16b3cc86699ab', srn=1)         # 1 = for SNR values from 0 to 10 dB
           [
               {
                   "id" : "002C",
                   "name" : "Labege 4",
                   "type" : "4d3091a05ee16b3cc86699ab",
                   "last" : 1343321977,
                   "averageSignal": 8.065601,
                   "averageSnr": 8.065601,
                   "averageRssi": -122.56,
                   "state": 0,
                   "lat" : 43.45,
                   "lng" : 1.54,
                   "computedLocation": {
                       "lat" : 43.45,
                       "lng" : 6.54,
                       "radius": 500
                   },
                   "activationTime": 1404096340556,
                   "pac": "545CB3B17AC98BA4",
                   "tokenType": "CONTRACT",
                   "contractId": "7896541254789654aedfba4c",
                   "tokenEnd": 1449010800000,
                   "preventRenewal": false
               },
               { ... }
           ]

        """

        return self.request('GET', '/devicetypes/%s/devices' % (devicetypeid), params=kwargs)


    def device_info(self, deviceid):
        """Get information about a device.

           :param deviceid: The device identifier.

           >>> s.device_info('002C')
           {
               "id" : "002C",
               "name" : "Labege 4",
               "type" : "4d3091a05ee16b3cc86699ab",
               "last" : 1343321977,
               "averageSignal": 8.065601,
               "averageSnr": 8.065601,
               "averageRssi": -122.56,
               "state": 0,
               "lat" : 43.45,
               "lng" : 1.54,
               "computedLocation": {
                   "lat" : 43.45,
                   "lng" : 6.54,
                   "radius": 500
               },
               "activationTime": 1404096340556,
               "pac": "545CB3B17AC98BA4",
               "tokenType": "CONTRACT",
               "contractId": "7896541254789654aedfba4c",
               "tokenEnd": 1449010800000,
               "preventRenewal": false
           }

        """

        return self.request('GET', '/devices/%s' % (deviceid))


    def device_tokenstate(self, deviceid):
        """Get information about a device's token

           :param deviceid: The device identifier.

           >>> s.device_tokenstate('4d3091a05ee16b3cc86699ab')
           {
                "code" : 1,
                "detailMessage" : "Off contract",
                "tokenType": "CONTRACT",
                 "contractId": "7896541254789654aedfba4c",
                 "tokenEnd": 1418673953200,
            }

        """

        return self.request('GET', '/devices/%s/token-state' % (deviceid))

    def device_messages(self, deviceid, **kwargs):
        """Get the messages that were sent by a device.

           :param deviceid: The device identifier.
           :param \**kwargs: Optional keyword arguments as described in the official
               documentation (`before`, `since`, `limit`, `offset`).

           >>> s.device_messages('4d3091a05ee16b3cc86699ab', since=time.time()-60*60*24)    # Last 24 hours
           [
               {
                   "device" : "002C",
                   "time" : 1343321977,
                   "data" : "3235353843fc",
                   "snr" : "38.2",
                   "computedLocation": {
                       "lat" : 43.45,
                       "lng" : 6.54,
                       "radius": 500
                   },
                   "linkQuality" : "GOOD",
                   "downlinkAnswerStatus" : {
                       "data" : "1511000a00007894"
                   }
               },
               { ... }
           ]

           .. note:: The ``snr`` field is a string and not a float. This is what
                     the REST-API returns.

        """

        return self.request('GET', '/devices/%s/messages' % (deviceid), params=kwargs)

    def device_locations(self, deviceid, **kwargs):
        """Get the messages location.

           :param deviceid: The device identifier.
           :param \**kwargs: Optional keyword arguments as described in the official
               documentation (`before`, `since`, `limit`, `offset`).

           >>> s.device_locations('4d3091a05ee16b3cc86699ab', since=time.time()-60*60*24)    # Last 24 hours)
           [
               {
                   "time" : 1343321977000,
                   "valid" : true,
                   "lat" : 42.4631156,
                   "lng" : 1.5652321,
                   "radius" : 360,
               },
               { ... }
           ]

        """

        return self.request('GET', '/devices/%s/locations' % (deviceid), params=kwargs)

    def device_errors(self, deviceid, **kwargs):
        """Get the communication down events for a device.

           :param deviceid: The device identifier.
           :param \**kwargs: Optional keyword arguments as described in the official
               documentation (`before`, `since`, `limit`, `offset`).

           >>> s.device_errors('4830')
           [
               {
                   "deviceId" : "4830",
                   "time" : 1381300600026,
                   "message" : "No message received since 2013-10-08 15:36:21",
                   "severity" : "ERROR",
                   "deviceTypeId" : "5256c4d6c9a871b80f5a2e50",
                   "callbacks" : [
                       {
                           "url" : "http://host/path?id=4830&time=1381300600",
                           "status" : 200
                       },
                       {
                           "subject" : "some subject",
                           "message" : "some messages",
                           "status" : 200
                       }
                   ]
               },
               { ... }
           ]


        """

        return self.request('GET', '/devices/%s/status/error' % (deviceid), params=kwargs)

    def device_warnings(self, deviceid, **kwargs):
        """Get the network issues events that were sent for a device

           :param deviceid: The device identifier.
           :param \**kwargs: Optional keyword arguments as described in the official
               documentation (`before`, `since`, `limit`, `offset`).

           >>> s.device_warnings('4830')
           [
               {
                   "deviceIds" : [ "0235", "023A", "4830" ],
                   "time" : 1381410600026,
                   "message" : "Sigfox network experiencing issues [SIC]",
                   "severity" : "WARN",
                   "deviceTypeId" : "5256c4d6c9a871b80f5a2e50",
                   "callbacks" : [
                       {
                           "url" : "http://host/path?id=4830&time=1381410600",
                           "status" : 600,
                           "info" : "Connection refused: host/path"
                       },
                       {
                           "subject" : "some subject",
                           "message" : "some messages",
                           "status" : 200
                       }
                   ]
               },
               { ... }
           ]

        """

        return self.request('GET', '/devices/%s/status/warn' % (deviceid), params=kwargs)

    def device_networkstate(self, deviceid):
        """Return the network status for a specific device.

           :param deviceid: The device identifier.

           >>> s.device_networkstate('4830')
           {
               "networkStatus" : "NOK"
           }

        """

        return self.request('GET', '/devices/%s/networkstate' % (deviceid))

    def device_messagemetrics(self, deviceid):
        """Returns the total number of device messages for one device, this day, this week and this month.

           :param deviceid: The device identifier.

           >>> s.device_messagemetrics('4830')
           {
               "lastDay": 47,
               "lastWeek": 276,
               "lastMonth": 784
           }

        """

        return self.request('GET', '/devices/%s/messages/metric' % (deviceid))

    def device_consumptions(self, deviceid, year):
        """Get a Device's consumptions for a year.

           :param deviceid: The device identifier.
           :param year: The year, e.g. ``2017``.

           >>> s.device_consumptions('4830', 2017)
           {
               "consumption": {
                   "id" : "4830_2017",
                   "consumptions": [
                       {
                           "frameCount": 12,
                           "downlinkFrameCount": 3
                       },
                       { ... }
                   ]
               }
           }

           Each entry in ``consumption`` is the data for one day, starting with the
           1st of January.

        """

        return self.request('GET', '/devices/%s/consumptions/%s' % (deviceid, year))

    def coverage_redundancy(self, lat, lng, mode='INDOOR'):
        """Get base station redundancy for a given latitude and longitude.

           :param lat: The decimal latitude.
           :param lng: The decimal longitude.
           :param mode: Can be either ``INDOOR`` or ``OUTDOOR``.


           >>> s.coverage_redundancy(43.415, 1.9693, mode='OUTDOOR')
           {
               "redundancy":3
           }

        """

        params = {'lat': lat, 'lng': lng, 'mode': mode}
        return self.request('GET', '/coverages/redundancy', params=params)

    def coverage_predictions(self, lat, lng, mode='INDOOR'):
        """Get coverage levels for a given latitude and longitude.

           :param lat: The decimal latitude.
           :param lng: The decimal longitude.
           :param mode: Can be either ``INDOOR``, ``OUTDOOR`` or ``UNDERGROUND``.

           The return value contains the margins values (dB) for redundancy level 1, 2 and 3.

           >>> s.coverage_preedictions(43.415, 1.9693)
           {
               'margins': [48, 20, 7]
           }

        """

        params = {'lat': lat, 'lng': lng}
        return self.request('GET', '/coverages/global/predictions', params=params)

    def user_list(self, groupid, **kwargs):
        """Lists all users registered with a role associated to a specific group.

           :param groupid: The group identifier.
           :param \**kwargs: Optional keyword arguments as described in the official
               documentation (`limit`, `offset`).
           :returns: List of dictionaries with user details as returned in the
               ``data`` field of the REST-API response.

           .. note:: This method may result in multiple HTTP request to automatically
                     iterate through paged responses.

           List all users.

           >>> s.user_list(groupid)
           [ {"firstName" : "Michel",
              "lastName" : "Dupont",
              "email" : "michel.dupont@sigfox.com",
              "timezone" : "Europe/Paris",
              "creationTime" : 1392812363644,
              "creationDate" : "Wed Feb 19 13:19:23 CET 2014",
              "lastLogin" : 1448351837467,
              "lastLoginDate" : "Tue Nov 24 08:57:17 CET 2015",
              "userRoles" : [ {
                "group" : {
                  "id" : "babecafebabecafebabecafe",
                  "name" : "Root",
                  "nameCI" : "root",
                  "description" : "Master Group",
                  "path" : [ ],
                  "billable" : false
                  },
                "customRole" : {
                  "id" : "51d19e7ce4b067e859e4c2c1",
                  "name" : "SUPPORT_CORP"
                  }
                } ]
              },
              { ... } ]

           Only list users #10 to #20.

           >>> s.user_list(groupid, offset=10, limit=10)

        """

        kwargs.update({'groupId': groupid})
        return self.request('GET', '/users', params=kwargs)


__all__ = ['DEBUG', 'IGNORE_SSL_VALIDATION', 'Sigfox', '_dictasobj']
