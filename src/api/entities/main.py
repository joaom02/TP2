import sys

from flask import Flask, jsonify, request
import psycopg2
from entities import Team

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

# set of all teams
# !TODO: replace by database access
teams = []
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


@app.route('/api/teams/', methods=['GET'])
def get_teams():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
    
    cursor_insert = db_dst.cursor()
    data={}
    cursor_insert.execute("SELECT name FROM cities")
    for name in cursor_insert:
        data= {
            "name":name
        } 

    return data


@app.route('/api/teams/', methods=['POST'])
def create_team():
    data = request.get_json()
    team = Team(name=data['name'])
    teams.append(team)
    return jsonify(team.__dict__), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
