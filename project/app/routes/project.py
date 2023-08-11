from flask_restx import Namespace, Resource, fields
from ..api_doc import project_fields, activity_fields
from ipss_utils.ipss_api_doc import create_record_response, update_record_response, list_response_model

# Initialize API routes

project_api_route = Namespace('Project', path='/project')

# List project API docs
project_model = project_api_route.model('project_model', {
    **project_fields,
    'created_username': fields.String
})

project_list_response = project_api_route.model('project_list_response', {
    **list_response_model,
    **{
        'results': fields.List(fields.Nested(project_model))
    }
})

# Create project model
create_project_model = project_api_route.model('create_project_model', project_fields)
create_project_response = project_api_route.model('create_project_response', create_record_response)

# Get project records model
get_project_response = project_api_route.model('get_project_response', project_fields)

# Update project record
update_project_fields = project_fields
update_project_model = project_api_route.model('update_project_model', update_project_fields)
update_project_response = project_api_route.model('update_project_response', update_record_response)

##############################################

# Initialize API routes

activity_api_route = Namespace('Main Activities', path='/project/main_activity')

# List main activity API docs
activity_model = activity_api_route.model('activity_model', {
    **activity_fields,
    'deleted': fields.Boolean,
    'created_on': fields.String,
    'modified_on': fields.String
})

activity_list_response = activity_api_route.model('activity_list_response', {
    **list_response_model,
    **{
        'results': fields.List(fields.Nested(activity_model))
    }
})

# Create main activity model

create_activity_model = activity_api_route.model('create_activity_model', activity_fields)
create_activity_response = activity_api_route.model('create_activity_response', create_record_response)

# Get main activity records model
get_activity_response = activity_api_route.model('get_activity_response', activity_fields)

# Update main activity record
update_activity_fields = activity_fields
update_activity_model = activity_api_route.model('update_activity_model',
                                                 update_activity_fields)
update_activity_response = activity_api_route.model('update_activity_response', update_record_response)
# activity get all
activity_get_model = activity_api_route.model('activity_get_model', activity_fields)
activity_get_response = activity_api_route.model('activity_get_response', {
    'length': fields.Integer,
    'result': fields.List(fields.Nested(activity_get_model))
})
