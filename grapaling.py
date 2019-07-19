#!/usr/bin/env python3                                                                                                                                                                                                                                                                                                                                                                     
import urllib3
from neo4jrestclient.client import GraphDatabase

if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)    
    gdb = GraphDatabase("https://grapal.allenai.org:7473/db/data")

    # How many distinct relationship types?
    q = """MATCH (r:Relation) RETURN DISTINCT r.relation_type"""
    result = gdb.query(q=q, data_contents=True)
    print(result.rows)
    
