from flask_restx import Namespace, Resource, fields
from ..api_doc import page_fields
from ipss_utils.ipss_api_doc import create_record_response, update_record_response, list_response_model


# Initialize API routes

page_api_route = Namespace('page_config', path='/page_config')

# List page_config API docs
page_model = page_api_route.model('page_model', {
            **page_fields,
            'deleted': fields.Boolean,
            'created_on': fields.String,
            'modified_on': fields.String
        })

page_list_response = page_api_route.model('page_list_response', {
    **list_response_model,
    **{
        'results': fields.List(fields.Nested(page_model))
    }
})


# Create page_config model
create_page_model = page_api_route.model('create_page_model', page_fields)
create_page_response = page_api_route.model('create_page_response', create_record_response)

# Get page_config records model
get_page_response = page_api_route.model('get_page_response', page_fields)

# Update page_config record
update_page_fields = page_fields
update_page_model = page_api_route.model('update_page_model', update_page_fields)
update_page_response = page_api_route.model('update_page_response', update_record_response)


##############################################
