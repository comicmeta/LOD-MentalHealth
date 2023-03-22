# comics-lod-gephi-beta.py 
# script for creating csv for visualizing rdf data with gephi
# supports updated sequence model (v0.16)

import rdflib

from rdflib import Graph, Literal, FOAF, RDF, URIRef, Namespace, Dataset

# parse graph

g = Graph()
g.parse("comics-lod-short.json")

g.bind("ex", rdflib.Namespace("https://comicmeta.org/example/#"))
g.bind("cbo", rdflib.Namespace("https://comicmeta.org/cbo/"))
g.bind("schema", rdflib.Namespace("https://schema.org"))
g.bind("meddra", rdflib.Namespace("http://purl.bioontology.org/ontology/MEDDRA/"))
g.bind("ncit", rdflib.Namespace("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#"))
g.bind("lcsh", rdflib.Namespace("http://id.loc.gov/authorities/subjects/"))
g.bind("comics", rdflib.Namespace("https://www.comics.org/issue/"))
g.bind("comics_1963646", rdflib.Namespace("https://www.comics.org/issue/1963646/#"))

ns = {
    "ex": "https://comicmeta.org/cbo/",
    "cbo": "https://comicmeta.org/cbo/",
    "schema": "https://schema.org/"
}

# include all triples in graph

results = g.query("""CONSTRUCT { 
       ?s ?p ?o
   } WHERE { 
       ?s ?p ?o
   } """, initNs=ns)

# create a new graph from the output of the construct query

x = Graph()
x.parse(results.serialize(format='ttl'))

# setup headers for gephi nodes and edges csv template

nodes = "Id,Label,Object,Size\n"
edges = "Source,Label,Target,Type,Weight,Relationship\n"

# loop through all triples in the new graph (x), or full graph (g)

for s, p, o in x.triples((None, None, None)):
    subj = s.n3(g.namespace_manager)
    pred = p.n3(g.namespace_manager)
    obj = o.n3(g.namespace_manager)

    """
    size = {
        "cbo:story": 30,
        "schema:about": 20,
        "schema:name": 10
    }
    """

    size = {
        "rdf:type": 0,
        "cbo:story": 50,
        "cbo:page": 40,
        "cbo:gutter": 35,
        "cbo:panel": 30,
        "schema:about": 20,
        "schema:name": 10
    }

    nodes += f"{subj},{subj}\n"
    nodes += f"{obj},{obj},{pred},{size[pred]}\n"
    edges += f"{subj},{pred},{obj},Undirected,{size[pred]},{pred}\n "

# write csv to disk

f = open("visualizations/comics-lod-short-edges.csv", "w")
f.write(edges)
f.close()

f = open("visualizations/comics-lod-short-nodes.csv", "w")
f.write(nodes)
f.close()
