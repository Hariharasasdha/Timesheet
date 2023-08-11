import os
from datetime import timedelta


class Config:
    # SERVER_NAME = "127.0.0.1:5000"
    CACHE_TYPE = "redis"
    CACHE_REDIS_HOST = "redis"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = REDIS_URL = os.getenv("redis://default:redispw@localhost:49158")
    CACHE_DEFAULT_TIMEOUT = 500
    SQLALCHEMY_DATABASE_URI = r'sqlite:///C:\\Users\\Hariharasasdha\\Desktop\ecom.s3db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    pool_pre_ping = True
    SQLALCHEMY_ECHO = True
    IS_WORKER = False
    IPSS_PERMISSIONS = [{
        'module_name': "Organization Report",
        'module_group': "Reports",
        'module_id': "ts_organization_report_id",
        'module_description': "Timesheet submission and approval status report. [for HR's/ Managers]",
        'project_id': "Timesheet Management",
        'permissions': ['view', 'export']
    },
        {
            'module_name': "Status Report",
            'module_group': "Reports",
            'module_id': "ts_daily_report_id",
            'module_description': "The HR or Admin has the ability to monitor whether their employees submit their daily timesheet, including the hours worked.",
            'project_id': "Timesheet Management",
            'permissions': ['view', 'export']
        }
    ]
