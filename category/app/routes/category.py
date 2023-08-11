from flask_restx import Namespace, Resource, fields
from ..api_doc import category_fields
from ipss_utils.ipss_api_doc import create_record_response, update_record_response, list_response_model


# Initialize API routes

category_config_api_route = Namespace('category_config', path='/category_config')

# List category API docs
category_config_model = category_config_api_route.model('category_config_model', {
            **category_fields,
            'deleted': fields.Boolean,
            'created_on': fields.String,
            'modified_on': fields.String
        })

category_config_list_response = category_config_api_route.model('category_config_list_response', {
    **list_response_model,
    **{
        'results': fields.List(fields.Nested(category_config_model))
    }
})


# Create category_config model
create_category_config_model = category_config_api_route.model('create_category_config_model', category_fields)
create_category_config_response = category_config_api_route.model('create_category_config_response',
                                                                  create_record_response)

# Get category_config records model
get_category_config_response = category_config_api_route.model('get_category_config_response', category_fields)

# Update category_config record
update_category_config_fields = category_fields
update_category_config_model = category_config_api_route.model('update_category_config_model',
                                                               update_category_config_fields)
update_category_config_response = category_config_api_route.model('update_category_config_response',
                                                                  update_record_response)


##############################################
