import os
from datetime import timedelta


class Config:
    # SERVER_NAME = "127.0.0.1:5000"
    CACHE_TYPE = "redis"
    CACHE_REDIS_HOST = "redis"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = REDIS_URL = os.getenv("REDIS_DB_URL", "redis://localhost:6379/0")
    CACHE_DEFAULT_TIMEOUT = 500
    SQLALCHEMY_DATABASE_URI = r'sqlite:///C:\\Users\\Hariharasasdha\\Desktop\ecom.s3db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True
    }
    IS_WORKER = False
    IPSS_PERMISSIONS = [{
        'module_name': "Assign Project",
        'module_group': "Manager Activities",
        'module_id': "Assign_Task_ID",
        'module_description': "Managers can manage teams who can be part of a given project.",
        'project_id': "Timesheet Management",
        'permissions': ['list', 'view', 'add', 'edit', 'delete', 'import', 'export']
    }]
    SQLALCHEMY_ECHO = True
