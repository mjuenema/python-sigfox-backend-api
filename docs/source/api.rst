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

.. automethod:: sigfoxapi.Sigfox.user_list

.. code-block:: python

   # List all users.
   >>> s.user_list(groupid)
   # TODO

Groups
------

.. automethod:: sigfoxapi.Sigfox.group_info

.. code-block:: python

   >>> s.group_info(groupid)
   {'billable': True,
    'description': 'Some Group',
    'id': '5947bc1150057463d724131a',
    'name': 'Some Group',
    'nameCI': 'some group',
    'path': ['588b8b9e5005743eec66391f',
             '588b8b9e5005743eec663909',
             '5491afbe9336a3d6154fee03',
             'deadbeeffacecafebabecafe',
             'babecafebabecafebabecafe']}

.. automethod:: sigfoxapi.Sigfox.group_list

.. code-block:: python

   >>> s.group_list()
   []

Device types
------------


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
