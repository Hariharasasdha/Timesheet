from flask_restx import Namespace, Resource, fields
from ..api_doc import report_fields, project_report_fields

# Initialize API routes
timesheet_report_api_route = Namespace('ts_report', path='/ts_report')

timesheet_report_model = timesheet_report_api_route.model('timesheet_report_model', report_fields)
timesheet_report_response = timesheet_report_api_route.model('timesheet_report_response', {
    'length': fields.Integer,
    'total_hrs': fields.String,
    'result': fields.List(fields.Nested(timesheet_report_model))
})
project_report_model = timesheet_report_api_route.model('project_report_model', project_report_fields)
project_report_response = timesheet_report_api_route.model('project_report_response', {
    'length': fields.Integer,
    'results': fields.List(fields.Nested(project_report_model))
})
