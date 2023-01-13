import sys

from flask import Flask, jsonify, request
import psycopg2
from entities import City
from entities import Job
from entities import Company

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

# set of all teams
# !TODO: replace by database access
cities = []
db_dst = None



app = Flask(__name__)
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
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


@app.route('/api/companies/get/', methods=['GET'])
def get_companies():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
    companies = []
    
    cursor_insert = db_dst.cursor() 
    cursor_insert.execute("SELECT id, name, rating FROM companies")
    for element in cursor_insert:
        company = Company(name=element[1], id = element[0], rating = element[2])
        companies.append(company)
    return jsonify([company.__dict__ for company in companies]), 201


@app.route('/api/cities/get/', methods=['GET'])
def get_cities():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
    cities = []
    
    cursor_insert = db_dst.cursor() 
    cursor_insert.execute("SELECT id, name, latitude, longitude FROM cities")
    for element in cursor_insert:
        city = City(name=element[1], id = element[0], latitude = element[2], longitude = element[3])
        cities.append(city)
    return jsonify([city.__dict__ for city in cities]), 201


@app.route('/api/jobs/get/', methods=['GET'])
def get_jobs():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
    jobs = []
    
    cursor_insert = db_dst.cursor() 
    cursor_insert.execute("SELECT id, name, summary FROM jobs")
    for element in cursor_insert:
        job = Job(name=element[1], id = element[0], summary= element[2])
        jobs.append(job)
    return jsonify([job.__dict__ for job in jobs]), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
