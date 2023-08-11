from flask_restx import fields

# grade list response
category_fields = {
    'category_mast_id': fields.Integer,
    'category_name': fields.String,
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
