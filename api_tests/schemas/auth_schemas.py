REGISTRATION_RESPONSE_SCHEMA = {
    'type': 'object',
    'required': [
        'id',
        'username',
        'email',
    ],
    'properties': {
        'id': {
            'type': 'integer',
        },
        'username': {
            'type': 'string',
        },
        'email': {
            'type': 'string',
        },
    },
    'additionalProperties': False,
}

TOKEN_RESPONSE_SCHEMA = {
    'type': 'object',
    'required': [
        'access',
        'refresh',
    ],
    'properties': {
        'access': {
            'type': 'string',
            'minLength': 1,
        },
        'refresh': {
            'type': 'string',
            'minLength': 1,
        },
    },
    'additionalProperties': False,
}

TOKEN_REFRESH_RESPONSE_SCHEMA = {
    'type': 'object',
    'required': [
        'access',
    ],
    'properties': {
        'access': {
            'type': 'string',
            'minLength': 1,
        },
    },
    'additionalProperties': False,
}