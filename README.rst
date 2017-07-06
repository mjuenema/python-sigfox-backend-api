python-sigfoxapi
================

.. image:: https://img.shields.io/pypi/v/sigfoxapi.svg?style=flat-square
   :target: https://pypi.python.org/pypi/sigfoxapi
   :alt: Version

.. image:: https://img.shields.io/github/license/mjuenema/python-sigfox-backend-api.svg?style=flat-square
   :target: https://opensource.org/licenses/BSD-2-Clause
   :alt: License

.. image:: https://img.shields.io/github/issues/mjuenema/python-sigfox-backend-api.svg?style=flat-square
   :target: https://github.com/mjuenema/python-sigfox-backend-api/issues
   :alt: Issues

.. image:: https://img.shields.io/travis/mjuenema/python-sigfox-backend-api/master.svg?style=flat-square
   :target: https://www.travis-ci.org/mjuenema/python-sigfox-backend-api/builds
   :alt: Travis-CI

.. image:: https://img.shields.io/codecov/c/github/mjuenema/python-sigfox-backend-api/master.svg?style=flat-square
   :target: https://codecov.io/gh/mjuenema/python-sigfox-backend-api
   :alt: Coverage

**python-sigfoxapi** is a Python wrapper for the Sigfox_ backend REST API. 

.. _Sigfox: https://www.sigfox.com

At this stage only features that are accessible with *LIMITED_ADMIN*
permissions have been implemented as I personally don't have full
access tp the REST-API.

* Groups (info, list).
* Device types (list, edit, errors, warnings, messages, disengage).
* Callbacks (list, new, delete, enable, disable, errors, downlink).
* Devices (info, list, tokenstate, messages, locations, errors, warnings,
  networkstate, message metrics, consumptions).
* Coverage (redundancy, predictions).
* Users (list)

For more details about the Sigfox backend REST API navigate to the *Group*
page in the Sigfox backend web interface, select a group, click on *REST-API*
and then on the *API documentation* link. The documentation is generated
automatically and tailored to the access permission of the logged-in user.

Example
-------

The example retrieves information about a device.

.. code-block:: python

   >>> from sigfoxapi import Sigfox
   >>> s = Sigfox('mylogin', 'mypassword')
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

It is also possible to have the ``Sigfox()`` methods return objects instead
of dictionaries by setting ``sigfoxapi.RETURN_OBJECTS`` to ``True``.

.. code-block:: python

   >>> sigfoxapi.RETURN_OBJECTS = True
   >>> device = s.device_info('002C')
   >>> device.averageRssi
   -122.56
   >>> device.computedLocation.lat
   43.45


Documentation
-------------

The full documentation can be found at http://python-sigfoxapi.readthedocs.io/en/master/#.
