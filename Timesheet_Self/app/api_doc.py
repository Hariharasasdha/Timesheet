from flask_restx import fields

# self list response
self_fields = {
    'self_id': fields.Integer,
    'sheet_id': fields.Integer,
    'emp_id': fields.Integer,
    'task_id': fields.Integer,
    'sub_task_id': fields.Integer,
    'category_id': fields.Integer,
    'project_id': fields.Integer,
    'page_id': fields.Integer,
    'description': fields.String,
    'mon': fields.String,
    'tue': fields.String,
    'wed': fields.String,
    'thu': fields.String,
    'fri': fields.String,
    'sat': fields.String,
    'sun': fields.String,
    'hrs_per_task': fields.String,
    'compcode': fields.Integer,
    'modified_by': fields.String,
    'modified_on': fields.String,
    'created_by': fields.String,
    'created_on': fields.String,
    'deleted': fields.Boolean,
    'deleted_at': fields.String
}

# timesheet list response
timesheet_fields = {
    'sheet_id': fields.Integer,
    'emp_id': fields.Integer,
    'from_date': fields.String,
    'to_date': fields.String,
    'date': fields.String,
    'total_hrs': fields.String,
    'send': fields.Boolean,
    'sent_at': fields.String,
    'status': fields.String,
    'status_at': fields.String,
    'reason':fields.String,
    'compcode': fields.Integer,
    'modified_by': fields.String,
    'modified_on': fields.String,
    'created_by': fields.String,
    'created_on': fields.String,
    'deleted': fields.Boolean,
    'deleted_at': fields.String
}

search_filter = {
    'start_date': {
        'from_date': 'str',
        'description': "from_date"
    },
    'end_date': {
        'to_date': 'str',
        'description': "to_date"
    },
    'employee_id': {
        'emp_id': 'int',
        'description': "emp_id"
    },
    'manager': {
        'type': 'str',
        'description': "YES"
    }

}
sheet_params = {
    'hours': {
        'hrs_per_task': 'str',
        'description': "Hours to update",
        'required': True
    },
    'sheet_id': {
        'sheet_id': 'int',
        'description': "Sheet_id",
        'required': True
    }

}

############################################################

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

search_filters = {
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

# activity_fields = {
#     'activity_id': fields.Integer,
#     'project_id': fields.Integer,
#     'activity_name': fields.String,
#     'description': fields.String,
#     'compcode': fields.Integer,
#     'modified_by': fields.String,
#     'modified_on': fields.String,
#     'created_by': fields.String,
#     'created_on': fields.String,
#     'deleted': fields.Boolean,
#     'deleted_at': fields.String
# }
project_fields = {
    'project_id': fields.Integer,
    'project_name': fields.String,
    'description': fields.String,
    'from_date': fields.String,
    'to_date': fields.String,
    'compcode': fields.Integer,
    'modified_by': fields.String,
    'modified_on': fields.String,
    'created_by': fields.String,
    'created_on': fields.String,
    'deleted': fields.Boolean,
    'deleted_at': fields.String
}