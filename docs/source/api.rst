python-sigfox  API
==================

.. note:: Currently only the features that are accessible as *LIMITED_ADMIN* are
          implemented.

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

User list by group
~~~~~~~~~~~~~~~~~~

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
.. automethod:: sigfoxapi.Sigfox.devicetype_gelocsconfig
.. automethod:: sigfoxapi.Sigfox.devicetype_messages
.. automethod:: sigfoxapi.Sigfox.devicetype_disengage

Devices
-------


Callbacks
---------


Coverage
--------



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
