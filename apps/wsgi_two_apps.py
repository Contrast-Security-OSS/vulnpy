import sys
from wsgiref.simple_server import make_server

from wsgi_app import make_app

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000

    app1 = make_app()

    app2 = make_app()

    httpd = make_server(host, port, app1)
    print("WSGI app starting on http://{}:{}".format(host, port))
    httpd.handle_request()

    second_port = port + 1
    httpd2 = make_server(host, second_port, app2)
    print("WSGI app starting on http://{}:{}".format(host, second_port))
    httpd2.handle_request()
