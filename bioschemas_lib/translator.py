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
        for prop_name in bioschemas_lib.MANDATORY_PROPERTIES[schema]:
            if prop_name in bioschemas_lib.JSONLD_TO_SOLR_MAP:
                solr_prop_name = bioschemas_lib.JSONLD_TO_SOLR_MAP[prop_name]
            else:
                solr_prop_name = prop_name

            print(
                'Adding key "%s" -> "%s" for %s, value "%s"'
                % (prop_name, solr_prop_name, jsonld[prop_name], schema))

            solr_json[solr_prop_name] = jsonld[prop_name]

    parent_schema = bioschemas_lib.SCHEMA_INHERITANCE_GRAPH[schema]
    if parent_schema is not None:
        solr_json.update(create_solr_json_with_mandatory_properties(parent_schema, jsonld))

    return solr_json
