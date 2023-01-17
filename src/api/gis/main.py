import sys
import psycopg2
from flask import Flask,jsonify, request
import json

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000
db_dst = None
app = Flask(__name__)
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
    cities=[]
    
    for city in data:
        cities.append(city)
        cursor_save.execute("UPDATE cities SET latitude = "+str(data[city]["latitude"])+", longitude = "+ str(data[city]["longitude"])+" WHERE id = "+str(data[city]["id"]))
        cursor_save.execute("SELECT * FROM cities")
    db_dst.commit()
    db_dst.close() 
    return json.dumps(cities)
   


@app.route('/api/markers', methods=['GET'])
def get_markers():
    args = request.args

    return [
        {
            "type": "feature",
            "geometry": {
                "type": "Point",
                "coordinates": [41.69462, -8.84679]
            },
            "properties": {
                "id": "7674fe6a-6c8d-47b3-9a1f-18637771e23b",
                "name": "Ronaldo",
                "country": "Portugal",
                "position": "Striker",
                "imgUrl": "https://cdn-icons-png.flaticon.com/512/805/805401.png",
                "number": 7
            }
        }
    ]


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
