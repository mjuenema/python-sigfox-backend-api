python-sigfox  API
==================

.. note:: Currently only the features that are accessible as *LIMITED_ADMIN* are
          implemented.

This page describes the API of the **python-sigfox** package. All code
examples have been copied from the official documentation.

Importing the module
--------------------

.. code-block:: python

   >>> from sigfoxapi import Sigfox

The Sigfox class
----------------

.. autoclass:: sigfoxapi.Sigfox
.. code-block:: python

   >>> s = Sigfox('1234567890abcdef', 'fedcba09876543221')

Users
-----

.. automethod:: sigfoxapi.Sigfox.user_list

Groups
------

.. automethod:: sigfoxapi.Sigfox.group_info
.. automethod:: sigfoxapi.Sigfox.group_list

Device types
------------

.. automethod:: sigfoxapi.Sigfox.devicetype_edit
.. automethod:: sigfoxapi.Sigfox.devicetype_list
.. automethod:: sigfoxapi.Sigfox.devicetype_errors
.. automethod:: sigfoxapi.Sigfox.devicetype_warnings
.. automethod:: sigfoxapi.Sigfox.devicetype_messages
.. automethod:: sigfoxapi.Sigfox.devicetype_disengage

Devices
-------

.. automethod:: sigfoxapi.Sigfox.device_list
.. automethod:: sigfoxapi.Sigfox.device_info
.. automethod:: sigfoxapi.Sigfox.device_tokenstate
.. automethod:: sigfoxapi.Sigfox.device_messages
.. automethod:: sigfoxapi.Sigfox.device_locations
.. automethod:: sigfoxapi.Sigfox.device_errors
.. automethod:: sigfoxapi.Sigfox.device_warnings
.. automethod:: sigfoxapi.Sigfox.device_networkstate
.. automethod:: sigfoxapi.Sigfox.device_messagemetrics
.. automethod:: sigfoxapi.Sigfox.device_consumptions

Callbacks
---------

.. automethod:: sigfoxapi.Sigfox.callback_new
.. automethod:: sigfoxapi.Sigfox.callback_list
.. automethod:: sigfoxapi.Sigfox.callback_delete
.. automethod:: sigfoxapi.Sigfox.callback_enable
.. automethod:: sigfoxapi.Sigfox.callback_disable
.. automethod:: sigfoxapi.Sigfox.callback_downlink
.. automethod:: sigfoxapi.Sigfox.callback_errors


Coverage
--------

.. automethod:: sigfoxapi.Sigfox.coverage_redundancy
.. automethod:: sigfoxapi.Sigfox.coverage_predictions

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
