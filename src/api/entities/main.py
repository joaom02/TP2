import sys

from flask import Flask, jsonify, request
import psycopg2
import json
from entities import City
from entities import Job
from entities import Company

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

# set of all teams
# !TODO: replace by database access
db_dst = None



app = Flask(__name__)
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
app.config["DEBUG"] = True



@app.route('/api/cities/insert/',methods=['POST','GET'])
def insert_cities():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
    data = request.get_json()
    cursor_insert = db_dst.cursor() 
    cities = json.loads(data)
    for city in cities:
        cursor_insert.execute("SELECT * FROM cities WHERE name = '"+city["name"]+"'")
        temp = cursor_insert.fetchall()

        if len(temp) == 0:
            cursor_insert.execute("INSERT INTO cities (name) values ('"+city["name"]+"')")

    db_dst.commit()
    db_dst.close()
    return data



@app.route('/api/companies/insert/',methods=['POST'])
def insert_companies():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
    cursor_insert = db_dst.cursor() 
    data = request.get_json()
    companies = json.loads(data)

    for company in companies:
        cursor_insert.execute("SELECT * FROM companies WHERE name = '"+company["name"]+"'")
        temp = cursor_insert.fetchall()

        if len(temp) == 0:
            cursor_insert.execute("INSERT INTO companies (name,rating) values ('"+company["name"]+"','"+company["rating"]+"')")

    db_dst.commit()
    db_dst.close()
    return data


@app.route('/api/jobs/insert/',methods=['POST'])
def insert_jobs():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
    data = request.get_json()
    cursor_insert = db_dst.cursor()
    jobs = json.loads(data)

    for job in jobs:

        cursor_insert.execute("SELECT id FROM companies WHERE name = '"+str(job["companyname"])+"'")
        for e in cursor_insert:
            companyname=e[0]
        

        cursor_insert.execute("SELECT id FROM cities WHERE name = '"+str(job["cityname"])+"'")
        for e in cursor_insert:
            cityname=e[0]
        
        summary = str(job["summary"]).replace("'"," ")
        name = str(job["name"]).replace("'"," ")
        cursor_insert.execute("INSERT INTO jobs (name,companyid,cityref,summary) values ('"+name+"','"+str(companyname)+"','"+str(cityname)+"','"+summary+"')")
        db_dst.commit()
    
    db_dst.close()
    return "top"


@app.route('/api/companies/get/', methods=['GET'])
def get_companies():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
    companies = []
    
    cursor_insert = db_dst.cursor() 
    cursor_insert.execute("SELECT id, name, rating, created_on, updated_on FROM companies")
    for element in cursor_insert:
        company = Company(name=element[1], id = element[0], rating = element[2], created_on = element[3], updated_on = element[4])
        companies.append(company)
    return jsonify([company.__dict__ for company in companies]), 201


@app.route('/api/cities/get/', methods=['GET'])
def get_cities():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
    cities = []
    
    cursor_insert = db_dst.cursor() 
    cursor_insert.execute("SELECT id, name, latitude, longitude, created_on, updated_on FROM cities")
    for element in cursor_insert:
        city = City(name=element[1], id = element[0], latitude = element[2], longitude = element[3], created_on = element[4], updated_on = element[5])
        cities.append(city)
    return jsonify([city.__dict__ for city in cities]), 201

@app.route('/api/city/get/', methods=['GET'])
def get_city():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
    cities = []
    cursor_insert = db_dst.cursor() 
    cursor_insert.execute("SELECT name FROM cities")
    for element in cursor_insert:
        city = element
        cities.append(city)
    return jsonify([city for city in cities]), 201


@app.route('/api/jobs/get/', methods=['GET'])
def get_jobs():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
    jobs = []
    
    cursor_insert = db_dst.cursor() 
    cursor_insert.execute("SELECT id, name, summary, created_on, updated_on FROM jobs")
    for element in cursor_insert:
        job = Job(name=element[1], id = element[0], summary= element[2],  created_on = element[3], updated_on = element[4])
        jobs.append(job)
    return jsonify([job.__dict__ for job in jobs]), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
