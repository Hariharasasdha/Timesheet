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
    SQLALCHEMY_DATABASE_URI = os.getenv('COMMON_DB_URL',"postgresql+psycopg2://ipss_dev:AT4eqHUYr98475fhdNcuaRsDev@142.93.209.90:5433/ipss_dev")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True
    }
    IS_WORKER = False
    IPSS_PERMISSIONS = [{
        'module_name': "Timesheet Entry",
        'module_group': "Employee Activities",
        'module_id': "Timesheet_ID",
        'module_description': "Employees logging their efforts against project activities.",
        'project_id': "Timesheet Management",
        'permissions': ['list', 'view', 'add', 'edit', 'delete', 'import', 'export', 'submit']
    },
        {
        'module_name': "Approve or Reject timesheet",
        'module_group': "Manager Activities",
        'module_id': "Timesheet_Reportees_ID",
        'module_description': "Managers can review and approve/reject their reportees timesheet.",
        'project_id': "Timesheet Management",
        'permissions': ['approve', 'reportees']
    }]
    SQLALCHEMY_ECHO = True
