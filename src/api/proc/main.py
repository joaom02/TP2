import sys
import xmlrpc.client
from flask import Flask

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/PrimeiraRotina', methods=['GET'])
def get_Jobs_in_city():
    server = xmlrpc.client.ServerProxy('http://rpc-server:9000')
    teste = server.PrimeiraRotina("San Francisco Bay Area")


    return str(teste)

@app.route('/api/SegundaRotina', methods=['GET'])
def get_Companies_by_rating():
    server = xmlrpc.client.ServerProxy('http://rpc-server:9000')
    teste = server.SegundaRotina("3")


    return str(teste)

@app.route('/api/TerceiraRotina', methods=['GET'])
def get_Number_of_Available_Jobs_by_Company():
    server = xmlrpc.client.ServerProxy('http://rpc-server:9000')
    teste = server.TerceiraRotina("CapitalPlanHoldings")


    return str(teste)

@app.route('/api/QuartaRotina', methods=['GET'])
def get_random_job():
    server = xmlrpc.client.ServerProxy('http://rpc-server:9000')
    teste = server.QuartaRotina()


    return str(teste)

@app.route('/api/QuintaRotina', methods=['GET'])
def get_Companies_with_jobs_in_a_city():
    server = xmlrpc.client.ServerProxy('http://rpc-server:9000')
    teste = server.QuintaRotina('San Francisco Bay Area')


    return str(teste)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
