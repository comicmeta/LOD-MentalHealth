# comics-lod-gephi.py - script for creating csv for visualizing rdf data with gephi

import rdflib

from rdflib import Graph, Literal, FOAF, RDF, URIRef, Namespace, Dataset

# parse graph

g = Graph()
g.parse("comics-lod.json")

g.bind("ex", rdflib.Namespace("https://comicmeta.org/example/#"))
g.bind("cbo", rdflib.Namespace("https://comicmeta.org/cbo/"))
g.bind("schema", rdflib.Namespace("https://schema.org"))
g.bind("icd10cm", rdflib.Namespace("http://purl.bioontology.org/ontology/ICD10CM/"))
g.bind("mesh", rdflib.Namespace("http://purl.bioontology.org/ontology/MESH/"))
g.bind("meddra", rdflib.Namespace("http://purl.bioontology.org/ontology/MEDDRA/"))
g.bind("ogms", rdflib.Namespace("http://purl.obolibrary.org/obo/OGMS_"))
g.bind("nddf", rdflib.Namespace("http://purl.bioontology.org/ontology/NDDF/"))
g.bind("obo", rdflib.Namespace("http://purl.obolibrary.org/obo/"))
g.bind("medlineplus", rdflib.Namespace("http://purl.bioontology.org/ontology/MEDLINEPLUS/"))
g.bind("icnp", rdflib.Namespace("http://www.icn.ch/icnp#"))
g.bind("ndfrt", rdflib.Namespace("http://purl.bioontology.org/ontology/NDFRT/"))
g.bind("icpc2p", rdflib.Namespace("http://purl.bioontology.org/ontology/ICPC2P/"))

ns = {
    "ex": "https://comicmeta.org/cbo/",
    "cbo": "https://comicmeta.org/cbo/",
    "schema": "https://schema.org/"
}

results = g.query("""CONSTRUCT { 
        ?comic cbo:story ?story . 
        ?story schema:about ?about . 
        ?about schema:name ?name 
    } WHERE { 
        ?comic cbo:story ?story . 
        ?story (cbo:page|cbo:page/cbo:panel) ?content . 
        ?content schema:about ?about . ?about schema:name ?name 
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
        "cbo:panel": 30,
        "schema:about": 20,
        "schema:name": 10
    }
    """

    nodes += f"{subj},{subj}\n"
    nodes += f"{obj},{obj},{pred},{size[pred]}\n"
    edges += f"{subj},{pred},{obj},Undirected,{size[pred]},{pred}\n "

# write csv to disk

f = open("visualizations/comics-lod-edges-chapter.csv", "w")
f.write(edges)
f.close()

f = open("visualizations/comics-lod-nodes-chapter.csv", "w")
f.write(nodes)
f.close()
