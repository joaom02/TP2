import signal, sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from functions.PrimeiraRotina import PrimeiraRotina
from functions.SegundaRotina import SegundaRotina
from functions.TerceiraRotina import TerceiraRotina
from functions.QuartaRotina import QuartaRotina
from functions.QuintaRotina import QuintaRotina

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

if __name__ == "__main__":
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)

    with SimpleXMLRPCServer(('0.0.0.0', PORT), requestHandler=RequestHandler) as server:
        server.register_introspection_functions()

        def signal_handler(signum, frame):
            print("received signal")
            server.server_close()

            # perform clean up, etc. here...
            print("exiting, gracefully")
            sys.exit(0)

        # signals
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGHUP, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

        # register both functions
        server.register_function(PrimeiraRotina)
        server.register_function(SegundaRotina)
        server.register_function(TerceiraRotina)
        server.register_function(QuartaRotina)
        server.register_function(QuintaRotina)
       

        # start the server
        print(f"Starting the RPC Server in port {PORT}...")
        server.serve_forever()
