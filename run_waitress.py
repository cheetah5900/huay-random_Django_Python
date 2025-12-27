import os
from waitress import serve
from betmanager.wsgi import application

if __name__ == "__main__":
    print("Starting Waitress server on http://0.0.0.0:8001")
    serve(application, host='0.0.0.0', port=8001, threads=10)
