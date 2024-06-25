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
  query1 = f"""
  PREFIX org: <http://www.w3.org/ns/org#>
  SELECT DISTINCT ?name WHERE {'{'}
      ?institution <http://xmlns.com/foaf/0.1/name> "{selected_institution}".
      ?institution a <https://semopenalex.org/ontology/Institution> .
      ?author org:memberOf ?institution .
      ?work <http://purl.org/dc/terms/creator> ?author .
      << ?work <https://semopenalex.org/ontology/hasTopic> ?concept >> ?p ?o .
      ?concept <http://www.w3.org/2004/02/skos/core#prefLabel> ?name .
  {'}'} LIMIT 3
  """
  query_response = sparql_query(query1, False, True)
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
  << ?work <https://semopenalex.org/ontology/hasTopic> ?concept >> ?p ?o .
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

if __name__ =='__main__':
  app.run();
