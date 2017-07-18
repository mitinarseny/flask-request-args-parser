from flask import abort, request
from werkzeug.datastructures import MultiDict


def _get_locations():
    params = {
        'args': None,
        'json': None,
        'headers': None,
        'cookies': None,
    }
    if request.args:
        params['args'] = request.args.copy()
    if request.get_json():
        params['json'] = request.get_json()
    if request.headers:
        pass
        # params['headers'] = request.headers.copy()
    if request.cookies:
        pass
        # params['cookies'] = request.cookies.copy()
    return params


def _get_params(all_params, locations):
    params = {}
    for l in locations:
        if all_params[l]:
            if isinstance(all_params[l], dict):
                params.update(all_params[l])
            elif isinstance(all_params[l], MultiDict):
                params.update(all_params[l].to_dict())
    return params


def _check_required(param_name, resolved_params, params, locations):
    if resolved_params[param_name].get('required') and param_name not in params:
        return abort(
            400,
            'Missing required param: \'{}\' in {}.'.format(
                param_name, ', '.join(locations))
        )


def _check_type(param_name, resolved_params, params):
    if 'type' in resolved_params[param_name]:
        try:
            return resolved_params[param_name]['type'](params[param_name])
        except (ValueError, TypeError):
            return abort(
                400,
                'Invalid param type: \'{}\' must be \'{}\', not \'{}\'.'.format(
                    param_name,
                    resolved_params[param_name]['type'].__name__,
                    params[param_name].__class__.__name__
                )
            )
    else:
        return params[param_name]


def _check_validators(param_name, params, validators):
    for v in validators:
        validation = v(params[param_name])
        if not isinstance(validation, tuple):
            if validation is None:
                return abort(
                    400,
                    'Invalid \'{param_name}\' param: \'{param_val}\'.'.format(
                        param_name=param_name,
                        param_val=params[param_name]
                    )
                )
            return validation
        elif validation[0] is None:
            return abort(
                400,
                'Invalid \'{param_name}\' param: \'{param_val}\': {msg}.'.format(
                    param_name=param_name,
                    param_val=params[param_name],
                    msg=validation[1]
                )
            )
        else:
            return validation[0]
    return params[param_name]


def parse_params(resolved_params):
    parsed_params = {}
    all_params = _get_locations()
    for param_name in resolved_params:
        locations = resolved_params[param_name].get(
            'locations', ['args', 'json'])
        params = _get_params(all_params, locations)
        _check_required(param_name, resolved_params, params, locations)
        if param_name in params:
            parsed_params[param_name] = _check_type(
                param_name, resolved_params, params)
        elif 'default' in resolved_params[param_name]:
            parsed_params[param_name] = resolved_params[param_name]['default']
        if param_name in parsed_params:
            parsed_params[param_name] = _check_validators(param_name, parsed_params,
                                                          resolved_params[param_name].get('validators', []))
    return parsed_params
