import re

def camel_case_to_underscore(string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def stupid_pluralize(string):
    return string + "s"

def table_name(cls):
    return stupid_pluralize(camel_case_to_underscore(cls.__name__))
