from flask import Flask, send_from_directory, request, jsonify
import requests
from flask_cors import CORS

app= Flask(__name__, static_folder='build', static_url_path='/')
CORS(app)

@app.route('/')
def index():
  return send_from_directory(app.static_folder, 'index.html')

@app.route('/update-text', methods=['POST'])
def update_text():
  input_text = request.json.get('inputText')
  isChecked = request.json.get('isChecked')
  query_response = sparql_query(input_text, isChecked, False)
  return {'updatedText': input_text, 'queryResults': query_response}

@app.route('/get-institutions', methods=['POST'])
def get_institutions():
  query = """
  SELECT ?name WHERE {
      ?institution a <https://semopenalex.org/ontology/Institution> .
      ?institution <http://xmlns.com/foaf/0.1/name> ?name
  } LIMIT 3
  """
  query_response = sparql_query(query, False, True)
  return {'one': str(query_response[0]), 'two': str(query_response[1]), 'three': str(query_response[2])}

@app.route('/get-topics', methods=['POST'])
def get_topics():
  selected_institution = request.json.get('selectedOption')
  query1 = """
  PREFIX org: <http://www.w3.org/ns/org#>
  SELECT DISTINCT ?name WHERE {
      ?institution <http://xmlns.com/foaf/0.1/name> """
  query2 = """ .
      ?institution a <https://semopenalex.org/ontology/Institution> .
      ?author org:memberOf ?institution .
      ?work <http://purl.org/dc/terms/creator> ?author .
      ?work <https://semopenalex.org/ontology/hasConcept> ?concept .
      ?concept <http://www.w3.org/2004/02/skos/core#prefLabel> ?name .
  } LIMIT 3
  """
  name = "\'" + str(selected_institution) + "\'"
  full_query = query1 + name + query2
  query_response = sparql_query(full_query, False, True)
  return {'one': str(query_response[0]), 'two': str(query_response[1]), 'three': str(query_response[2])}

@app.route('/get-authors', methods=['POST'])
def get_authors():
  selected_topic = request.json.get('selectedTopicOption')
  selected_institution = request.json.get('selectedOption')
  queryA = """PREFIX org: <http://www.w3.org/ns/org#>
  SELECT DISTINCT ?institution WHERE {
  ?institution <http://xmlns.com/foaf/0.1/name>
  """
  queryB = """ .
  ?institution a <https://semopenalex.org/ontology/Institution>
  } LIMIT 3
  """
  instQuery = queryA + "\'" + str(selected_institution) + "\'" + queryB
  result = sparql_query(instQuery, False, True)
  selected_institution = str(result[0])
  query1 = """PREFIX org: <http://www.w3.org/ns/org#>
  SELECT DISTINCT ?name WHERE {
  ?work <http://purl.org/dc/terms/creator> ?author .
  ?work <https://semopenalex.org/ontology/hasConcept> ?topic .
  ?topic <http://www.w3.org/2004/02/skos/core#prefLabel>
  """
  query2 = """ .
  ?author org:memberOf
  """
  query3 = """ .
  ?author <http://xmlns.com/foaf/0.1/name> ?name .
  } LIMIT 5
  """
  name_topic = "\'" + str(selected_topic) + "\'"
  name_institution = "<" + str(selected_institution) + ">"
  full_query = query1 + name_topic + query2 + name_institution + query3
  query_response = sparql_query(full_query, False, False)
  return {'authors': query_response}

def sparql_query(query, checkbox, list):
  if not checkbox:
      endpoint_url = "https://semopenalex.org/sparql"
  else:
      endpoint_url = "https://frink.apps.renci.org/semopenalex/sparql"
  response = requests.post(endpoint_url, data={"query": query}, headers={'Accept': 'application/json'})
  return_value = []
  data = response.json()
  for object in data['results']['bindings']:
      for entry in object:
          return_value.append(object[entry]['value'])
  if not list:
      return_string = ''
      for a in return_value:
          return_string = return_string + str(a) + ', '
      return return_string
  else:
      return return_value

### NEW API CALLS

@app.route('/initial-search', methods=['POST'])
def initial_search():
  institution = request.json.get('organization')
  researcher = request.json.get('researcher')
  type = request.json.get('type')
  topic = request.json.get('topic')
  if institution and researcher and topic:
    works = get_works(researcher, topic, institution)
    institution_data = get_institution_metadata(institution)
    researcher_data = get_author_metadata(researcher)
    topic_data = get_topic_metadata(topic)
    results = {"works": works, "institution_metadata": institution_data, "author_metadata": researcher_data, "topic_metadata": topic_data}
  elif institution and researcher:
    institution_data = get_institution_metadata(institution)
    researcher_data = get_author_metadata(researcher)
    topics = get_topics(researcher, institution)
    results = {"topics": topics, "institution_metadata": institution_data, "author_metadata": researcher_data}
  elif institution and topic:
    authors = get_authors(institution, topic)
    institution_data = get_institution_metadata(institution)
    topic_data = get_topic_metadata(topic)
    results = {"authors": authors, "institution_metadata": institution_data, "topic_metadata": topic_data}
  elif researcher and topic:
    works = get_works(researcher, topic, "")
    researcher_data = get_author_metadata(researcher)
    topic_data = get_topic_metadata(topic)
    results = {"works": works, "author_metadata": researcher_data, "topic_metadata": topic_data}
  elif topic:
    results = get_topic_metadata(topic)
  elif institution:
    results = get_institution_metadata(institution)
  elif researcher:
    results = get_author_metadata(researcher)
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
        ?institution foaf:name '{institution}' .
        ?topic skos:prefLabel '{topic}' .
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
      return {"names": authors}

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
      return {"names": topics}

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
      return {"titles": titles}
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
      return {"titles": titles}


def get_institution_metadata(institution):
  query = f"""
  SELECT ?ror ?workscount ?citedcount ?homepage (COUNT(distinct ?people) as ?peoplecount)
  WHERE {'{'}
  ?institution <http://xmlns.com/foaf/0.1/name> "{institution}" .
  ?institution <https://semopenalex.org/ontology/ror> ?ror .
  ?institution <https://semopenalex.org/ontology/worksCount> ?workscount .
  ?institution <https://semopenalex.org/ontology/citedByCount> ?citedcount .
  ?institution <http://xmlns.com/foaf/0.1/homepage> ?homepage .
  ?people <http://www.w3.org/ns/org#memberOf> ?institution .
  {'}'} GROUP BY ?ror ?workscount ?citedcount ?homepage
  """
  results = query_endpoint(query)
  ror = results[0]['ror']
  works_count = results[0]['workscount']
  cited_count = results[0]['citedcount']
  homepage = results[0]['homepage']
  author_count = results[0]['peoplecount']
  return {"name": institution, "ror": ror, "works_count": works_count, "cited_count": cited_count, "homepage": homepage, "author_count": author_count}

def get_topic_metadata(topic):
   query = f"""
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT DISTINCT ?works_count ?cited_by_count ?note
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

   return {"works_count": works_count, "cited_by_count": cited_by_count, "description": description}

def get_author_metadata(author):
   query = f"""
    SELECT ?cite_count ?orcid ?works_count ?current_institution_name
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

   return {"name": author, "cited_by_count": cited_by_count, "orcid": orcid, "work_count": work_count, "current_institution": current_institution}

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
  app.run();
