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
    q = "CALL db.()"     
    q = "CALL db.schema()" # doesn't work for some reason
    q = "CALL db.indexes()"

    
    #
    # Entity node explorations
    #

    # What kind of properties do Entity nodes have?
    #  entity_id, name
    q = "MATCH (e:Entity) UNWIND keys(e) AS entity_keys RETURN DISTINCT entity_keys"

    # How many entity instances? 564,249
    q = "MATCH (e:Entity) RETURN COUNT(*)"

    # How many unique entity names? 563,844
    q = "MATCH (e:Entity) RETURN COUNT(DISTINCT e.name)"    

    
    #
    # Relation[Instance] node explorations
    #
    
    # What kind of properties do Relation nodes have?
    #  relation_id, relation_type, relation_subtype
    q = "MATCH(r:Relation) UNWIND keys(r) AS relation_keys RETURN DISTINCT relation_keys"
    
    # How many distinct relationship types? 7
    q = "MATCH (r:Relation) RETURN DISTINCT r.relation_type"

    # How many distinct relationship subtypes? 560!
    #  gene_associated_with_disease
    #  gene_product_malfunction_associated_with_disease
    q = "MATCH (r:Relation) RETURN DISTINCT r.relation_subtype"

    # What kind of properties do RelationInstance nodes have? None
    q = "MATCH(ri:RelationInstance) UNWIND keys(ri) AS ri_keys RETURN DISTINCT ri_keys"    
    
    # How many relation instances? 4,551,645
    q = "MATCH (r:RelationInstance) RETURN COUNT(*)"

    # Relations I care about
    subtypes = [
        'gene_associated_with_disease',
        'gene_product_malfunction_associated_with_disease',
        ]
    # NB: must double {} that appear in output string (gross) 
    q = """MATCH (n)-[:WITH_ENTITY {{entity_placement: "['0']"}}]->(e0:Entity),
                 (n)-[:WITH_RELATIONSHIP]->(r:Relation {{relation_subtype: '{subtype}'}}),
                 (n)-[:WITH_ENTITY]->(e1:Entity)
           RETURN COUNT(DISTINCT e0.entity_id), COUNT(DISTINCT e1.entity_id), COUNT(*)"""
    for subtype in subtypes:
        result = gdb.query(q=q.format(subtype=subtype), data_contents=True)
        print(subtype, result.rows)
