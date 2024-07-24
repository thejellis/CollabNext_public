from flask import Flask, send_from_directory, request, jsonify
import requests
from flask_cors import CORS
import json

app= Flask(__name__, static_folder='build', static_url_path='/')
CORS(app)

@app.route('/')
def index():
  return send_from_directory(app.static_folder, 'index.html')

### NEW API CALLS

@app.route('/initial-search', methods=['POST'])
def initial_search():
  institution = request.json.get('organization')
  researcher = request.json.get('researcher')
  type = request.json.get('type')
  topic = request.json.get('topic')
  if institution and researcher and topic:
    works, graph = get_works(researcher, topic, institution)
    institution_data, aGraph = get_institution_metadata(institution)
    researcher_data, aGraph = get_author_metadata(researcher)
    topic_data, aGraph = get_topic_metadata(topic)
    results = {"works": works, "institution_metadata": institution_data, "author_metadata": researcher_data, "topic_metadata": topic_data, "graph": graph}
  elif institution and researcher:
    institution_data, aGraph = get_institution_metadata(institution)
    researcher_data, aGraph = get_author_metadata(researcher)
    topics, graph = get_topics(researcher, institution)
    results = {"topics": topics, "institution_metadata": institution_data, "author_metadata": researcher_data, "graph": graph}
  elif institution and topic:
    authors, graph = get_authors(institution, topic)
    institution_data, aGraph = get_institution_metadata(institution)
    topic_data, aGraph = get_topic_metadata(topic)
    results = {"authors": authors, "institution_metadata": institution_data, "topic_metadata": topic_data, "graph": graph}
  elif researcher and topic:
    works, graph = get_works(researcher, topic, "")
    researcher_data, aGraph = get_author_metadata(researcher)
    topic_data, aGraph = get_topic_metadata(topic)
    results = {"works": works, "author_metadata": researcher_data, "topic_metadata": topic_data, "graph": graph}
  elif topic:
    data, graph = get_topic_metadata(topic)
    results = {"metadata": data, "graph": graph}
  elif institution:
    data, graph = get_institution_metadata(institution)
    results = {"metadata": data, "graph": graph}
  elif researcher:
    data, graph = get_author_metadata(researcher)
    results = {"metadata": data, "graph": graph}
  return results

def get_authors(institution, topic):
   if institution and topic:
      query = f"""
      PREFIX soa: <https://semopenalex.org/ontology/>
      PREFIX dct: <http://purl.org/dc/terms/>
      PREFIX foaf: <http://xmlns.com/foaf/0.1/>
      PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

      SELECT DISTINCT ?name
      WHERE {'{'}
        ?institution foaf:name "{institution}" .
        ?topic skos:prefLabel "{topic}" .
        ?author <http://www.w3.org/ns/org#memberOf> ?institution .
        ?work dct:creator ?author .
        << ?work soa:hasTopic ?topic >> ?p ?o .
        ?author foaf:name ?name .
      {'}'}
      """
      results = query_endpoint(query)
      authors = []
      for author in results:
         authors.append(author['name'])

      nodes = []
      edges = []
      institution_node = { 'data': { 'id': institution, 'label': institution, "type": "institution" } }
      topic_node = { 'data': { 'id': topic, 'label': topic, "type": "topic" } }
      nodes.append(institution_node)
      nodes.append(topic_node)
      for author_name in authors:
        author_node = { 'data': { 'id': author_name, 'label': author_name, "type": "researcher" } }
        topic_edge = { 'data': { 'source': author_name, 'target': topic, "label": "researches" } }
        institution_edge = { 'data': { 'source': author_name, 'target': institution, "label": "memberOf" } }
        nodes.append(author_node)
        if not topic_edge in edges:
          edges.append(topic_edge)
        if not institution_edge in edges:
          edges.append(institution_edge)

      return {"names": authors}, {"nodes": nodes, "edges": edges}

