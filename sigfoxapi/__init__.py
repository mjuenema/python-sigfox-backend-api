"""
Python wrapper for the Sigfox backend REST API.

Inspired by https://pypi.python.org/pypi/pySigfox.

(c) 2017 Markus Juenemann

"""

__name__ = 'sigfoxapi'
__version__ = '0.0.1'
__license__ = 'BSD 2-clause "Simplified" License'

SIGFOX_API_URL = 'https://backend.sigfox.com/api/'

import drest
import drest.serialization

IGNORE_SSL_VALIDATION = False
DEBUG = False


# TODO: handle paged responses


class Sigfox(object):
    """Interact with the Sigfox backend API.

       :param login: Login as shown on the *Group* - *REST API* pacge of the
                     Sigfox backend web interface.
       :param password: Password as shown on the *Group* - *REST API* pacge of the
                     Sigfox backend web interface.

       >>> s = Sigfox('1234567890abcdef', 'fedcba09876543221')

       To enable debugging and show the HTTP requests and responses set the global
       variable `sigfox.DEBUG` to ``True``.

       >>> sigfox.DEBUG = True

       In case of SSL problems the global variable `sigfox.IGNORE_SSL_VALIDATION`
       can be set to ``True``.

       >>> sigfox.IGNORE_SSL_VALIDATION = True

    """

    def __init__(self, login, password):
        self.api = drest.API(SIGFOX_API_URL, debug=DEBUG,
                             serialization_handler=drest.serialization.JsonSerializationHandler,
                             serialize=True,
                             deserialize=True,
                             ignore_ssl_validation=IGNORE_SSL_VALIDATION,
                             trailing_slash=False)
        self.api.auth(login, password)


    def request(self, method, path, params=None, headers=None):
        """Perform HTTP(S) request and return response data.

           The response data will already have been serialized to a dictionary because
           of ``serialization_handler=drest.serialization.JsonSerializationHandler``.

           :param method: The HTTP method to use.
           :param params: Any parameters to be send to the resource.
           :param headers: Any headers to be send to the resource.

        """

        resp = self.api.make_request(method, path, params=params, headers=headers)

        try:
            return resp.data['data']
        except (KeyError, TypeError):
            return resp.data


    def group_info(self, groupid):
        """Get the description of a particular group.

           :param groupid: The group identifier.

        """

        return self.request('GET', '/groups/'+groupid)


    def group_list(self):
        """Lists all children groups of your group.

        """

        return self.request('GET', '/groups')


    def devicetype_edit(self, params):
        """Edit a device type.

           :param params: Dictionary of the format described in the
               official documentation

        """

        self.request('POST', '/devicetypes/edit', params=params)
        return self.info(devicetypeid)


    def devicetype_list(self):
        """Lists all device types available to your group.

        """

        return self.request('GET', '/devicetypes')


    def devicetype_errors(self, devicetypeid):
        """Get the communication down events for devices belonging to a device type.

           :param devicetypeid: The device type identifier.

        """

        return self.request('GET', '/devicetypes/%s/status/error' % (devicetypeid))


    def devicetype_warnings(self, devicetypeid):
        """Get the network issues events that were sent for devices
           belonging to a device type.

           :param devicetypeid: The device type identifier.

        """

        return self.request('GET', '/devicetypes/%s/status/warn' % (devicetypeid))


