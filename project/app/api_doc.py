from flask_restx import fields

# project list response
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
# activity list response
activity_fields = {
    'activity_id': fields.Integer,
    'project_id': fields.Integer,
    'activity_name': fields.String,
    'description': fields.String,
    'compcode': fields.Integer,
    'modified_by': fields.String,
    'modified_on': fields.String,
    'created_by': fields.String,
    'created_on': fields.String,
    'deleted': fields.Boolean,
    'deleted_at': fields.String
}
get_all_messages = {'get_seen_messages': {
    'type': 'str',
    'description': "Pass 'SEEN' If you all mails"
}}

filter_params = {
    'project_id': {
        'type': 'int',
        'description': "project_id"
    }
}

params_search = {
    'project_id': {
        'type': 'str',
        'description': "project_id"
    }
}
