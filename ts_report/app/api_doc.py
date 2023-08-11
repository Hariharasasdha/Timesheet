from flask_restx import fields

# Employee register report

search_params = {
    'from_date': {
        'type': 'str',
        'description': "from_date"
    },
    'to_date': {
        'type': 'str',
        'description': "to_date"
    },
    'project_id': {
        'type': 'str',
        'description': "project_id"
    },
    'activity_id': {
        'type': 'str',
        'description': "activity_id"
    },
    'task_id': {
        'type': 'str',
        'description': "task_id"
    },
    'category_id': {
        'type': 'str',
        'description': "category_id"
    }
}

report_fields = {
    "emp_name": fields.String,
    "emp_company_id": fields.String,
    'from_date': fields.String,
    'to_date': fields.String,
    'status': fields.String,
    'send': fields.Boolean,
    'hrs_per_task': fields.String,
    'project_id': fields.Integer,
    'project_name': fields.String,
    'activity_id': fields.Integer,
    'activity_name': fields.String,
    'task_id': fields.Integer,
    'task_name': fields.String,
    # 'category_name': fields.String,
    # 'page_name': fields.String,

}
project_report_fields = {
    'project_id': fields.Integer,
    'project_name': fields.String,
    'description': fields.String,
    'from_date': fields.String,
    'to_date': fields.String,
}
