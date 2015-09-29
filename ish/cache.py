import os
import time
import json


def needs_new(cache_file, max_age):
    try:
        mod_time = os.path.getmtime(cache_file)
        now = int(time.time())
        return (now - mod_time) > max_age

    except OSError:
        return True


def load_or(cache_file, otherwise, max_age=60):
    if not needs_new(cache_file, max_age):
        with open(cache_file) as cf:
            try:
                return json.loads(cf.read())
            except ValueError:
                pass

    with open(cache_file, 'w') as cf:
        new_data = otherwise()
        cf.write(json.dumps(new_data))
        return new_data
