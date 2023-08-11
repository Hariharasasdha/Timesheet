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
        'module_name': "Project Definition",
        'module_group': "Manager Activities",
        'module_id': "Project_Config_ID",
        'module_description': "Managers can create projects.[can be later assigned to individuals]",
        'project_id': "Timesheet Management",
        'permissions': ['list', 'view', 'add', 'edit', 'delete', 'import', 'export']
    },
        {
            'module_name': "Project Activities",
            'module_group': "Manager Activities",
            'module_id': "Activity_ID",
            'module_description': "Managers can create major activities for the project.[employees fill timesheet "
                                  "against this]",
            'project_id': "Timesheet Management",
            'permissions': ['list', 'view', 'add', 'edit', 'delete', 'import', 'export']
        }
    ]

