# LOD-MentalHealth
Linked Open Data (LOD) Mental Health Pilot Study

# Abstract

Comic books and graphic novels represent a narrative format that is both easily understandable and accessible, making the visual and engaging medium a great form of [graphic medicine](https://www.graphicmedicine.org), defined as "the intersection of comics and healthcare" (Czerwiec et al., 2020, p. 1), for communicating healthcare information and sharing stories of health and illness. However, metadata describing comics publications may lack medical subject headings or descriptions of the narrative content itself, which often illustrates related topics like symptoms, treatments, and side-effects. Enriching comics metadata with Linked Open Data (LOD) offers an opportunity to enhance the discoverability of relevant comics material and content for patients, caregivers, and healthcare providers.

# Methodology

This pilot study explores the use of semantic enrichment, “the process of adding a layer of topical metadata to content so that machines can make sense of it and build connections to it” (Clarke & Harley, 2014, p. 40), to better connect comics content to common healthcare vocabularies and ontologies. This strategy has been successfully implemented by libraries, archives, and museums (LAMs) to improve the discoverability and reuse of their data (Zeng, 2019), and has the potential to enhance the discovery of comics material for specific healthcare terms and medical topics.

The methodology used in this study builds upon the Linked Data approach seen in resources like [WorldCat](https://www.worldcat.org/title/states-of-mind/oclc/1057775520) and the content or sequence indexing model of the [Grand Comics Database (GCD)](https://www.comics.org/issue/1963646/) by extending those approaches to include references for each relevant page and panel, and linking those references to LOD resources.

To achieve this objective, a domain model of comics content from the [Comic Book Ontology (CBO)](https://comicmeta.org/cbo/) was implemented to structure and organize the indexed data in a template ([comics-lod.csv](data/comics-lod.csv)), alongside properties from the [Schema.org](https://schema.org/) vocabulary (schema:name, schema:about) to link content to healthcare terms found in [BioPortal](https://bioportal.bioontology.org/), a repository of biomedical ontologies.

A script was then utilized to parse and process the template data ([comics-lod.py](scripts/comics-lod.py)), converting that data to an RDF graph and finally serializing it to JSON-LD ([comics-lod.json](comics-lod.json)), a common data format for creating Linked Data that is both easy to read and write, as well as embed on webpages between script tags.

The resulting graph contained about 76 pages or panels illustrating topics related to mental health, and a total of 37 healthcare terms from 11 LOD healthcare ontologies ([visualizations/comics-lod-graph.png](visualizations/comics-lod-graph.png)).

# How To

Open a terminal window and execute the [comics-lod.py](scripts/comics-lod.py) script, passing the source data location ([comics-lod.csv](data/comics-lod.csv)) and the target output location ([comics-lod.json](comics-lod.json)). This command will parse source data created using the ([comics-lod-template.csv](templates/comics-lod.template.csv)) template, and output an RDF graph encoded as JSON-LD.

```
python3 scripts/comics-lod.py data/comics-lod.csv comics-lod.json
```

After generating the RDF graph and JSON-LD output, the results can then be visualized using tools like [Gephi](https://gephi.org/). Execute the [comics-lod-gephi.py](scripts/comics-lod-gephi.py) script to generate a set of CSV files containing all nodes and edge in the results ([visualizations/comics-lod-nodes.csv](visualizations/comics-lod-nodes.csv) and [visualizations/comics-lod-edges.csv](visualizations/comics-lod-edges.csv)), then import to Gephi.

```
python3 scripts/comics-lod-gephi.py
```

# Summary

An opportunity exists to better link metadata for comics and comics content to common healthcare vocabularies and ontologies, potentially enhancing the discovery of distinct comics content for specific medical terms and healthcare topics, while also better enabling the potential of this content to be reused, especially in patient and provider education.

# References

Clarke, M., & Harley, P. (2014). How smart is your content? Using semantic enrichment to improve your user experience and your bottom line. 
*Science*, 37(2), 40-44

Czerwiec, MK., Williams, I., Squier, S. M., Green, M. J., Myers, K. R., & Smith, S. T. (2020). *Graphic medicine manifesto.* Penn State Press.

Zeng, M. L. (2019). Semantic enrichment for enhancing LAM data and supporting digital humanities. Review article. *El profesional de la información*, 28(1) [https://doi.org/10.3145/epi.2019.ene.03](https://doi.org/10.3145/epi.2019.ene.03)
