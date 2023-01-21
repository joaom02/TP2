import sys
import psycopg2
from flask import Flask,jsonify, request
import json

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000
db_dst = None
app = Flask(__name__)
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
app.config["DEBUG"] = True


@app.route('/api/retrive/', methods=['POST'])
def retrive():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
    data = request.get_json()
    cities={}
    cursor_retrive = db_dst.cursor() 
    cursor_retrive.execute("SELECT id,name,latitude,longitude FROM cities WHERE latitude IS NULL AND longitude IS NULL LIMIT "+str(data["ENTITIES_PER_ITERATION"]))

    for element in cursor_retrive:
        
        cities[element[0]] ={
            "id": element[0],
            "name": element[1],
            "latitude":element[2],
            "longitude":element[3]
        }

    db_dst.close() 
    return cities
       
@app.route('/api/save/', methods=['POST'])
def save():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
    data = request.get_json()
    cursor_save = db_dst.cursor() 
    print(data)
    for city in data:
        
        cursor_save.execute("UPDATE cities SET latitude = "+str(data[city]["latitude"])+", longitude = "+ str(data[city]["longitude"])+" WHERE id = '"+str(data[city]["id"])+"'")
        cursor_save.execute("SELECT * FROM cities")
    db_dst.commit()
    db_dst.close() 
    return "top"
   


@app.route('/api/markers', methods=['GET'])
def get_markers():
    args = request.args
    cities = []
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
    
    cursor_insert = db_dst.cursor() 
    cursor_insert.execute("SELECT id, name, latitude, longitude FROM cities")
    for element in cursor_insert:
        #city = City(name=element[1], id = element[0], latitude = element[2], longitude = element[3])
        city={
                "type": "feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [element[2], element[3]]
                },
                "properties": {
                    "id": element[0],
                    "name": element[1],
                    "imgUrl": "https://image.shutterstock.com/image-vector/city-vector-icon-260nw-144313540.jpg",
                }
            }
        cities.append(city)
    return cities
    


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
