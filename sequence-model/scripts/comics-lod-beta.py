# comics-lod-beta.py 
# script for converting comics-lod-template.csv data to json-ld.
# supports updated sequence model (v0.16)

import rdflib
import csv
import json
import sys

from rdflib import Graph, Literal, FOAF, RDF, URIRef, Namespace, Dataset
from pyld import jsonld

# test arguments
if len(sys.argv) < 1:
    print('Missing source file...')
    exit()
elif len(sys.argv) < 2:
    print('Missing target file...')
    exit()

# add namespaces
CBO = rdflib.Namespace('https://comicmeta.org/cbo/')
SCHEMA = rdflib.Namespace('https://schema.org/')

# create graph
g = Graph()
g.bind('cbo', CBO)
g.bind('schema', SCHEMA)

# template columns
COMIC = 0
STORY = 1
PAGE = 2
GUTTER = 3
PANEL = 4
LABEL = 5
ABOUT = 6

# open csv file, add contents to graph
with open(sys.argv[1]) as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')

    # skip header row
    next(reader)

    for row in reader:
        g.add((URIRef(row[COMIC]), RDF.type, CBO.Comic))
        g.add((URIRef(row[COMIC]), CBO.story, URIRef(row[STORY])))
        g.add((URIRef(row[STORY]), RDF.type, CBO.Story))
        g.add((URIRef(row[STORY]), CBO.page, URIRef(row[PAGE])))
        g.add((URIRef(row[PAGE]), RDF.type, CBO.Page))

        if row[GUTTER] != '':
            g.add((URIRef(row[PAGE]), CBO.gutter, URIRef(row[GUTTER])))
            g.add((URIRef(row[GUTTER]), RDF.type, CBO.Gutter))
            g.add((URIRef(row[GUTTER]), CBO.panel, URIRef(row[PANEL])))
            g.add((URIRef(row[PANEL]), RDF.type, CBO.Panel))
            g.add((URIRef(row[GUTTER]), SCHEMA.about, URIRef(row[ABOUT])))
            g.add((URIRef(row[ABOUT]), RDF.type, SCHEMA.Intangible))
            g.add((URIRef(row[ABOUT]), SCHEMA.name, Literal(row[LABEL])))
        elif row[PANEL] != '':
            g.add((URIRef(row[PAGE]), CBO.panel, URIRef(row[PANEL])))
            g.add((URIRef(row[PANEL]), RDF.type, CBO.Panel))
            g.add((URIRef(row[PANEL]), SCHEMA.about, URIRef(row[ABOUT])))
            g.add((URIRef(row[ABOUT]), RDF.type, SCHEMA.Intangible))
            g.add((URIRef(row[ABOUT]), SCHEMA.name, Literal(row[LABEL])))
        else:
            g.add((URIRef(row[PAGE]), SCHEMA.about, URIRef(row[ABOUT])))
            g.add((URIRef(row[ABOUT]), RDF.type, SCHEMA.Intangible))
            g.add((URIRef(row[ABOUT]), SCHEMA.name, Literal(row[LABEL])))

# serialize graph to json-ld
doc = g.serialize(format='json-ld')

# frame json-ld
frame = {
    "@context": {
        "cbo": "https://comicmeta.org/cbo/",
        "schema": "https://schema.org/",
        "@base": "https://comicmeta.org/example/"
    },
    "@type": "cbo:Comic",
    "story": {
        "@type": "cbo:Story",
        "page": {
            "@type": "cbo:Page",
            "panel": {
                "@type": "cbo:Panel"
            },
            "gutter": {
                "@type": "cbo:Gutter",
                "panel": {
                    "@type": "cbo:Panel"
                }
            }
        }
    }
}

framed = jsonld.frame(json.loads(doc), frame)

# write json-ld to disk
f = open(sys.argv[2], "w")
f.write(json.dumps(framed, indent=2))
f.close()

print('Success!')
