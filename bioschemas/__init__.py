# The properties that must exist on schemas for us to accept them for indexing
MANDATORY_PROPERTIES = {
    'Thing': ['@type', 'name', 'url'],
    'DataCatalog': ['description', 'keywords'],
    'PhysicalEntity': ['additionalType']
}

# The properties that will be indexed if present
OPTIONAL_PROPERTIES = {
    'Thing': ['alternateName']
}

# The inheritance graph of the schemas that we care about
SCHEMA_INHERITANCE_GRAPH = {
    'CreativeWork': 'Thing',
    'DataCatalog': 'CreativeWork',
    'PhysicalEntity': 'Thing',
    'Thing': None
}

# The schemas that we want to index
SCHEMAS_TO_PARSE = ['DataCatalog', 'PhysicalEntity']

# If a type is not in the map, then assume the source and target names are the same
JSONLD_TO_SOLR_MAP = {'@type': 'AT_type'}
