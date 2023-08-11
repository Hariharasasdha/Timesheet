import os
from datetime import timedelta


class Config:
    # SERVER_NAME = "127.0.0.1:5000"
    CACHE_TYPE = "redis"
    CACHE_REDIS_HOST = "redis"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = REDIS_URL = os.getenv("REDIS_DB_URL", "redis://default:redispw@localhost:49153")
    CACHE_DEFAULT_TIMEOUT = 500
    SQLALCHEMY_DATABASE_URI =r'sqlite:///C:\\Users\\Hariharasasdha\\Desktop\ecom.s3db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True
    }
    SQLALCHEMY_ECHO = True
    IS_WORKER = False
    IPSS_PERMISSIONS = [{
        'module_name': "Sub Task Configuration",
        'module_group': "Admin Configuration",
        'module_id': "Category_Config_ID",
        'module_description': "One time configuration of organization level subtasks.",
        'project_id': "Timesheet Management",
        'permissions': ['list', 'view', 'add', 'edit', 'delete', 'import', 'export']
    }]