def get_topics(author, institution):
   if author and institution:
      query = f"""
      PREFIX soa: <https://semopenalex.org/ontology/>
      PREFIX dct: <http://purl.org/dc/terms/>
      PREFIX foaf: <http://xmlns.com/foaf/0.1/>
      PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

      SELECT DISTINCT ?name (GROUP_CONCAT(DISTINCT ?workTitle; SEPARATOR=", ") AS ?workTitles)
      WHERE {'{'}
        ?author foaf:name "{author}" .
        ?institution foaf:name "{institution}" .
        ?work dct:creator ?author .
        ?work soa:hasAuthorship ?authorship .
        ?authorship soa:hasOrganization ?institution .
        << ?work soa:hasTopic ?topic >> ?p ?o .
        ?work <http://purl.org/dc/terms/title> ?workTitle .
        ?topic skos:prefLabel ?name .
      {'}'}GROUP BY ?name
      """
      results = query_endpoint(query)
      topics = []
      for topic in results:
         topics.append((topic['name'], topic['workTitles']))
      
      edges = []
      nodes = []
      institution_node = { 'data': { 'id': institution, 'label': institution, "type": "institution" } }
      author_node = { 'data': { 'id': author, 'label': author, "type": "researcher" } }
      nodes.append(institution_node)
      nodes.append(author_node)
      edges.append( { 'data': { 'source': author, 'target': institution, "label": "memberOf" } })
      for entry in topics:
        topic_name = entry[0]
        works = entry[1]
        topic_node = { 'data': { 'id': topic_name, 'label': topic_name, "type": "topic" } }
        topic_edge = { 'data': { 'source': author, 'target': topic_name, "label": "researches", "connectingWorks": works } }
        nodes.append(topic_node)
        if not topic_edge in edges:
          edges.append(topic_edge)
      topic_list = []
      for a in topics:
        topic_list.append(a[0])
      
      return {"names": topic_list}, {"nodes": nodes, "edges": edges}

def get_works(author, topic, institution):
   if author and topic and institution:
      query = f"""
      PREFIX soa: <https://semopenalex.org/ontology/>
      PREFIX dct: <http://purl.org/dc/terms/>
      PREFIX foaf: <http://xmlns.com/foaf/0.1/>
      PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

      SELECT DISTINCT ?name
      WHERE {'{'}
        ?author foaf:name "{author}" .
        ?institution foaf:name "{institution}" .
        ?topic skos:prefLabel "{topic}" .
        ?work dct:creator ?author .
        ?work soa:hasAuthorship ?authorship .
        ?authorship soa:hasOrganization ?institution .
        << ?work soa:hasTopic ?topic >> ?p ?o .
        ?work dct:title ?name .
      {'}'}
      """
      results = query_endpoint(query)
      titles = []
      for title in results:
         titles.append(title['name'])
      
      nodes = []
      edges = []
      author_node = { 'data': { 'id': author, 'label': author, 'type': 'researcher' } }
      topic_node = { 'data': { 'id': topic, 'label': topic, 'type': 'topic' } }
      institution_node = { 'data': { 'id': institution, 'label': institution, 'type': 'institution' } }
      nodes.append(author_node)
      nodes.append(topic_node)
      nodes.append(institution_node)
      edges.append({ 'data': { 'source': author, 'target': institution, 'label': 'memberOf' } })
      for work in titles:
        work_node = { 'data': { 'id': work, 'label': work, 'type': 'work' } }
        work_edge = { 'data': { 'source': work, 'target': author, 'label': 'authored' } }
        topic_edge = { 'data': { 'source': work, 'target': topic, 'label': 'hasTopic' } }
        nodes.append(work_node)
        edges.append(work_edge)
        if not topic_edge in edges:
          edges.append(topic_edge)

      return {"titles": titles}, {"nodes": nodes, "edges": edges}
   elif author and topic:
      query = f"""
      PREFIX soa: <https://semopenalex.org/ontology/>
      PREFIX dct: <http://purl.org/dc/terms/>
      PREFIX foaf: <http://xmlns.com/foaf/0.1/>
      PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

      SELECT DISTINCT ?name
      WHERE {'{'}
        ?author foaf:name "{author}" .
        ?topic skos:prefLabel "{topic}" .
        ?work dct:creator ?author .
        << ?work soa:hasTopic ?topic >> ?p ?o .
        ?work dct:title ?name .
      {'}'}
      """
      results = query_endpoint(query)
      titles = []
      for title in results:
         titles.append(title['name'])

      nodes = []
      edges = []
      author_node = { 'data': { 'id': author, 'label': author, 'type': 'researcher' } }
      topic_node = { 'data': { 'id': topic, 'label': topic, 'type': 'topic' } }
      nodes.append(author_node)
      nodes.append(topic_node)
      for work in titles:
        work_node = { 'data': { 'id': work, 'label': work, 'type': 'work' } }
        work_edge = { 'data': { 'source': work, 'target': author, 'label': 'authored' } }
        topic_edge = { 'data': { 'source': work, 'target': topic, 'label': 'hasTopic' } }
        nodes.append(work_node)
        edges.append(work_edge)
        if not topic_edge in edges:
          edges.append(topic_edge)

      return {"titles": titles}, {"nodes": nodes, "edges": edges}


