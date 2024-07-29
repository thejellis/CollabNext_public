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
   # DONE
   if institution and topic:
      query = f"""
      PREFIX soa: <https://semopenalex.org/ontology/>
      PREFIX dct: <http://purl.org/dc/terms/>
      PREFIX foaf: <http://xmlns.com/foaf/0.1/>
      PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

      SELECT DISTINCT ?name ?institution ?topic ?author ?workTitle
      WHERE {'{'}
        ?institution foaf:name "{institution}" .
        ?topic skos:prefLabel "{topic}" .
        ?author <http://www.w3.org/ns/org#memberOf> ?institution .
        ?work dct:creator ?author .
        << ?work soa:hasTopic ?topic >> ?p ?o .
        ?author foaf:name ?name .
        ?work <http://purl.org/dc/terms/title> ?workTitle .
      {'}'}
      """
      results = query_endpoint(query)
      authors = []
      connecting_works = {}
      for entry in results:
         oa_link = entry['author']
         author_id = oa_link.replace('semopenalex', 'openalex').replace('author', 'authors')
         if author_id in connecting_works:
           connecting_works[author_id].append(entry['workTitle'])
         else:
           authors.append((entry['name'], author_id))
           institution_id = entry['institution'].replace('semopenalex', 'openalex').replace('institution', 'institutions')
           topic_id = entry['topic'].replace('semopenalex', 'openalex').replace('topic', 'topics')
           connecting_works[author_id] = [entry['workTitle']]
      nodes = []
      edges = []
      institution_node = { 'id': institution_id, 'label': institution, "type": "INSTITUTION" } 
      topic_node = { 'id': topic_id, 'label': topic, "type": "TOPIC" }
      nodes.append(institution_node)
      nodes.append(topic_node)
      for entry in authors:
        author_name = entry[0]
        author_id = entry[1]
        author_node = { 'id': author_id, 'label': author_name, "type": "AUTHOR" }
        workTitles = ', '.join(connecting_works[author_id])
        topic_edge = { 'id': f"""{author_id}-{topic_id}""", 'start': author_id, 'end': topic_id, "label": "researches", "start_type": "AUTHOR", "end_type": "TOPIC", "connecting_works": workTitles}
        institution_edge = { 'id': f"""{author_id}-{institution_id}""" ,'start': author_id, 'end': institution_id, "label": "memberOf", "start_type": "AUTHOR", "end_type": "INSTITUTION"}
        nodes.append(author_node)
        if not topic_edge in edges:
          edges.append(topic_edge)
        if not institution_edge in edges:
          edges.append(institution_edge)

      return {"names": authors}, {"nodes": nodes, "edges": edges}

def get_topics(author, institution):
   # DONE
   if author and institution:
      query = f"""
      PREFIX soa: <https://semopenalex.org/ontology/>
      PREFIX dct: <http://purl.org/dc/terms/>
      PREFIX foaf: <http://xmlns.com/foaf/0.1/>
      PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

      SELECT DISTINCT ?name ?author ?institution ?topic (GROUP_CONCAT(DISTINCT ?workTitle; SEPARATOR=", ") AS ?workTitles)
      WHERE {'{'}
        ?author foaf:name "{author}" .
        ?institution foaf:name "{institution}" .
        ?work dct:creator ?author .
        ?work soa:hasAuthorship ?authorship .
        ?authorship soa:hasOrganization ?institution .
        << ?work soa:hasTopic ?topic >> ?p ?o .
        ?work <http://purl.org/dc/terms/title> ?workTitle .
        ?topic skos:prefLabel ?name .
      {'}'}GROUP BY ?name ?author ?institution ?topic
      """
      results = query_endpoint(query)
      topics = []
      for entry in results:
         topic_name = entry['name']
         work_titles = entry['workTitles']
         topic_id = entry['topic'].replace('semopenalex', 'openalex').replace('topic', 'topics')
         topics.append((topic_name, topic_id, work_titles))
         institution_id = entry['institution'].replace('semopenalex', 'openalex').replace('institution', 'institutions')
         author_id = entry['author'].replace('semopenalex', 'openalex').replace('author', 'authors')
      edges = []
      nodes = []
      institution_node = { 'id': institution_id, 'label': institution, "type": "INSTITUTION" } 
      author_node = { 'id': author_id, 'label': author, "type": "AUTHOR" }
      nodes.append(institution_node)
      nodes.append(author_node)
      edges.append({'id': f"""{author_id}-{institution_id}""", 'start': author_id, 'end': institution_id, "label": "memberOf", "start_type": "AUTHOR", "end_type": "INSTITUTION"})
      for entry in topics:
        topic_name = entry[0]
        topic_id = entry[1]
        works = entry[2]
        topic_node = { 'id': topic_id, 'label': topic_name, "type": "TOPIC" }
        topic_edge = { 'id': f"""{author_id}-{topic_id}""", 'start': author_id, 'end': topic_id, "label": "researches", "start_type": "AUTHOR", "end_type": "TOPIC", "connecting_works": works}
        nodes.append(topic_node)
        if not topic_edge in edges:
          edges.append(topic_edge)
      topic_list = []
      for a in topics:
        topic_list.append(a[0])
      
      return {"names": topic_list}, {"nodes": nodes, "edges": edges}

