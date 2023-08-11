from flask_restx import Namespace, Resource, fields
from ..api_doc import timesheet_fields, self_fields, task_fields, project_fields
from ipss_utils.ipss_api_doc import create_record_response, update_record_response, list_response_model

# Initialize API routes


timesheet_api_route = Namespace('timesheet', path='/timesheet')

# List self API docs
timesheet_model = timesheet_api_route.model('timesheet_model', {
    **timesheet_fields,
    "emp_name": fields.String,
    "emp_company_id": fields.String,
    # 'deleted': fields.Boolean,
    # 'created_on': fields.String,
    # 'modified_on': fields.String
})
timesheet_get_model = timesheet_api_route.model('timesheet_get_model', {
    **timesheet_fields,
    "emp_name": fields.String,
    "emp_company_id": fields.String,
    # "task": fields.String,
    # "subtask": fields.String,
    # "category": fields.String,
    # 'deleted': fields.Boolean,
    # 'created_on': fields.String,
    # 'modified_on': fields.String
})
self_model = timesheet_api_route.model('self_model', {
    **self_fields,
    'project': fields.String,
    "task": fields.String,
    # "sub_task": fields.String,
    "category": fields.String,
    # 'page': fields.String
    # 'deleted': fields.Boolean,
    # 'created_on': fields.String,
    # 'modified_on': fields.String
})
self_get_model = timesheet_api_route.model('self_get_model', {
    **self_fields,
    'project': fields.String,
    "task": fields.String,
    # "sub_task": fields.String,
    "category": fields.String,
    # 'page': fields.String
    # 'deleted': fields.Boolean,
    # 'created_on': fields.String,
    # 'modified_on': fields.String
})

timesheet_list_response = timesheet_api_route.model('timesheet_list_response', {
    **list_response_model,
    **{
        'results': fields.List(fields.Nested(timesheet_model))
    }
})

timesheet_get = timesheet_api_route.model('timesheet_get', {

    **timesheet_model,
    'selfLists': fields.List(fields.Nested(self_model))

})
timesheet_get_all = timesheet_api_route.model('timesheet_get_all', {

    **timesheet_get_model,
    'selfLists': fields.List(fields.Nested(self_get_model))

})
timesheet_get_list = timesheet_api_route.model('timesheet_get_list', {

    **list_response_model,
    'results': fields.List(fields.Nested(timesheet_get_all))

})

# Create self model

create_timesheet_model = timesheet_api_route.model('create_timesheet_model', timesheet_fields)
create_timesheet_response = timesheet_api_route.model('create_timesheet_response', create_record_response)

# step1
create_self_model = timesheet_api_route.model('create_timesheet_model', self_fields)
# step2
create_ts_model = timesheet_api_route.model('create_ts_model', {
    **create_timesheet_model,
    'selfLists': fields.List(fields.Nested(create_self_model))
})

# Get self records model
get_timesheet_response = timesheet_api_route.model('get_timesheet_response', timesheet_fields)
get_timesheet_self_response = timesheet_api_route.model('get_timesheet_self_response', self_fields)

# Update user record
# step1
update_timesheet_fields = timesheet_fields
update_timesheet_model = timesheet_api_route.model('update_timesheet_model', update_timesheet_fields)
# step2
update_self_fields = self_fields
update_self_model = timesheet_api_route.model('update_self_model', update_self_fields)
update_ts_model = timesheet_api_route.model('update_ts_model', {
    **update_timesheet_model,
    'selfLists': fields.List(fields.Nested(update_self_model))
})
update_timesheet_response = timesheet_api_route.model('update_self_response', update_record_response)

sheet_fields = {'status': fields.String,
                'reason':fields.String
                }
update_sheet_model = timesheet_api_route.model('update_sheet_model', sheet_fields)
update_sheet_response = timesheet_api_route.model('update_sheet_response', update_record_response)
#############################################


# List task API docs
task_model = timesheet_api_route.model('task_model', {
    **task_fields,
    "emp_name": fields.String,
    "emp_company_id": fields.String,
    'project_name': fields.String,
    'task_name': fields.String,
    'category_name': fields.String,
    'page_name': fields.String,
    'deleted': fields.Boolean,
    'created_on': fields.String,
    'modified_on': fields.String
})

task_list_response = timesheet_api_route.model('task_list_response', {
    **list_response_model,
    **{
        'results': fields.List(fields.Nested(task_model))
    }
})

project_get_model = timesheet_api_route.model('project_get_model', project_fields)
project_get_response = timesheet_api_route.model('project_get_response', {
    'length': fields.Integer,
    'result': fields.List(fields.Nested(project_get_model))
})
