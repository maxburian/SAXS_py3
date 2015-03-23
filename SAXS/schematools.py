import json
def schematodefault(schema):
    data={}
    if 'properties' in schema:
        for key in schema['properties']:
            if "required" in schema['properties'][key] and schema['properties'][key]["required"]:
                data[key]=schematodefault(schema['properties'][key])
        return data
    elif 'default' in schema:
        return schema['default']
    elif schema["type"]=="array":
        if "minItems" in schema:
            array=[]
            for i in range(schema['minItems']):
                array.append(schematodefault(schema['items']))
            return array
        else:
            return []
    else:
        return ""