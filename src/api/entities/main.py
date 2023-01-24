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


#inserts the cities received from the db-xml in the db-rel 
@app.route('/api/cities/insert/',methods=['POST','GET'])
def insert_cities():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
    cursor = db_dst.cursor()
    data = request.get_json()
     
    cities = json.loads(data)
    for city in cities:
        cursor.execute("SELECT * FROM cities WHERE name = '"+city["name"]+"'")
        temp = cursor.fetchall()

        if len(temp) == 0:
            cursor.execute("INSERT INTO cities (name) values ('"+city["name"]+"')")

    db_dst.commit()
    db_dst.close()
    return data


#inserts the companies received from the db-xml in the db-rel 
@app.route('/api/companies/insert/',methods=['POST'])
def insert_companies():
    data = request.get_json()
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
    cursor = db_dst.cursor()
    companies = json.loads(data)

    for company in companies:
        cursor.execute("SELECT * FROM companies WHERE name = '"+company["name"]+"'")
        temp = cursor.fetchall()

        if len(temp) == 0:
            cursor.execute("INSERT INTO companies (name,rating) values ('"+company["name"]+"','"+company["rating"]+"')")

    db_dst.commit()
    db_dst.close()
    return data

#inserts the jobs received from the db-xml in the db-rel 
@app.route('/api/jobs/insert/',methods=['POST'])
def insert_jobs():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
    cursor = db_dst.cursor()
    data = request.get_json()
    jobs = json.loads(data)
   
    for job in jobs:
        
        cursor.execute("SELECT id FROM companies WHERE name = '"+str(job["companyname"])+"'")
        for e in cursor:
            companyname=e[0]
        

        cursor.execute("SELECT id FROM cities WHERE name = '"+str(job["cityname"])+"'")
        for e in cursor:
            cityname=e[0]
        
        summary = str(job["summary"]).replace("'"," ")
        name = str(job["name"]).replace("'"," ")
        cursor.execute("INSERT INTO jobs (name,companyid,cityref,summary) values ('"+name+"','"+str(companyname)+"','"+str(cityname)+"','"+summary+"')")
        db_dst.commit()
    
    db_dst.close()
    return "top"

#returns all the companies in the relational dabase 
@app.route('/api/companies/get/', methods=['GET'])
def get_companies():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
    cursor = db_dst.cursor()
    companies = []
    
    cursor.execute("SELECT id, name, rating, created_on, updated_on FROM companies")
    for element in cursor:
        company = Company(name=element[1], id = element[0], rating = element[2], created_on = element[3], updated_on = element[4])
        companies.append(company)
    return jsonify([company.__dict__ for company in companies]), 201

#returns all the cities in the relational dabase 
@app.route('/api/cities/get/', methods=['GET'])
def get_cities():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
    cursor = db_dst.cursor()
    cities = []
    
    cursor.execute("SELECT id, name, latitude, longitude, created_on, updated_on FROM cities")
    for element in cursor:
        city = City(name=element[1], id = element[0], latitude = element[2], longitude = element[3], created_on = element[4], updated_on = element[5])
        cities.append(city)
    return jsonify([city.__dict__ for city in cities]), 201



#returns all the jobs in the relational dabase 
@app.route('/api/jobs/get/', methods=['GET'])
def get_jobs():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
    cursor = db_dst.cursor()
    jobs = []
    
    cursor.execute("SELECT id, name, summary, created_on, updated_on FROM jobs")
    for element in cursor:
        job = Job(name=element[1], id = element[0], summary= element[2],  created_on = element[3], updated_on = element[4])
        jobs.append(job)
    return jsonify([job.__dict__ for job in jobs]), 201



@app.route('/api/city/get/', methods=['GET'])
def get_city():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
    cursor = db_dst.cursor()
    cities = []

    cursor.execute("SELECT name FROM cities")
    for element in cursor:
        city = element
        cities.append(city)
    return jsonify([city for city in cities]), 201

@app.route('/api/company/get/', methods=['GET'])
def get_company():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
    cursor = db_dst.cursor()
    companies = []

    cursor.execute("SELECT name FROM companies")
    for element in cursor:
        company = element
        companies.append(company)
    return jsonify([company for company in companies]), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
