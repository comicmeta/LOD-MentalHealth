# comics-lod-sparql.py - sparql examples

import rdflib

from rdflib import Graph

g = Graph()
g.parse("comics-lod.json")

# query 1 - all content, all terms
results = g.query('SELECT ?content ?about ?label WHERE { ?content schema:about ?about . ?about schema:name ?label . }', initNs={ 'cbo': 'https://comicmeta.org/cbo/', 'schema': 'https://schema.org/' })

for row in results:
    print(f"{row.content} {row.about} ({row.label})")