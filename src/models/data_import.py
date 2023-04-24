base = {
    "version": "0.7.1",
    "graph":{
        "nodes":[],
        "relationships":[]
    },
    "dataModel":{
        "fileModel":{
            "fileSchemas":{

            }
        },
        "graphModel":{
            "nodeSchemas":{

            },
            "relationshipSchemas":{
            }
        },
        "mappingModel":{
            "nodeMappings":{
            },
            "relationshipMappings":{
            }
        },
        "configuration":{
            "idsToIgnore":[],
        }
    }
}

def cleaned_property_value(value):
    if value in ["integer", "float", "datetime", "boolean"]:
        return value
    return "string"

def convert_from_arrows(arrows_json: dict) -> dict:
    # Converts an Arrows JSON file to a data-importer JSON file
    # Returns a dict

    # TODO: Flag warnings
    result = base

    # Convert nodes 
    converted_nodes = {}
    converted_node_positions = []
    node_mappings = {}
    nodes = arrows_json['nodes']
    for node in nodes:
        nid = node.get('id', None)
        if nid is None:
            continue
        converted_nodes[nid] = {
            "key":{
                "name": "",
                "properties":[]
            },
            "label": node.get('caption', None),
            "labelProperties": node.get('properties', None),
            "properties":[{} for prop in node.get('properties', [])],
            "additionalLabels": [
            
            ],
        }
        converted_node_positions.append({
            "caption":node.get('caption', None),
            "id": nid,
            "position":{
                "x":node.get('position', {}).get('x', None),
                "y":node.get('position', {}).get('y', None)
            }
        }) 
        node_mappings[nid] = {
            "nodeSchema":nid,
            "mappings":[]
        } 
    result["dataModel"]["graphModel"]["nodeSchemas"] = converted_nodes
    result["graph"]["nodes"] = converted_node_positions
    result["dataModel"]["mappingModel"]["nodeMappings"] = node_mappings

    converted_rels = {}
    converted_rel_positions = []
    rel_mappings = {}
    # Convert relationships
    relationships = arrows_json["relationships"]
    for rel in relationships:
        rid = rel.get('id', None)
        if rid is None:
            continue
        converted_rels[rid] = {
            "sourceNodeSchema": rel.get("fromId", None),
            "targetNodeSchema": rel.get("toId", None),
            "properties":[{
                "identifier":"<tbd>",
                "property":key,
                "type": cleaned_property_value(value)
            } for key, value in enumerate(rel.get('properties', []))],
            "property": rel.get("type", None)
        }
        converted_rel_positions.append(
            {
                "fromId":rel.get('fromId', None),
                "id":rid,
                "toId": rel.get('toId', None),
                "type":rel.get('type', None)
            }
        )
        rel_mappings[rid] = {
            "relationshipSchema": rid,
            "mappings":[],
            "sourceMappings": [],
            "targetMappings": []
        }
    result["dataModel"]["graphModel"]["relationshipSchemas"] = converted_rels
    result["graph"]["relationships"] = converted_rel_positions
    result["dataModel"]["mappingModel"]["relationshipMappings"] = rel_mappings

    return result