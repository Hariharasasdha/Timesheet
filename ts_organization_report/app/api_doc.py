from flask_restx import fields

# Employee register report

search_params = {
    'from_date': {
        'type': 'str',
        'description': "from_date"
    },
    'to_date': {
        'type': 'str',
        'description': "to_date"
    },
    'status': {
        'type': 'str',
        'description': "status"
    }
}

report_fields = {
    "emp_mast_id": fields.Integer,
    "emp_name": fields.String,
    "emp_id": fields.String,
    'from_date': fields.String,
    'to_date': fields.String,
    'status': fields.String

}
timesheet_fields ={
    "emp_mast_id": fields.Integer,
    "emp_name": fields.String,
    "idcard": fields.String,
    'from_date': fields.String,
    'to_date': fields.String,
    'deptname': fields.String,
    'designation': fields.String,
    'sheet_id': fields.String,
    'time_sheet_details':fields.Raw
}

filter_params=  {
    'from_date': {
        'type': 'str',
        'description': "from_date"
    },
    'to_date': {
        'type': 'str',
        'description': "to_date"
    }}

