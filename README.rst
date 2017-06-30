python-sigfoxapi
================

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

The example lists all devices belonging to a known device type ID. In this case
only a single device is returned.

.. code-block:: python

   >>> from sigfoxapi import Sigfox
   >>> s = Sigfox('mylogin', 'mypassword')
   >>> s.device_list(device_type_id)
   [{'state': 0, 'preventRenewal': True, 'name': 'Device 00112233',
     'activationTime': 1497905981832, 'tokenType': 'CONTRACT',
     'averageSnr': 39.503254, 'averageRssi': -104.20602,
     'averageSignal': 39.503254, 'contractId': '588123459058c25feb9d70b0',
     'lng': 0.0, 'id': '654321', 'tokenEnd': 1529441981832,
     'last': 1498135234, 'lat': 0.0, 'type': '5947b63241057463d724131c'}]

Documentation
-------------

The full documentation can be found at http://python-sigfoxapi.readthedocs.io/en/master/#.
