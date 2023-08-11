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
    title="Timesheet Organization Report API",
    doc="/ts_organization_report/api-docs",
    authorizations=authorization_api_doc,
    security='api_key',
    base_url="/ts_organization_report",
    url_scheme="http"
)
ipss_db = IpssDb()


def create_app(config):
    app = Flask(
        __name__
    )
    app.config.from_object(config)

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
        from .api.ts_organization_report import ts_report_api_route
        rest_api.add_namespace(ts_report_api_route)
        # Passing module's permissions to user control.
        if not current_app.config.get('IS_WORKER'):
            ipss_redis.load_module()
        return app
