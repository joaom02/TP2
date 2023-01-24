import sys

import graphene
from flask import Flask,request,jsonify
from flask_graphql import GraphQLView
import json
import psycopg2
import random

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000
connection = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
cursor = connection.cursor()



app = Flask(__name__)
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
app.config["DEBUG"] = True

class Query(graphene.ObjectType):

    PrimeiraRotina = graphene.String(city=graphene.Argument(graphene.String, default_value="San Francisco"))

    def resolve_PrimeiraRotina(self, info, city):
        result=[]
        cityid = []
        coiso = "SELECT id FROM cities where name ='" + city+"'"
        cursor.execute(coiso)
        for row in cursor:
            for e in row:
                if e not in cityid:
                    cityid.append(e)
        
        for id in cityid:
            cursor.execute("SELECT name FROM jobs where cityref = '"+str(id)+"' LIMIT 20")

            for row in cursor:
                for e in row:
                    if e not in result:
                        result.append(e)  
        
        return json.dumps(result)
    

    SegundaRotina = graphene.String(rate=graphene.Argument(graphene.String, default_value="3"))

    def resolve_SegundaRotina(self,info,rate):
        result=[]
        
        sql = "SELECT name FROM companies where rating >= '"+rate+"' LIMIT 20"
        cursor.execute(sql)
        
        
        for row in cursor:    
            for e in row:
                if e not in result:
                    result.append(e)

        return  json.dumps(result)

    
    TerceiraRotina = graphene.String(CompanyName=graphene.Argument(graphene.String, default_value="Microsoft"))

    def resolve_TerceiraRotina(self,info,CompanyName):
        result=[]
        companyid = []
        coiso = "SELECT id FROM companies where name ='" + CompanyName+"'"
        cursor.execute(coiso)
        for row in cursor:
            for e in row:
                if e not in companyid:
                    companyid.append(e)
        print(companyid)
        for id in companyid:
            cursor.execute("SELECT name FROM jobs where companyid = '"+str(id)+"' LIMIT 20")

            for row in cursor:
                for e in row:
                    if e not in result:
                        result.append(e)  

        return json.dumps(result)


    QuartaRotina = graphene.String()

    def resolve_QuartaRotina(self,info):
        result=[]
        jobid = random.randint(0,560)
        job={}

        cursor.execute("SELECT name, companyid, cityref,summary FROM jobs ORDER BY RANDOM() LIMIT 1")

        for element in cursor:
            cursor_temp = connection.cursor()
            cursor_temp2 = connection.cursor()
            summary = str(element[3]).replace("'"," ")
            cursor_temp.execute("SELECT name FROM cities where id = '"+element[2]+"'")
            for city in cursor_temp:
                cityName = city[0]
                cursor_temp2.execute("SELECT name FROM companies where id ='"+element[1]+"'")
                for company in cursor_temp2:
                    companyName = company[0]
        
                job = {
                            "name":element[0],
                            "companyname":companyName,
                            "cityname":cityName,
                            "summary":summary
                        }
            result.append(job)

        return  json.dumps(result)


    QuintaRotina = graphene.String(city=graphene.Argument(graphene.String, default_value="San Francisco"))

    def resolve_QuintaRotina(self, info, city):
        result=[]
        cityid = []
        
        coiso = "SELECT id FROM cities where name ='" + city+"'"
        cursor.execute(coiso)
        for row in cursor:
            for e in row:
                if e not in cityid:
                    cityid.append(e)
        
        for id in cityid:
            cursor.execute("SELECT c.name FROM companies c, jobs j where j.companyid = c.id AND j.cityref = '"+str(id)+"' LIMIT 20")

            for row in cursor:
                for e in row:
                    if e not in result:
                        result.append(e)   

        return json.dumps(result)


schema = graphene.Schema(query=Query)




@app.route('/graphql/PrimeiraRotina', methods=['GET'])
def get_Jobs_in_city():
    response = request.args.get('name')
    result = schema.execute(
    '''
    {
        PrimeiraRotina(city: "'''+str(response)+ '''")
    }
    '''
    )   
   


    return jsonify(result.data['PrimeiraRotina'])




@app.route('/graphql/SegundaRotina', methods=['GET'])
def get_Companies_by_rating():
    response = request.args.get('name')
    
    result = schema.execute(
    '''
    {
        SegundaRotina(rate: "'''+str(response)+ '''")
    }
    '''
    )   

    return jsonify(result.data['SegundaRotina'])


@app.route('/graphql/TerceiraRotina', methods=['GET'])
def get_Number_of_Available_Jobs_by_Company():
    response = request.args.get('name')
    result = schema.execute(
    '''
    {
        TerceiraRotina(CompanyName: "'''+str(response)+ '''")
    }
    '''
    )   

    return jsonify(result.data['TerceiraRotina'])


@app.route('/graphql/QuartaRotina', methods=['GET'])
def get_random_job():
    result = schema.execute(
    '''
    {
        QuartaRotina
    }
    '''
    )   

    return jsonify(result.data['QuartaRotina'])

@app.route('/graphql/QuintaRotina', methods=['GET'])
def get_Companies_with_jobs_in_a_city():
    response = request.args.get('name')
    result = schema.execute(
    '''
    {
        QuintaRotina(city: "'''+str(response)+ '''")
    }
    '''
    )   

    return jsonify(result.data['QuintaRotina'])


if __name__ == '__main__':

    app.config["DEBUG"] = True
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))
    app.run(host="0.0.0.0", port=PORT)
