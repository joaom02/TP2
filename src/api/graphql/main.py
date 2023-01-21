import sys

import graphene
from flask import Flask,request
from flask_graphql import GraphQLView
import json
import psycopg2
import random

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000
connection = psycopg2.connect(host='db-xml', database='is', user='is', password='is')
cursor = connection.cursor()

app = Flask(__name__)

class Query(graphene.ObjectType):

    PrimeiraRotina = graphene.String(city=graphene.Argument(graphene.String, default_value="San Francisco"))

    def resolve_PrimeiraRotina(self, info, city):
        result=[]
        cityid = []
        coiso = "SELECT unnest(xpath('//JobDataset/Cities/City[@name =''"+city+"'']/@id',xml)) FROM imported_documents"
        cursor.execute(coiso)
        for row in cursor:
            for e in row:
                if e not in cityid:
                    cityid.append(e)
        
        for id in cityid:
            cursor.execute("SELECT unnest(xpath('//JobDataset/Companies/Company/Jobs/Job[City/@ref =''"+str(id)+"'' ]/Name/text()',xml)) FROM imported_documents LIMIT 20 ")

            for row in cursor:
                for e in row:
                    if e not in result:
                        result.append(e)  

        return json.dumps(result)
    

    SegundaRotina = graphene.String(rate=graphene.Argument(graphene.String, default_value="3"))

    def resolve_SegundaRotina(self,info,rate):
        result=[]
        sql = "SELECT unnest(xpath('/JobDataset/Companies/Company[Rating>=''"+rate+"'']/Name/text()',xml)) from imported_documents LIMIT 20"
        cursor.execute(sql)
      
        
        for row in cursor:    
            for e in row:
                if e not in result:
                    result.append(e)

        return  json.dumps(result)

    
    TerceiraRotina = graphene.String(CompanyName=graphene.Argument(graphene.String, default_value="Microsoft"))

    def resolve_TerceiraRotina(self,info,CompanyName):
        result=[]
        sql = "SELECT unnest(xpath('/JobDataset/Companies/Company[Name/text()=''"+CompanyName+"'']/Jobs/Job/Name/text()',xml)) FROM imported_documents LIMIT 20"
        cursor.execute(sql)
        
        for row in cursor:
            for e in row:
                if e not in result:
                    result.append(e)

        return  json.dumps(result)


    QuartaRotina = graphene.String()

    def resolve_QuartaRotina(self,info,):
        result=[]
        jobid = random.randint(0,560)
        job={}

        cursor.execute("SELECT unnest(xpath('//Job[@id=''"+str(jobid)+"'']/Name/text()',xml)),unnest(xpath('//Job[@id=''"+str(jobid)+"'']/Summary/text()',xml)),unnest(xpath('//Company[Jobs/Job/@id=''"+str(jobid)+"'']/Name/text()',xml)),unnest(xpath('//Job[@id=''"+str(jobid)+"'']/City/@ref',xml)) FROM imported_documents LIMIT 20")

        for element in cursor:
            print(element)
            cursor_temp = connection.cursor()
            summary = str(element[1]).replace("'"," ")
            cursor_temp.execute("SELECT unnest(xpath('//City[@id="+str(element[3])+"]/@name',xml)) FROM imported_documents")
            for city in cursor_temp:
                companyName = city[0]
        
            job = {
                        "name":element[0],
                        "companyname":element[2],
                        "cityname":companyName,
                        "summary":summary
                    }
        result.append(job)

        return  json.dumps(result)


    QuintaRotina = graphene.String(city=graphene.Argument(graphene.String, default_value="San Francisco"))

    def resolve_QuintaRotina(self, info, city):
        result=[]
        cityid = []
        coiso = "SELECT unnest(xpath('//JobDataset/Cities/City[@name =''"+city+"'']/@id',xml)) FROM imported_documents"
        cursor.execute(coiso)
        for row in cursor:
            for e in row:
                if e not in cityid:
                    cityid.append(e)
        
        for id in cityid:
            cursor.execute("SELECT unnest(xpath('//JobDataset/Companies/Company[Jobs/Job/City/@ref =''"+str(id)+"'' ]/Name/text()',xml)) FROM imported_documents LIMIT 20 ")

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
   


    return json.dumps(result.data['PrimeiraRotina'])




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

    return json.dumps(result.data['SegundaRotina'])


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

    return json.dumps(result.data['TerceiraRotina'])


@app.route('/graphql/QuartaRotina', methods=['GET'])
def get_random_job():
    result = schema.execute(
    '''
    {
        QuartaRotina
    }
    '''
    )   

    return json.dumps(result.data['QuartaRotina'])

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

    return json.dumps(result.data['QuintaRotina'])


if __name__ == '__main__':

    app.config["DEBUG"] = True
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))
    app.run(host="0.0.0.0", port=PORT)
