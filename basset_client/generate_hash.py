from __future__ import absolute_import, division, print_function, unicode_literals

import hashlib


def generate_file_hash(filename):
    hash = hashlib.sha1()
    memory_view = memoryview(bytearray(128 * 1024))
    with open(filename, 'rb', buffering=0) as file:
        for n in iter(lambda: f.readinto(memory_view), 0):
            hash.update(memory_view[:n])
    return hash.hexdigest()


def generate_hash(content):
    hash = hashlib.sha1()
    hash.update(content)
    return hash.hexdigest()