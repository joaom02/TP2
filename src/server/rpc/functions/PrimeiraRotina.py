import psycopg2


def PrimeiraRotina(cityName):
    connection = None
    cursor = None
    result=[]
    city = []
  
    try:
        connection = psycopg2.connect(host='db-xml', database='is', user='is', password='is')
        cursor = connection.cursor()
        
        coiso = "SELECT unnest(xpath('//JobDataset/Cities/City[@name =''"+cityName+"'']/@id',xml)) FROM imported_documents"
        cursor.execute(coiso)
        for row in cursor:
            for e in row:
                if e not in city:
                    city.append(e)

        
        for id in city:
            cursor.execute("SELECT unnest(xpath('//JobDataset/Companies/Company/Jobs/Job[City/@ref =''"+str(id)+"'' ]/Name/text()',xml)) FROM imported_documents LIMIT 20 ")

            for row in cursor:
                for e in row:
                    if e not in result:
                        result.append(e)  

        
              
        
       
    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)
        

    finally:
        if connection:
            
            cursor.close()
            
            connection.close()

    return result