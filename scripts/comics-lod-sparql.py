# comics-lod-sparql.py - sparql examples

import rdflib

from rdflib import Graph

g = Graph()
g.parse("comics-lod.json")

ns = {
    "cbo": "https://comicmeta.org/cbo/",
    "schema": "https://schema.org/",
    "meddra": "http://purl.bioontology.org/ontology/MEDDRA/"
}

# query 1 - all content, all terms

results = g.query("""
   SELECT ?content ?about ?label 
    WHERE { 
        ?content schema:about ?about . 
        ?about schema:name ?label . 
    }""", initNs=ns)


# query 2 - content about panic attacks (meddra:10033664)

# results = g.query("""
#   SELECT ?content
#   WHERE {
#        ?content schema:about meddra:10033664 .
#    }""", initNs=ns)

for row in results:
    print(f"{row.content} {row.about} ({row.label})")
