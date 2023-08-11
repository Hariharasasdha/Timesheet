from flask_restx import Namespace, Resource, fields
from ..api_doc import report_fields,timesheet_fields

# Initialize API routes
ts_report_api_route = Namespace('ts_organization_report', path='/ts_organization_report')

ts_report_model = ts_report_api_route.model('ts_report_model', report_fields)
timesheet_report_response = ts_report_api_route.model('timesheet_report_response', {
    'length': fields.Integer,
    'result': fields.List(fields.Nested(ts_report_model))
})
daily_report_model = ts_report_api_route.model('daily_report_model', timesheet_fields)
daily_report_response = ts_report_api_route.model('daily_report_response', {
    'length': fields.Integer,
    'result': fields.List(fields.Nested(daily_report_model))
})


