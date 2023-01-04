import sys

from flask import Flask, jsonify, request
import psycopg2
from entities import City

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

# set of all teams
# !TODO: replace by database access
cities = []
db_dst = None


app = Flask(__name__)
app.config["DEBUG"] = True



@app.route('/api/cities/insert/',methods=['POST'])
def insert_cities():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
    data = request.get_json()
    cursor_insert = db_dst.cursor() 
    cursor_insert.execute("INSERT INTO cities (id,name) values ('"+data["id"]+"','"+data["name"]+"')")
    db_dst.commit()
    db_dst.close()
    return data


@app.route('/api/companies/insert/',methods=['POST'])
def insert_companies():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
    data = request.get_json()
    cursor_insert = db_dst.cursor() 
    cursor_insert.execute("INSERT INTO companies (id,name,rating) values ('"+data["id"]+"','"+data["name"]+"','"+data["rating"]+"')")
    db_dst.commit()
    db_dst.close()
    return data


@app.route('/api/jobs/insert/',methods=['POST'])
def insert_jobs():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
    data = request.get_json()
    cursor_insert = db_dst.cursor() 
    cursor_insert.execute("INSERT INTO jobs (id,name,companyid,cityref,summary) values ('"+data["id"]+"','"+data["name"]+"','"+data["companyid"]+"','"+data["cityRef"]+"','"+data["summary"]+"')")
    db_dst.commit()
    db_dst.close()
    return data


@app.route('/api/cities/get/', methods=['GET'])
def get_cities():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
    
    cursor_insert = db_dst.cursor() 
    cursor_insert.execute("SELECT name FROM cities")
    for element in cursor_insert:
        city = City(name=element)
        cities.append(city)
    return jsonify([city.__dict__ for city in cities]), 201


@app.route('/api/cities/', methods=['POST'])
def get_city():
    data = request.get_json()
    cursor_insert = db_dst.cursor() 
    cursor_insert.execute("SELECT name FROM cities")
    city = City(name=data['name'])
    cities.append(city)
    return jsonify([city.__dict__ for city in cities]), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
