import fastwsgi
import os

from config import settings
from database import init_database
from handler import Handler


def app(environ, start_response):
    return Handler(environ, start_response).run()

if __name__ == "__main__":

    if not os.path.exists(settings.database_file):
        init_database(settings.init_sql_file)
    fastwsgi.run(wsgi_app=app, host=settings.server_host, port=settings.server_port)

