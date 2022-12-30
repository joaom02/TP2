import sys
import time
import requests
import psycopg2
from geopy.geocoders import Nominatim
import json

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60
ENTITIES_PER_ITERATION = int(sys.argv[2]) if len(sys.argv) >= 3 else 10

if __name__ == "__main__":

    while True:
        db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        cursor = db_dst.cursor()

        cursor.execute("SELECT latitude FROM cities")

        for element in cursor:
            print(type(element))
            print(element)
        print(f"Getting up to {ENTITIES_PER_ITERATION} entities without coordinates...")
        # !TODO: 1- Use api-gis to retrieve a fixed amount of entities without coordinates (e.g. 100 entities per iteration, use ENTITIES_PER_ITERATION)
        entries={
            "ENTITIES_PER_ITERATION":ENTITIES_PER_ITERATION,     
        }
    
        try:

            url='http://api-gis:8080/api/retrive/'
            x = requests.post(url,json=entries)
            cities=x.json()
        except(Exception, psycopg2.Error) as error:
            print(error)

        # !TODO: 2- Use the entity information to retrieve coordinates from an external API

        geolocator = Nominatim(user_agent="MyApp")
        
        i=1
        for city in cities:
            
            location = geolocator.geocode(cities[""+str(i)+""]["name"])
            cities[""+str(i)+""]["latitude"] = location.latitude
            cities[""+str(i)+""]["longitude"] = location.longitude
            i+=1
        
        try:

            url='http://api-gis:8080/api/save/'
            x = requests.post(url,json=cities)
            print(x.text)
        except(Exception, psycopg2.Error) as error:
            print(error)

        


        # !TODO: 3- Submit the changes
        time.sleep(POLLING_FREQ)