def get_works(author, topic, institution):
   if author and topic and institution:
      # DONE
      query = f"""
      PREFIX soa: <https://semopenalex.org/ontology/>
      PREFIX dct: <http://purl.org/dc/terms/>
      PREFIX foaf: <http://xmlns.com/foaf/0.1/>
      PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

      SELECT DISTINCT ?name ?author ?topic ?institution
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
      for entry in results:
         author_id = entry['author'].replace('semopenalex', 'openalex').replace('author', 'authors')
         topic_id = entry['topic'].replace('semopenalex', 'openalex').replace('topic', 'topics')
         institution_id = entry['institution'].replace('semopenalex', 'openalex').replace('institution', 'institutions')
         titles.append(entry['name'])
      
      nodes = []
      edges = []
      author_node = { 'id': author_id, 'label': author, 'type': 'AUTHOR' } 
      topic_node = { 'id': topic_id, 'label': topic, 'type': 'TOPIC' }
      institution_node = { 'id': institution_id, 'label': institution, 'type': 'INSTITUTION' }
      nodes.append(author_node)
      nodes.append(topic_node)
      nodes.append(institution_node)
      edges.append({'id': f"""{author_id}-{institution_id}""", 'start': author_id, 'end': institution_id, "label": "memberOf", "start_type": "AUTHOR", "end_type": "INSTITUTION"})
      for work in titles:
        work_node = { 'id': work, 'label': work, 'type': 'WORK' } 
        work_edge = { 'id': f"""{work}-{author_id}""", 'start': work, 'end': author_id, 'label': 'authored' }
        topic_edge = { 'id': f"""{work}-{topic_id}""", 'start': work, 'end': topic_id, 'label': 'hasTopic' } 
        nodes.append(work_node)
        edges.append(work_edge)
        if not topic_edge in edges:
          edges.append(topic_edge)

      return {"titles": titles}, {"nodes": nodes, "edges": edges}
   elif author and topic:
      #Done
      query = f"""
      PREFIX soa: <https://semopenalex.org/ontology/>
      PREFIX dct: <http://purl.org/dc/terms/>
      PREFIX foaf: <http://xmlns.com/foaf/0.1/>
      PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

      SELECT DISTINCT ?name ?author ?topic
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
      for entry in results:
         author_id = entry['author'].replace('semopenalex', 'openalex').replace('author', 'authors')
         topic_id = entry['topic'].replace('semopenalex', 'openalex').replace('topic', 'topics')
         titles.append(entry['name'])

      nodes = []
      edges = []
      author_node = { 'id': author_id, 'label': author, 'type': 'AUTHOR' } 
      topic_node = { 'id': topic_id, 'label': topic, 'type': 'TOPIC' }
      nodes.append(author_node)
      nodes.append(topic_node)
      for work in titles:
        work_node = { 'id': work, 'label': work, 'type': 'WORK' } 
        work_edge = { 'id': f"""{work}-{author_id}""", 'start': work, 'end': author_id, 'label': 'authored' }
        topic_edge = { 'id': f"""{work}-{topic_id}""", 'start': work, 'end': topic_id, 'label': 'hasTopic' } 
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
  SELECT DISTINCT ?topicName ?topic
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
  nodes.append({ 'id': oa_link, 'label': institution, 'type': 'INSTITUTION' })
  results2 = query_endpoint(query2)
  for topic in results2:
    topic_id = topic['topic']
    name = topic['topicName']
    node = { 'id': topic_id, 'label': name, 'type': 'TOPIC' }
    node_edge = { 'id': f"""{oa_link}-{topic_id}""", 'start': oa_link, 'end': topic_id, "label": "researches", "start_type": "INSTITUTION", "end_type": "TOPIC"}
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
    SELECT DISTINCT ?institutionName ?institution
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
   nodes.append({ 'id': oa_link, 'label': topic, 'type': 'TOPIC' })
   results2 = query_endpoint(query2)
   for inst in results2:
     name = inst['institutionName']
     institution_id = inst['institution']
     node = {'id': institution_id, 'label': name, 'type': 'INSTITUTION' }
     node_edge = { 'id': f"""{institution_id}-{oa_link}""", 'start': institution_id, 'end': oa_link, "label": "researches", "start_type": "INSTITUTION", "end_type": "TOPIC"}
     nodes.append(node)
     edges.append(node_edge)

   return {"works_count": works_count, "cited_by_count": cited_by_count, "description": description, "oa_link": oa_link}, {"nodes": nodes, "edges": edges}

