import bioschemas_lib


def create_solr_json_with_mandatory_properties(schema, jsonld):
    """
    Create JSON we can put into Solr from the Bioschemas JsonLD

    :param schema:
    :param jsonld:
    :return:
    """
    solr_json = {}

    if schema in bioschemas_lib.MANDATORY_PROPERTIES:
        for prop in bioschemas_lib.MANDATORY_PROPERTIES[schema]:
            print('Adding "%s":"%s" for %s' % (prop, jsonld[prop], schema))
            solr_json[prop] = jsonld[prop]

    parent_schema = bioschemas_lib.SCHEMA_INHERITANCE_GRAPH[schema]
    if parent_schema is not None:
        solr_json.update(create_solr_json_with_mandatory_properties(parent_schema, jsonld))

    return solr_json
