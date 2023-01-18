import psycopg2


def SegundaRotina(rate):
    connection = None
    cursor = None
    result=[]
    
  
    try:
        connection = psycopg2.connect(host='db-xml', database='is', user='is', password='is')

        cursor = connection.cursor()
        sql = "SELECT unnest(xpath('/JobDataset/Companies/Company[Rating>=''"+rate+"'']/Name/text()',xml)) from imported_documents LIMIT 20"
        cursor.execute(sql)
      
        
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