import psycopg2
import random

def QuartaRotina():
    connection = None
    cursor = None
    result=[]
    jobid = random.randint(0,560)
    job={}
    try:
        connection = psycopg2.connect(host='db-xml', database='is', user='is', password='is')

        cursor = connection.cursor()
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
             

        

       
    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)
        

    finally:
        if connection:
            
            cursor.close()
            
            connection.close()

    return result