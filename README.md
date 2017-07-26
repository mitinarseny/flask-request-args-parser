# flask-request-args-parser
This is a Pyhton3 package, that implements flask.request args parsing.

## Installiation
```bash
pip install flask-request-args-parser
```
## Dependencies
* [Flask](http://flask.pocoo.org)
## How to use
Somewhere in your code:
```python
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
```
## Attributes definition

### Order
The order checking attributes is:
1. [`locations`](#locations)
1. [`required`](#required)
1. [`type`](#type)
1. [`default`](#default)
1. [`validators`](#validators)

### `locations`
Type: `list[str]`  
Default: `['args','json']`  
This attribute tells where to look for a param.
Possible locations: `'args' | 'json' | 'headers' | 'cookies'`.  
You can combine locations: `'locations': ['args', 'headers']`.  

### `required`
Type: `bool`  
If `required` is `True` and param is missing in given `locations`, Flask will `abort` with `400`, `Missing required param: <param_name> in <locations>.`.
    
### `type`
Type: `class`  
If `type` is specified, parser will try to convert param into given type. Otherwise Flask will `abort` with `400`, `Invalid param type: <param_name> must be <param_type>, not <input_type>.`.

### `default`
Type: `object`  
If param isn't required and it is not listed in required locations the `default` value will be assigned to this param.

### `validators`  
Type: `list[function | lambda]`
If param has `validators`, the input param value will go through all validators in given order and return value of last given validator will be assigned to this param. If at least one of validators returns None and error message, Flask will `abort` with `400`, `Invalid <param_name> param: <>.`. Here is the illustration:
```python
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
```
This validation will return `v3(v2(v1(<input_param>)))`  

## Example of usage
```python
from flask_restful import Resource
from flask_request_args_parser import parse_params


def _limit_validator(v):
    if not 0 <= v <= 100:
      return None, '\'limit\' must be in [0, 100]'
    return v

def _split_validator(v):
    return v.split(',')


class R(Resource):

    PARAMS = {
        'GET': {
            'limit': {
                'type': int,
                'default': 20,
                'valudators: [_limit_validator],
                'locations': ['args']
            },
            'ids': {
                'type': str,
                'validators': [
                    _split_validator,
                    lambda v: list(map(int,v))
                ],
                'locations': ['args']
            }
        },
        'POST': {
            'headline': {
                'type': str,
                'vaildators': [
                    lambda v: v.lower(),
                ],
                'locations': ['json']
            }
        }
    }

    def get(self):
        params = parse_params(self.PARAMS['GET'])
        limit = params['limit']
        # do smth
        return {'response': limit}

    def post(self):
        params = parse_params(self.PARAMS['POST'])
        headline = params['headline']
        # do smth
        return {
            'response': {
                'headline': headline
            }
        }
```
