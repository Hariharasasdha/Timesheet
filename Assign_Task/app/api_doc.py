from flask_restx import fields

# task list response
task_fields = {
    'task_id': fields.Integer,
    'emp_id': fields.Integer,
    'manager_id': fields.Integer,
    'from_date': fields.String,
    'to_date': fields.String,
    'task': fields.String,
    'sub_task': fields.String,
    'category': fields.String,
    'project_id': fields.Integer,
    'task_mast_id': fields.Integer,
    'category_mast_id': fields.Integer,
    'page_id': fields.Integer,
    'description': fields.String,
    'compcode': fields.Integer,
    'modified_by': fields.String,
    'modified_on': fields.String,
    'created_by': fields.String,
    'created_on': fields.String,
    'deleted': fields.Boolean,
    'deleted_at': fields.String
}
# search params
search_filter = {
    'start_date': {
        'type': 'str',
        'description': "from_date"
    },
    'end_date': {
        'type': 'str',
        'description': "to_date"
    },
    'employee_id': {
        'type': 'int',
        'description': "emp_id"
    },
    'manager_id': {
        'type': 'int',
        'description': "manager_id"
    }
}
