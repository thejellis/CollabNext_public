from flask import Flask, send_from_directory, request, jsonify
import requests
from flask_cors import CORS

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
    institution_data = get_institution_metadata(institution)
    researcher_data = get_author_metadata(researcher)
    topic_data = get_topic_metadata(topic)
    results = {"works": works, "institution_metadata": institution_data, "author_metadata": researcher_data, "topic_metadata": topic_data, "graph": graph}
  elif institution and researcher:
    institution_data = get_institution_metadata(institution)
    researcher_data = get_author_metadata(researcher)
    topics, graph = get_topics(researcher, institution)
    results = {"topics": topics, "institution_metadata": institution_data, "author_metadata": researcher_data, "graph": graph}
  elif institution and topic:
    authors, graph = get_authors(institution, topic)
    institution_data = get_institution_metadata(institution)
    topic_data = get_topic_metadata(topic)
    results = {"authors": authors, "institution_metadata": institution_data, "topic_metadata": topic_data, "graph": graph}
  elif researcher and topic:
    works, graph = get_works(researcher, topic, "")
    researcher_data = get_author_metadata(researcher)
    topic_data = get_topic_metadata(topic)
    results = {"works": works, "author_metadata": researcher_data, "topic_metadata": topic_data, "graph": graph}
  elif topic:
    data = get_topic_metadata(topic)
    graph = [{ 'data': { 'id': topic, 'label': topic } }]
    results = {"metadata": data, "graph": graph}
  elif institution:
    data = get_institution_metadata(institution)
    graph = [{ 'data': { 'id': institution, 'label': institution } }]
    results = {"metadata": data, "graph": graph}
  elif researcher:
    data = get_author_metadata(researcher)
    graph = [{ 'data': { 'id': researcher, 'label': researcher } }]
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

      graph = []
      institution_node = { 'data': { 'id': institution, 'label': institution } }
      topic_node = { 'data': { 'id': topic, 'label': topic } }
      graph.append(institution_node)
      graph.append(topic_node)
      for author_name in authors:
        author_node = { 'data': { 'id': author_name, 'label': author_name } }
        topic_edge = { 'data': { 'source': author_name, 'target': topic } }
        institution_edge = { 'data': { 'source': author, 'target': institution } }
        graph.append(author_node)
        if not topic_edge in graph:
          graph.append(topic_edge)
        if not institution_edge in graph:
          graph.append(institution_edge)

      return {"names": authors}, graph

def get_topics(author, institution):
   if author and institution:
      query = f"""
      PREFIX soa: <https://semopenalex.org/ontology/>
      PREFIX dct: <http://purl.org/dc/terms/>
      PREFIX foaf: <http://xmlns.com/foaf/0.1/>
      PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

      SELECT DISTINCT ?name
      WHERE {'{'}
        ?author foaf:name "{author}" .
        ?institution foaf:name "{institution}" .
        ?work dct:creator ?author .
        ?work soa:hasAuthorship ?authorship .
        ?authorship soa:hasOrganization ?institution .
        << ?work soa:hasTopic ?topic >> ?p ?o .
        ?topic skos:prefLabel ?name .
      {'}'}
      """
      results = query_endpoint(query)
      topics = []
      for topic in results:
         topics.append(topic['name'])
      
      graph = []
      institution_node = { 'data': { 'id': institution, 'label': institution } }
      author_node = { 'data': { 'id': author, 'label': author } }
      graph.append(institution_node)
      graph.append(author_node)
      graph.append( { 'data': { 'source': author_node, 'target': institution_node } })
      for topic_name in topics:
        topic_node = { 'data': { 'id': topic_name, 'label': topic_name } }
        topic_edge = { 'data': { 'source': topic_name, 'target': author } }
        graph.append(topic_node)
        if not topic_edge in graph:
          graph.append(topic_edge)
      
      return {"names": topics}, graph

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
      
      graph = []
      author_node = { 'data': { 'id': author, 'label': author } }
      topic_node = { 'data': { 'id': topic, 'label': topic } }
      institution_node = { 'data': { 'id': institution, 'label': institution } }
      graph.append(author_node)
      graph.append(topic_node)
      graph.append(institution_node)
      graph.append({ 'data': { 'source': author, 'target': institution } })
      for work in titles:
        work_node = { 'data': { 'id': work, 'label': work } }
        work_edge = { 'data': { 'source': work, 'target': author } }
        topic_edge = { 'data': { 'source': work, 'target': topic } }
        graph.append(work_node)
        graph.append(work_edge)
        if not topic_edge in graph:
          graph.append(topic_edge)

      return {"titles": titles}, graph
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

      graph = []
      author_node = { 'data': { 'id': author, 'label': author } }
      topic_node = { 'data': { 'id': topic, 'label': topic } }
      graph.append(author_node)
      graph.append(topic_node)
      for work in titles:
        work_node = { 'data': { 'id': work, 'label': work } }
        work_edge = { 'data': { 'source': work, 'target': author } }
        topic_edge = { 'data': { 'source': work, 'target': topic } }
        graph.append(work_node)
        graph.append(work_edge)
        if not topic_edge in graph:
          graph.append(topic_edge)

      return {"titles": titles}, graph


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
  results = query_endpoint(query)
  ror = results[0]['ror']
  works_count = results[0]['workscount']
  cited_count = results[0]['citedcount']
  homepage = results[0]['homepage']
  author_count = results[0]['peoplecount']
  oa_link = results[0]['institution']
  oa_link = oa_link.replace('semopenalex', 'openalex').replace('institution', 'institutions')
  return {"name": institution, "ror": ror, "works_count": works_count, "cited_count": cited_count, "homepage": homepage, "author_count": author_count, 'oa_link': oa_link}

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
   results = query_endpoint(query)
   works_count = results[0]['works_count']
   cited_by_count = results[0]['cited_by_count']
   description = results[0]['note']
   oa_link = results[0]['topic']
   oa_link = oa_link.replace('semopenalex', 'openalex').replace('topic', 'topics')
   return {"works_count": works_count, "cited_by_count": cited_by_count, "description": description, "oa_link": oa_link}

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
   results = query_endpoint(query)
   cited_by_count = results[0]['cite_count']
   orcid = results[0]['orcid']
   work_count = results[0]['works_count']
   current_institution = results[0]['current_institution_name']
   oa_link = results[0]['author']
   oa_link = oa_link.replace('semopenalex', 'openalex').replace('author', 'authors')
   return {"name": author, "cited_by_count": cited_by_count, "orcid": orcid, "work_count": work_count, "current_institution": current_institution, "oa_link": oa_link}

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

if __name__ =='__main__':
  app.run()
