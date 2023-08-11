from flask_restx import Namespace, Resource, fields
from ..api_doc import task_fields
from ipss_utils.ipss_api_doc import create_record_response, update_record_response, list_response_model

# Initialize API routes

task_api_route = Namespace('assign_task', path='/assign_task')

# List task API docs
task_model = task_api_route.model('task_model', {
    **task_fields,
    "emp_name": fields.String,
    "emp_company_id": fields.String,
    'project_name': fields.String,
    # 'task_name': fields.String,
    # 'category_name': fields.String,
    # 'page_name': fields.String,
    'deleted': fields.Boolean,
    'created_on': fields.String,
    'modified_on': fields.String
})

task_list_response = task_api_route.model('task_list_response', {
    **list_response_model,
    **{
        'results': fields.List(fields.Nested(task_model))
    }
})

# Create task model

create_task_model = task_api_route.model('create_task_model', task_fields)
create_task_response = task_api_route.model('create_task_response', create_record_response)

# Bulk post task model

bulk_post_model = task_api_route.model('bulk_post_model', task_fields)
bulk_post_response = task_api_route.model('bulk_post_response', {
    **{
        'data': fields.List(fields.Nested(bulk_post_model))}
})

# Get task records model
get_task_response = task_api_route.model('get_task_response', task_fields)

# Update user record
update_task_fields = task_fields
update_task_model = task_api_route.model('update_task_model', update_task_fields)
update_task_response = task_api_route.model('update_task_response', update_record_response)

##############################################
