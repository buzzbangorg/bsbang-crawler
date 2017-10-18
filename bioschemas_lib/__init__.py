MANDATORY_PROPERTIES = {
    'Thing': ['@type', 'name', 'url'],
    'DataCatalog': ['description', 'keywords'],
    'PhysicalEntity': ['additionalType']
}

SCHEMA_INHERITANCE_GRAPH = {
    'CreativeWork': 'Thing',
    'DataCatalog': 'CreativeWork',
    'PhysicalEntity': 'Thing',
    'Thing': None
}

SCHEMAS_TO_PARSE = ['DataCatalog', 'PhysicalEntity']

# If a type is not in the map, then assume the source and target names are the same
JSONLD_TO_SOLR_MAP = {'@type': 'AT_type'}
