# flask-request-args-parser
This is a pyhton package, that implements flask.request args parsing.
## Installiation
```bash
pip install flask-request-args-parser
```
## How to use
Somewhere in your code:
```python
# ...
def _param1_validator(v):
    if v <= 0:
        return None, '\'param1\' must be greater than 0' # return None and error message if input value 'v' is not valid
    return v # return any value that will be assigned to param, that is being validated
PARAMS = {
    'param_name_1': { # replace it with your str param_name
        'type': int, # or any other class
        'default': 10, # or any other value with satisfying 'type' field
        'validators': [ # list your validators here
            _param1_validator,
            lambda v: v**2,
        ],
        'locations': ['args'], # default locations are ['args', 'json']; possible locations are 'args', 'json', 'headers' and 'cookies'
        'required': True, # default is False
    },
    'param_name_2': {
        # ...
    }
}
params = parse_params(PARAMS)
param1 = params['param_name_1']
```
### `required`
If param is required Flask will abort with code 400 and message: 'Missing required param: \'<param_name>\' in <locations>'
### `type`
If param can't be converted to its `type` field Flask will abort with code 400 and message: 'Invalid param type: \'<param_name>\' must be \'<param_type>\', not \'got_type\''
### `default`
If param isn't required and it is not listed in required locations the default value will be assigned to this param
### ---------------
## Example
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
                'valudators: [_limit_validator, ],
                'locations': ['args', ]
            },
        },
        'POST': {
            's': {
                'type': str,
                'default': '1,2,3',
                'vaildators': [
                    _split_validator,
                    lambda v: list(map(int, v)),
                ],
                'locations': ['json', ]
            },
            'h': {
                'locations': ['headers',]
            }
        }
    }

    def get(self):
        params = parse_params(self.PARAMS['GET'])
        limit = params['limit']
        return {'response': limit}

    def post(self):
        params = parse_params(self.PARAMS['POST'])
        s = params['s']
        h = params['h']
        return {
            'response': {
                's': s,
                'h': h
            }
        }
```
