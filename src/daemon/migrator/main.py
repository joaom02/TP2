import sys
import time

import psycopg2
from psycopg2 import OperationalError
import requests
import json

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60


def print_psycopg2_exception(ex):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print("\npsycopg2 ERROR:", ex, "on line number:", line_num)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print("\nextensions.Diagnostics:", ex.diag)

    # print the pgcode and pgerror exceptions
    print("pgerror:", ex.pgerror)
    print("pgcode:", ex.pgcode, "\n")

    

if __name__ == "__main__":

    

    while True:

        # Connect to both databases
        db_org = None
        

        try:
            db_org = psycopg2.connect(host='db-xml', database='is', user='is', password='is')
            cursor_org = db_org.cursor()
            
            # !TODO: 1- Execute a SELECT query to check for any changes on the table
            cursor_org.execute("SELECT file_name FROM imported_documents WHERE file_name NOT IN (SELECT file_name FROM converted_documents);")

            for file_name in cursor_org:
               
                cities=[]
                companies=[]
                jobs=[]

                 # !TODO: 2- Execute a SELECT queries with xpath to retrieve the data we want to store in the relational db
                name=str(file_name).split("'")
                cursor_data=db_org.cursor()
                
                cursor_data.execute("SELECT unnest(xpath('//City/@name',xml)) FROM imported_documents WHERE file_name='"+str(name[1])+"'")
                
                for element in cursor_data:
                    city = {
                    "name":element[0]
                    }
                    cities.append(city)
                   
                #!TODO: 3- Execute INSERT queries in the destination db
                #Mandar para a API
                
                try:
                    url='http://api-entities:8080/api/cities/insert/'
                    x = requests.post(url,json=json.dumps(cities))
                except(Exception, psycopg2.Error) as error:
                    print(error)

                
            
                cursor_data.execute("SELECT unnest(xpath('//Company/Name/text()',xml)),unnest(xpath('//Company/Rating/text()',xml)) FROM imported_documents WHERE file_name='"+str(name[1])+"'")

                for element in cursor_data:
                    company = {
                        "name":element[0],
                        "rating":element[1]
                    }
                    companies.append(company)

                #!TODO: 3- Execute INSERT queries in the destination db
                #Mandar para a API
                
                try:
                    url='http://api-entities:8080/api/companies/insert/'
                    x = requests.post(url,json=json.dumps(companies))
                except(Exception, psycopg2.Error) as error:
                    print(error)
                
               

                cursor_data.execute("SELECT unnest(xpath('//Job/Name/text()',xml)),unnest(xpath('//Job/Summary/text()',xml)),unnest(xpath('//Job/City/@ref',xml)),unnest(xpath('//Job/@id',xml)) FROM imported_documents WHERE file_name='"+str(name[1])+"'")

                for element in cursor_data:
                    print(element[3])
                    jobid=element[3]
                    jobname = str(element[0]).replace("'","\'")
                    summary = str(element[1]).replace("'","\'")
                    cursor_temp = db_org.cursor()
                    cursor_temp.execute("SELECT unnest(xpath('//Company[Jobs/Job/@id=''"+jobid+"'']/Name/text()',xml)) FROM imported_documents WHERE file_name='"+str(name[1])+"'")
                    for company in cursor_temp:
                        companyname = company[0] 
                    print(companyname)
                    
                    cursor_temp.execute("SELECT unnest(xpath('//City[@id="+str(element[2])+"]/@name',xml)) FROM imported_documents WHERE file_name='"+str(name[1])+"'")
                    for city in cursor_temp:
                        cityid = city[0]
                    job = {
                        "name":jobname,
                        "companyname":companyname,
                        "cityname":cityid,
                        "summary":summary
                    }
                    jobs.append(job)
                
                #!TODO: 3- Execute INSERT queries in the destination db
                #Mandar para a API
                try:
                    url='http://api-entities:8080/api/jobs/insert/'
                    x = requests.post(url,json=json.dumps(jobs))
                except(Exception, psycopg2.Error) as error:
                    print(error)
                
                
                # !TODO: 4- Make sure we store somehow in the origin database that certain records were already migrated.
                #          Change the db structure if needed.

                cursor_store = db_org.cursor()

                cursor_store.execute("INSERT INTO converted_documents (file_name) values ('"+str(name[1])+"')")
                db_org.commit()
                
                
               
            
                

        except OperationalError as err:
            print_psycopg2_exception(err)

        if db_org is None:
            continue

        print("Checking updates...")
        

        db_org.close()
        

        time.sleep(POLLING_FREQ)
