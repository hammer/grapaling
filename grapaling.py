#!/usr/bin/env python3                                                                                                                                                                                                                                                                                                                                                                     
import urllib3
from neo4jrestclient.client import GraphDatabase

if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)    
    gdb = GraphDatabase("https://grapal.allenai.org:7473/db/data")

    #
    # Explore graph metadata
    #
    
    # Node labels:
    #  Paper
    #  Venue, Author, Affiliation
    #  Entity, Relation, RelationInstance
    q = "CALL db.labels()" 
    q = "CALL db.schema()" # doesn't work for some reason
    q = "CALL db.indexes()"

    
    #
    # Entity node explorations
    #
    # What kind of properties do Entity nodes have?
    #  entity_id, name
    q = "MATCH(e:Entity) UNWIND keys(e) AS entity_keys RETURN DISTINCT entity_keys"

    
    #
    # Relation node explorations
    #
    
    # What kind of properties do Relation nodes have?
    #  relation_id, relation_type, relation_subtype
    q = "MATCH(r:Relation) UNWIND keys(r) AS relation_keys RETURN DISTINCT relation_keys"
    
    # How many distinct relationship types? 7
    q = "MATCH (r:Relation) RETURN DISTINCT r.relation_type"

    # How many distinct relationship subtypes? 560!
    q = "MATCH (r:Relation) RETURN DISTINCT r.relation_subtype"
    result = gdb.query(q=q, data_contents=True)
    print(result.rows)    
    
