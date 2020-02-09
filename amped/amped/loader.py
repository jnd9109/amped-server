import json
import os
from django.core.exceptions import ImproperlyConfigured


_conf = {}
_conf_path = os.path.join(os.path.dirname(__file__), 'conf.json')
if os.path.exists(_conf_path):
    with open(_conf_path) as f:
        _secrets = json.loads(f.read())


def load_credential(key, default=None):
    if key in os.environ:
        return os.environ[key]
    elif key in _secrets:
        return _secrets[key]
    else:
        return default
