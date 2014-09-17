import json
def schematodefault(schema):
    data={}
    if 'properties' in schema:
        for key in schema['properties']:
            data[key]=schematodefault(schema['properties'][key])
        return data
    elif 'default' in schema:
        return schema['default']
    else:
        return ""