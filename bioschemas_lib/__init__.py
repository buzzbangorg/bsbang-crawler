MANDATORY_PROPERTIES = {
    'Thing': ['identifier', 'name', 'url'],
    'PhysicalEntity': ['additionalType']
}

SCHEMA_INHERITANCE_GRAPH = {
    'CreativeWork': 'Thing',
    'DataCatalog': 'CreativeWork',
    'PhysicalEntity': 'Thing',
    'Thing': None
}

SCHEMAS_TO_PARSE = ['DataCatalog', 'PhysicalEntity']
