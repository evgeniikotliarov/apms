import json
import os


def load(name):
    with open("{}/fixtures.json".format(os.path.dirname(__file__), ), 'r') as file:
        schema = json.load(file)
    return schema[name]


def load_instance(name, class_type):
    instance = class_type()

    for field, value in load(name).items():
        setattr(instance, field, value)
    return instance
