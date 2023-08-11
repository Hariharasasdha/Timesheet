from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_restx import Api
from ipss_utils.ipss_db import IpssDb
from ipss_utils.ipss_api_doc import authorization_api_doc
import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from ipss_utils.redis.ipss_redis import IpssRedis
from flask_redis import Redis

db_client = SQLAlchemy()
db_cache = Cache()
redis = Redis()
ipss_redis = IpssRedis()
rest_api = Api(
    title="Page Configuration API",
    doc="/page_config/api-docs",
    authorizations=authorization_api_doc,
    security='api_key',
    base_url="/page_config",
    url_scheme="http"
)
ipss_db = IpssDb()


def create_app(config):
    app = Flask(
        __name__
    )
    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db_client.init_app(app)
    db_cache.init_app(app)
    redis.init_app(app)
    ipss_redis.init_app(app, redis)
    # Registering routes
    rest_api.init_app(app)
    ipss_db.init_app(app, db_client)

    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[FlaskIntegration()]
    )

    with app.app_context():
        # Register route blueprints
        # from .api import user_routes
        # app.register_blueprint(user_routes
        # from .api.employees import employees_api_route
        # rest_api.add_namespace(employees_api_route)
        from .api.page import page_api_route
        rest_api.add_namespace(page_api_route)  # sku_match_api_route
        if not current_app.config.get('IS_WORKER'):
            ipss_redis.load_module()
        # from .api.notification import sku_match_api_route
        # rest_api.add_namespace(sku_match_api_route)
        #        from .api.form import form_api_route
        # from .api.grn_mange import vehicle_api_route_bulk
        #
        # rest_api.add_namespace(form_api_route)
        # rest_api.add_namespace(vehicle_api_route_bulk)
        return app
