python-sigfox  API
==================

.. note:: Currently only the features that are accessible as *LIMITED_ADMIN* are
          implemented.

This page describes the API of the **python-sigfox** package. All code
examples have been copied from the official documentation.

The sigfoxapi module
--------------------

.. autodata:: sigfoxapi.DEBUG
.. autodata:: sigfoxapi.IGNORE_SSL_VALIDATION
.. autodata:: sigfoxapi.RETURN_OBJECTS

Exceptions
----------

.. autoclass:: sigfoxapi.SigfoxApiError
.. autoclass:: sigfoxapi.SigfoxApiBadRequest
.. autoclass:: sigfoxapi.SigfoxApiAuthError
.. autoclass:: sigfoxapi.SigfoxApiAccessDenied
.. autoclass:: sigfoxapi.SigfoxApiNotFound
.. autoclass:: sigfoxapi.SigfoxApiServerError

The Sigfox class
----------------

.. autoclass:: sigfoxapi.Sigfox

Users
-----

user_list
~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.user_list

Groups
------

group_info
~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.group_info


group_list
~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.group_list

Device types
------------

devicetype_edit
~~~~~~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.devicetype_edit

devicetype_list
~~~~~~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.devicetype_list

devicetype_errors
~~~~~~~~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.devicetype_errors

devicetype_warnings
~~~~~~~~~~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.devicetype_warnings

devicetype_messages
~~~~~~~~~~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.devicetype_messages

devicetype_disengage
~~~~~~~~~~~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.devicetype_disengage

Devices
-------

device_list
~~~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.device_list

device_info
~~~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.device_info

device_tokenstate
~~~~~~~~~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.device_tokenstate

device_messages
~~~~~~~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.device_messages

device_locations
~~~~~~~~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.device_locations

device_errors
~~~~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.device_errors

device_warnings
~~~~~~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.device_warnings

devices_networkstate
~~~~~~~~~~~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.device_networkstate

device_messagemetrics
~~~~~~~~~~~~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.device_messagemetrics

device_consumptions
~~~~~~~~~~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.device_consumptions

Callbacks
---------

callback_new
~~~~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.callback_new

callback_list
~~~~~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.callback_list

callback_delete
~~~~~~~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.callback_delete

callback_enable
~~~~~~~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.callback_enable

callback_disable
~~~~~~~~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.callback_disable

callback_downlink
~~~~~~~~~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.callback_downlink

callback_errors
~~~~~~~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.callback_errors


Coverage
--------

coverage_redundancy
~~~~~~~~~~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.coverage_redundancy

coverage_predictions
~~~~~~~~~~~~~~~~~~~~

.. automethod:: sigfoxapi.Sigfox.coverage_predictions

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