#    def devicetype_gelocsconfig(self, groupid):
#        return self.request('GET', '/devicetypes/geolocs-config', params=groupid)

    def devicetype_messages(self, devicetypeid):
        """Get the messages that were sent by all the devices of a device type.

           :param devicetypeid: The device type identifier.

        """

        return self.request('GET', '/devicetypes/%s/messages' % (devicetypeid))


    def devicetype_disengage(self, devicetypeid):
        """Disengage sequence number check for next message of each device
           of the device type.

           :param devicetypeid: The device type identifier.

        """
        return self.request('GET', '/devicetypes/%s/disengage' % (devicetypeid))


    def callback_new(self, devicetypeid, callbacks):
        """Create new callbacks.


           :param callbacks: List of dictionaries as described in the official
               documentation.

        """

        return self.request('POST', '/devicetypes/%s/callbacks/new' % (devicetypeid),
                            params=callbacks)


    def callback_list(self, devicetypeid):
        """List the callbacks for a device type.

           :param devicetypeid: The device type identifier.

        """

        return self.request('GET', '/devicetypes/%s/callbacks' % (devicetypeid))


    def callback_delete(self, devicetypeid, callbackid):
        """Delete a callback.

           :param devicetypeid: The device type identifier.
           :param callbackid: The callback identifier.

        """

        return self.request('POST', '/devicetypes/%s/callbacks/%s/delete' %
                            (devicetypeid, callbackid))


    def callback_enable(self, devicetypeid, callbackid):
        """Enable a callback.

           :param devicetypeid: The device type identifier.
           :param callbackid: The callback identifier.

        """

        return self.request('POST', '/devicetypes/%s/callbacks/%s/enable?enabled=true' %
                            (devicetypeid, callbackid))


    def callback_disable(self, devicetypeid, callbackid):
        """Disable a callback.

           :param devicetypeid: The device type identifier.
           :param callbackid: The callback identifier.

        """

        return self.request('POST', '/devicetypes/%s/callbacks/%s/enable?enabled=false' %
                            (devicetypeid, callbackid))


    def callback_downlink(self, devicetypeid, callbackid):
        """Select a downlink callback.

           :param devicetypeid: The device type identifier.
           :param callbackid: The callback identifier.

        """

        return self.request('POST', '/devicetypes/%s/callbacks/%s/downlink' % (devicetypeid, callbackid))


    def callback_errors(self, **kwargs):
        """Returns device messages where at least one callback has failed.

           :param \**kwargs: Optional keyword arguments as described in the official
               documentation (`limit`, `offset`, `since`, `before`, `hexId`,
               `deviceTypeId`, `groupId`).

        """

        return self.request('GET', '/api/callbacks/messages/error', params=params)


    def device_list(self, devicetypeid, **kwargs):
        """Lists the devices associated to a specific device type.

           :param devicetypeid: The device type identifier.
           :param \**kwargs: Optional keyword arguments as described in the official
               documentation (`snr`, `limit`, `offset`).

        """

        return self.request('GET', '/devicetypes/%s/devices' % (devicetypeid), params=params)


    def device_info(self, deviceid):
        """Get information about a device.

           :param deviceid: The device identifier.

        """

        return self.request('GET', '/devices/%s' % (deviceid))


    def device_tokenstate(self, deviceid):
        return self.request('GET', '/devices/%s/token-state' % (deviceid))

    def device_messages(self, deviceid, **params):
        return self.request('GET', '/devices/%s/messages' % (deviceid), params=params)

    def device_locations(self, deviceid, **params):
        return self.request('GET', '/devices/%s/locations' % (deviceid), params=params)

    def device_errors(self, deviceid, **params):
        return self.request('GET', '/devices/%s/status/error' % (deviceid), params=params)

    def device_warnings(self, deviceid, **params):
        return self.request('GET', '/devices/%s/status/warn' % (deviceid), params=params)

    def device_networkstate(self, deviceid):
        return self.request('GET', '/devices/%s/networkstate' % (deviceid))

    def device_messagemetrics(self, deviceid):
        return self.request('GET', '/devices/%s/messages/metric' % (deviceid))

    def device_consumptions(self, deviceid, year):
        return self.request('GET', '/devices/%s/consumptions/%s' % (deviceid, year))

    def coverage_redundancy(self, lat, lng, mode='INDOOR'):
        params = {'lat': lat, 'lng': lng, 'mode': mode}
        return self.request('GET', '/coverages/redundancy', params=params)

    def coverage_predictions(self, lat, lng):
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

           .. todo:: Actually implement iterating through paged responses!

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

        return self.request('GET', '/users/%s' % (groupid), params=params)


__all__ = ['DEBUG', 'IGNORE_SSL_VALIDATION', '__name__',
           '__version__', '__license__', 'Sigox']
