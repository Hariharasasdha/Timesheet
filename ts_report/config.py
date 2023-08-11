import os
from datetime import timedelta


class Config:
    # SERVER_NAME = "127.0.0.1:5000"
    CACHE_TYPE = "redis"
    CACHE_REDIS_HOST = "redis"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = REDIS_URL = os.getenv("redis://default:redispw@localhost:49153")
    CACHE_DEFAULT_TIMEOUT = 500
    SQLALCHEMY_DATABASE_URI = os.getenv("COMMON_DB_URL","postgresql+psycopg2://ipss_dev:AT4eqHUYr98475fhdNcuaRsDev@142.93.209.90:5433/ipss_dev")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    pool_pre_ping = True
    SQLALCHEMY_ECHO = True
    IS_WORKER = False
    IPSS_PERMISSIONS = [{
        'module_name': "Manager Report",
        'module_group': "Reports",
        'module_id': "ts_report_id",
        'module_description': "Report of timesheet data between given dates based on the role.",
        'project_id': "Timesheet Management",
        'permissions': ['view', 'export']
    }]