def get_author_metadata(author):
   query = f"""
    SELECT ?cite_count ?orcid ?works_count ?current_institution_name ?author ?current_institution
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
    SELECT ?topicName ?topic (GROUP_CONCAT(DISTINCT ?workTitle; SEPARATOR=", ") AS ?workTitles)
    WHERE {"{"}
      ?person <http://xmlns.com/foaf/0.1/name> "Didier Contis" .
      ?work <http://purl.org/dc/terms/creator> ?person .
      << ?work <https://semopenalex.org/ontology/hasTopic> ?topic >> ?p ?o .
      ?topic <http://www.w3.org/2004/02/skos/core#prefLabel> ?topicName .
      ?work <http://purl.org/dc/terms/title> ?workTitle .
    {"}"}
    GROUP BY ?topicName ?topic
    LIMIT 10
   """
   results = query_endpoint(query)
   cited_by_count = results[0]['cite_count']
   orcid = results[0]['orcid']
   work_count = results[0]['works_count']
   current_institution = results[0]['current_institution_name']
   oa_link = results[0]['author']
   oa_link = oa_link.replace('semopenalex', 'openalex').replace('author', 'authors')
   current_institution_id = results[0]['current_institution_name'].replace('semopenalex', 'openalex').replace('institution', 'institutions')

   nodes = []
   edges = []
   nodes.append({ 'id': oa_link, 'label': author, 'type': 'AUTHOR' })
   nodes.append({ 'id': current_institution_id, 'label': current_institution, 'type': 'INSTITUTION' })
   edges.append({ 'id': f"""{oa_link}-{current_institution_id}""" ,'start': oa_link, 'end': current_institution_id, "label": "memberOf", "start_type": "AUTHOR", "end_type": "INSTITUTION"})
   results2 = query_endpoint(query2)
   for top in results2:
     name = top['topicName']
     id = top['topic']
     paper_titles = top['workTitles']
     node = {'id': id, 'label': name, 'type': 'TOPIC' }
     node_edge = { 'id': f"""{oa_link}-{id}""", 'start': oa_link, 'end': id, "label": "researches", "start_type": "AUTHOR", "end_type": "TOPIC", "connecting_works": paper_titles}
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