def get_institution_metadata(institution):
  query = f"""
  SELECT ?ror ?workscount ?citedcount ?homepage ?institution (COUNT(distinct ?people) as ?peoplecount)
  WHERE {'{'}
  ?institution <http://xmlns.com/foaf/0.1/name> "{institution}" .
  ?institution <https://semopenalex.org/ontology/ror> ?ror .
  ?institution <https://semopenalex.org/ontology/worksCount> ?workscount .
  ?institution <https://semopenalex.org/ontology/citedByCount> ?citedcount .
  ?institution <http://xmlns.com/foaf/0.1/homepage> ?homepage .
  ?people <http://www.w3.org/ns/org#memberOf> ?institution .
  {'}'} GROUP BY ?ror ?workscount ?citedcount ?homepage ?institution
  """
  query2 = f"""
  SELECT DISTINCT ?topicName
  WHERE {'{'}
  ?institution <http://xmlns.com/foaf/0.1/name> "{institution}" .
  ?person <http://www.w3.org/ns/org#memberOf> ?institution .
  ?work <http://purl.org/dc/terms/creator> ?person .
  << ?work <https://semopenalex.org/ontology/hasTopic> ?topic >> ?p ?o .
  ?topic <http://www.w3.org/2004/02/skos/core#prefLabel> ?topicName .
  {'}'}LIMIT 10
  """
  results = query_endpoint(query)
  ror = results[0]['ror']
  works_count = results[0]['workscount']
  cited_count = results[0]['citedcount']
  homepage = results[0]['homepage']
  author_count = results[0]['peoplecount']
  oa_link = results[0]['institution']
  oa_link = oa_link.replace('semopenalex', 'openalex').replace('institution', 'institutions')

  nodes = []
  edges = []
  nodes.append({ 'data': { 'id': institution, 'label': institution, 'type': 'institution' } })
  results2 = query_endpoint(query2)
  for topic in results2:
    name = topic['topicName']
    node = { 'data': { 'id': name, 'label': name, 'type': 'topic' } }
    node_edge = { 'data': { 'source': institution, 'target': name, 'label': 'researches' } }
    nodes.append(node)
    edges.append(node_edge)
  return {"name": institution, "ror": ror, "works_count": works_count, "cited_count": cited_count, "homepage": homepage, "author_count": author_count, 'oa_link': oa_link}, {"nodes": nodes, "edges": edges}

def get_topic_metadata(topic):
   query = f"""
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT DISTINCT ?works_count ?cited_by_count ?note ?topic
    WHERE {'{'}
        ?topic skos:prefLabel "{topic}" .
        ?topic <https://semopenalex.org/ontology/worksCount> ?works_count .
        ?topic <https://semopenalex.org/ontology/citedByCount> ?cited_by_count .
        ?topic <http://www.w3.org/2004/02/skos/core#note> ?note .
    {'}'}
   """
   query2 = f"""
    SELECT DISTINCT ?institutionName
    WHERE {'{'}
    ?topic <http://www.w3.org/2004/02/skos/core#prefLabel> "{topic}" .
    << ?work <https://semopenalex.org/ontology/hasTopic> ?topic >> ?p ?o .
    ?work <http://purl.org/dc/terms/creator> ?person .
    ?person <http://www.w3.org/ns/org#memberOf> ?institution .
    ?institution <http://xmlns.com/foaf/0.1/name> ?institutionName .
    {'}'}LIMIT 10
   """
   results = query_endpoint(query)
   works_count = results[0]['works_count']
   cited_by_count = results[0]['cited_by_count']
   description = results[0]['note']
   oa_link = results[0]['topic']
   oa_link = oa_link.replace('semopenalex', 'openalex').replace('topic', 'topics')

   nodes = []
   edges = []
   nodes.append({ 'data': { 'id': topic, 'label': topic, 'type': 'topic' } })
   results2 = query_endpoint(query2)
   for inst in results2:
     name = inst['institutionName']
     node = { 'data': { 'id': name, 'label': name, 'type': 'institution' } }
     node_edge = { 'data': { 'source': name, 'target': topic, 'label': 'researches' } }
     nodes.append(node)
     edges.append(node_edge)

   return {"works_count": works_count, "cited_by_count": cited_by_count, "description": description, "oa_link": oa_link}, {"nodes": nodes, "edges": edges}

