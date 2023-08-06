import json
import time

import pika
from deepmerge import always_merger
from flask import current_app, Blueprint
from invenio_base.signals import app_loaded
from invenio_db import db
from invenio_search import current_search_client
from redis import Redis


def check_rabbit(host):
    try:
        t1 = time.time()
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        t2 = time.time()
        if connection.is_open:
            connection.close()
            return {'RabbitMQ': {'connection': 'OK', 'time': t2-t1}}
    except Exception as error:
        return {'RabbitMQ': {'connection': json.dumps(str(error))}}

def check_db():
    try:
        t1 = time.time()
        db.session.execute('select 1').fetchall()
        t2 = time.time()
        return {'PostgreSQL': {'connection': 'OK', 'time': t2 - t1}}
    except Exception as error:
        return {'PostgreSQL': {'connection': json.dumps(str(error))}}

def check_redis(host):
    redis = Redis(host)
    try:
        t1 = time.time()
        redis.ping()
        t2 = time.time()
        return {'Redis': {'connection': 'OK', 'time': t2 - t1}}
    except Exception as error:
        return {'Redis': {'connection': json.dumps(str(error))}}

def check_es():
    try:
        t1 = time.time()
        current_search_client.indices.get_alias("*", request_timeout=10)
        t2 = time.time()
        return {'Elasticsearch': {'connection': 'OK', 'time': t2 - t1}}
    except Exception as error:
        return {'Elasticsearch': {'connection': json.dumps(str(error))}}

def health_check():
    with current_app.app_context():
        if current_app.config['SERVER_NAME'] == '127.0.0.1:5000':
            host = 'localhost'
        else:
            host = current_app.config['SERVER_NAME']
    response = {}
    always_merger.merge(response,check_rabbit(host) )
    always_merger.merge(response, check_db() )
    always_merger.merge(response, check_redis(host))
    always_merger.merge(response, check_es() )

    return response

def health_check_ext(sender, app=None, **kwargs):
    with app.app_context():
        health_check_bp = Blueprint("health_check", __name__, url_prefix=None, )
        health_check_bp.add_url_rule(rule='/health-check/', view_func=health_check, methods=['GET'])
        app.register_blueprint(health_check_bp)

class OARepoHealthCheck:
    def __init__(self, app=None, db=None):
        self.init_app(app, db)

    def init_app(self, app, db):
        app_loaded.connect(health_check_ext)