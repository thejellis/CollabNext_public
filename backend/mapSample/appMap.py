from flask import Flask, render_template, request, jsonify, send_file
import json
import geojson
import pandas as pd
import requests

app = Flask(__name__)

# Load GeoJSON data (HBCUs)
with open('data/hbcu.geojson') as f:
    hbcu_data = json.load(f)
    

# Load Topics CSV data
topics_df = pd.read_csv('data/topics.csv')
topics = topics_df['search_topic'].tolist()  # assuming the 'topic' column contains the topics

@app.route('/')
def index():
    # Extracting institutions, cities, and states from GeoJSON data
    institutions = [
        {"institution": f["properties"]["institution"], "city": f["properties"]["city"], "state": f["properties"]["state"]}
        for f in hbcu_data['features']
    ]
    states = sorted({f["properties"]["state"] for f in hbcu_data['features']})
    cities = sorted({f["properties"]["city"] for f in hbcu_data['features']})
    

    return render_template(
        'index.html',
        hbcu_geojson=geojson.dumps(hbcu_data),
        institutions=institutions,
        cities=cities,
        states=states,
        topics=topics  # Pass topics to the template
    )

# @app.route('/geojson-features', methods=['GET'])
# def get_all_points():
#     features = []
#     for geo_feature in hbcu_data:
#         features.append({
#             "type": "Feature",
#             "geometry": {
#                 "type": geo_feature[0]['geometry']['type'],
#                 "coordinates": geo_feature['geometry']['coordinates']
#             }
#         })
#     return jsonify(features)

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = f'{data["topic"]} AND {data["institution"]}'
    url = f'http://export.arxiv.org/api/query?search_query=all:{query}&max_results=10'
    response = requests.get(url)
    results = response.json()
    return jsonify(results)

@app.route('/download', methods=['GET'])
def download_csv():
    output_csv = 'arxiv_results.csv'
    return send_file(output_csv, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