def get_author_metadata(author):
   query = f"""
    SELECT ?cite_count ?orcid ?works_count ?current_institution_name ?author
    WHERE {'{'}
    ?author <http://xmlns.com/foaf/0.1/name> "{author}" .
    ?author <https://semopenalex.org/ontology/citedByCount> ?cite_count .
    ?author <https://dbpedia.org/ontology/orcidId> ?orcid .
    ?author <https://semopenalex.org/ontology/worksCount> ?works_count .
    ?author <http://www.w3.org/ns/org#memberOf> ?current_institution .
    ?current_institution <http://xmlns.com/foaf/0.1/name> ?current_institution_name .
    {'}'}
   """
   query2 = f"""
    SELECT ?topicName (GROUP_CONCAT(DISTINCT ?workTitle; SEPARATOR=", ") AS ?workTitles)
    WHERE {"{"}
      ?person <http://xmlns.com/foaf/0.1/name> "Didier Contis" .
      ?work <http://purl.org/dc/terms/creator> ?person .
      << ?work <https://semopenalex.org/ontology/hasTopic> ?topic >> ?p ?o .
      ?topic <http://www.w3.org/2004/02/skos/core#prefLabel> ?topicName .
      ?work <http://purl.org/dc/terms/title> ?workTitle .
    {"}"}
    GROUP BY ?topicName
    LIMIT 10
   """
   results = query_endpoint(query)
   cited_by_count = results[0]['cite_count']
   orcid = results[0]['orcid']
   work_count = results[0]['works_count']
   current_institution = results[0]['current_institution_name']
   oa_link = results[0]['author']
   oa_link = oa_link.replace('semopenalex', 'openalex').replace('author', 'authors')

   nodes = []
   edges = []
   nodes.append({ 'data': { 'id': author, 'label': author, 'type': 'researcher' } })
   nodes.append({ 'data': { 'id': current_institution, 'label': current_institution, 'type': 'institution' } })
   edges.append({ 'data': { 'source': author, 'target': current_institution, 'label': 'memberOf' } })
   results2 = query_endpoint(query2)
   for top in results2:
     name = top['topicName']
     paper_titles = top['workTitles']
     node = { 'data': { 'id': name, 'label': name, 'type': 'topic' } }
     node_edge = { 'data': { 'source': author, 'target': name, 'label': 'researches', 'connectingWorks': paper_titles } }
     nodes.append(node)
     edges.append(node_edge)

   return {"name": author, "cited_by_count": cited_by_count, "orcid": orcid, "work_count": work_count, "current_institution": current_institution, "oa_link": oa_link}, {'nodes': nodes, 'edges': edges}

def query_endpoint(query):
  endpoint_url = "https://semopenalex.org/sparql"
  response = requests.post(endpoint_url, data={"query": query}, headers={'Accept': 'application/json'})
  return_value = []
  data = response.json()
  for entry in data['results']['bindings']:
    my_dict = {}
    for e in entry:
      my_dict[e] = entry[e]['value']
    return_value.append(my_dict)
  return return_value

@app.route('/get-default-graph', methods=['POST'])
def get_default_graph():
  with open("default.json", "r") as file:
    graph = json.load(file)
  return {"graph": graph}
  

if __name__ =='__main__':
  app.run()
  """x,result = get_topics("Didier Contis", "Georgia Institute of Technology")
  print(x)
  for a in result['nodes']:
    print(a)
  print()
  print()
  for a in result['edges']:
    print(a)"""
