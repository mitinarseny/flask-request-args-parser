# flask-request-args-parser
This is a pyhton package, that implements flask.request args parsing.
## Installiation
```bash
pip install flask-request-args-parser
```
## How to use
```python
form flask_restful import Resource
from flask_request_args_parser import parse_params


def _number_validator(v):
    if not 0 <= v <= 100:
      return None, '\'limit\' must be in [0, 100]'
    return v

def _split_validator(v):
    return v.split(',')


class R(Resource):

    PARAMS = {
        'GET': {
            'n': {
                'type': int,
                'default': 10,
                'valudators: [_number_validator, ],
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
        n = params['n']
        return {'response': n}

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
