Flask-request-args-parser
=========================

Python3 package implementing flask.request args parsing.

Table of Contents
-----------------

-  `Installiation`_
-  `Dependencies`_
-  `How to use`_
-  `Attributes definition`_
-  `Example of usage`_

Installiation
-------------

Using pip:

.. code:: bash

    pip install flask-request-args-parser

Dependencies
------------

-  `Flask`_

How to use
----------

Somewhere in your code:

.. code:: python

    def _param1_validator(v):
        if v <= 0:
            return None, '\'param1\' must be greater than 0'
        return v

    PARAMS = {
        'param_name_1': {
            'type': int,
            'default': 10,
            'validators': [
                _param1_validator,
                lambda v: v**2
            ],
            'locations': ['args'],
            'required': True,
        },
        'param_name_2': {
            # ...
        },
        'param_name_3': {} # just a param without any attributes
    }


    params = parse_params(PARAMS)
    param1 = params['param_name_1']

Attributes definition
---------------------

Order
~~~~~

The order checking attributes is: 1. ```locations```_ 1. ```required```_
1. ```type```_ 1. ```default```_ 1. ```validators```_

``locations``
~~~~~~~~~~~~~

| Type: ``list[str]``
| Default: ``['args','json']``
| This attribute tells where to look for a param. Possible locations:
  ``'args' | 'json' | 'headers' | 'cookies'``.
| You can combine locations: ``'locations': ['args', 'headers']``.

``required``
~~~~~~~~~~~~

| Type: ``bool``
| If ``required`` is ``True`` and param is missing in given
  ``locations``, Flask will ``abort`` with ``400``,
  ``Missing required param: <param_name> in <locations>.``.

``type``
~~~~~~~~

| Type: ``class``
| If ``type`` is specified, parser will try to convert param into given
  type. Otherwise Flask will ``abort`` with ``400``,
  ``Invalid param type: <param_name> must be <param_type>, not <input_type>.``.

``default``
~~~~~~~~~~~

| Type: ``object``
| If param isn’t required and it is not listed in required locations the
  ``default`` value will be assigned to this param.

``validators``
~~~~~~~~~~~~~~

Type: ``list[function | lambda]`` If param has ``validators``, the input
param value will go through all validators in given order and return
value of last given validator will be assigned to this param. If at
least one of validators returns None and error message, Flask will
``abort`` with ``400``, ``Invalid <param_name> param: <>.``. Here is the
illustration:

.. code:: python

    def v1(v): 
        if v%2!=0:
            return None, 'must be even'
        return v
        
    def v2(v):
        if v <= 0:
            return None, 'must be positive'
        return v

    def v3(v):
        return v + 1
        
    PARAMS = {
        'p1': {
            'type': int,
            'validators': [v1, v2, v3]
        }
    }

    params = parse_params(PARAMS)

This validation will return ``v3(v2(v1(<input_param>)))``

Example of usage
----------------

\`\`\`python from flask\_restful import Resource from
flask\_request\_args\_parser import parse\_params

def \_limit\_validator(v): if not 0 <= v <= 100: return None, ‘'limit'
must be in [0, 100]’ return v

def \_split\_v

.. _Installiation: #installiation
.. _Dependencies: #dependencies
.. _How to use: #how-to-use
.. _Attributes definition: #attributes-definition
.. _Example of usage: #example-of-usage
.. _Flask: http://flask.pocoo.org
.. _``locations``: #locations
.. _``required``: #required
.. _``type``: #type
.. _``default``: #default
.. _``validators``: #validators
