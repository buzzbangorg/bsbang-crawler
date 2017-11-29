DEFAULT_CONFIG = {

    # The properties that must exist on schemas for us to accept them for indexing
    'mandatory_properties': {
        'Thing': ['@type', 'name', 'url'],
        'DataCatalog': ['description', 'keywords'],
        'PhysicalEntity': ['additionalType']
    },

    # The properties that will be indexed if present
    'optional_properties': {
        'Thing': ['alternateName']
    },

    # The inheritance graph of the schemas that we care about
    'schema_inheritance_graph': {
        'CreativeWork': 'Thing',
        'DataCatalog': 'CreativeWork',
        'PhysicalEntity': 'Thing',
        'Thing': None
    },

    # The schemas that we want to index
    'schemas_to_parse': ['DataCatalog', 'PhysicalEntity'],

    # To capture older Bioschemas markup, we want to map some older schemas onto newer ones
    'schema_map': {'BiologicalEntity': 'PhysicalEntity'},

    # If a type is not in the map, then assume the source and target names are the same
    'jsonld_to_solr_map': {'@type': 'AT_type'},
}
