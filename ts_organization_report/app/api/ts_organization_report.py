from flask import request
from flask_restx import Resource
from ipss_utils.decorators import login_required
from ipss_utils.ipss_api_doc import list_api_params
from ipss_utils.ipss_db import query_to_dict
from sqlalchemy import and_, text
from .. import ipss_db, db_client
from ..api_doc import search_params,filter_params
from ..routes.ts_organization_report import ts_report_api_route, timesheet_report_response, daily_report_response


@ts_report_api_route.route('/organization')
class TimesheetReportApi(Resource):
    @ts_report_api_route.marshal_with(timesheet_report_response)
    @ts_report_api_route.doc(params=search_params)
    @login_required(permissions='ts_organization_report_id.view')
    # @login_required()
    def get(self):
        current_user = request.args.get('current_user')
        compcode = current_user.get('company_id')
        status = request.args.get('status').lower() if request.args.get('status') else None
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        filters = ''
        if from_date and to_date:
            filters += f"and timesheet.from_date =:from_date  and timesheet.to_date =:to_date "
        if status == 'approved':
            filters += f"and timesheet.send IS true and timesheet.status = 'approved' "
        if status == 'rejected':
            filters += f"and timesheet.send IS false and timesheet.status = 'canceled' "
        if status == 'pending':
            filters += f"and timesheet.send IS true and timesheet.status = 'pending' "
        if status == 'not send':
            filters += "and timesheet.send IS false and timesheet.status = 'pending' "
        query = text('select timesheet.emp_id as emp_mast_id,'
                     "concat(hremploymast.fname,' ',hremploymast.lname) as emp_name,hremploymast.idcardno as emp_id, "
                     'timesheet.from_date as from_date ,timesheet.to_date as to_date, '
                     'INITCAP(timesheet.status) as status '
                     'from timesheet join hremploymast '
                     'on timesheet.emp_id = hremploymast.hremploymastid '
                     'where timesheet.deleted is not true and timesheet.compcode=:compcode  '
                     f'{filters}'
                     'order by timesheet.from_date desc '
                     )

        result = query_to_dict(db_client.engine.execute(
            query,
            from_date=from_date,
            to_date=to_date,
            compcode=compcode
        ))
        if (from_date is None or from_date) and (to_date is None or to_date) and status is None:
            sub_query = text('select timesheet.emp_id as emp_mast_id,'
                             "concat(hremploymast.fname,' ',hremploymast.lname) as emp_name,hremploymast.idcardno as "
                             "emp_id, "
                             'timesheet.from_date as from_date ,timesheet.to_date as to_date, '
                             'INITCAP(timesheet.status) as status '
                             'from timesheet join hremploymast '
                             'on timesheet.emp_id = hremploymast.hremploymastid '
                             'where timesheet.deleted is not true and timesheet.compcode=:compcode  '
                             "and timesheet.send IS false and timesheet.status = 'pending' "
                             # f'{filters}'
                             'order by timesheet.from_date desc '
                             )
            query_list = query_to_dict(db_client.engine.execute(
                sub_query,
                compcode=compcode
            ))
            for i in result:
                if i.get('status') == 'Canceled':
                    i['status'] = 'Rejected'
                for j in query_list:
                    if i.get('from_date') == j.get('from_date') and i.get('to_date') == j.get('to_date') and i.get(
                            'emp_id') == j.get('emp_id') and i.get('status') == j.get('status'):
                        i['status'] = 'Not Send'
        print(result)
        if status == 'rejected':
            for res in result:
                res['status'] = 'Rejected'
        if status == 'not send':
            for res in result:
                res['status'] = 'Not Send'
        return {
            'length': len(result),
            'result': result
        }
@ts_report_api_route.route('/daily_report')
class DailyReportApi(Resource):
    @ts_report_api_route.marshal_with(daily_report_response)
    @ts_report_api_route.doc(params=filter_params)
    @login_required(permissions='ts_daily_report_id.view')
    @login_required()
    def get(self):
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        query=text("SELECT emp_mast.hremploymastid as emp_mast_id,"
                "concat(emp_mast.fname, ' ', emp_mast.lname) as emp_name,"
                "dept.dept_name as deptname,"
               "desg.desg_name as designation,"
               "emp_mast.idcardno as idcard,"
               "timesheet.from_date as from_date,"
               "timesheet.to_date as to_date,"
               "timesheet.sheet_id,"
                "(SELECT json_build_object('mon', COALESCE(sum(ts.mon), 0.00), 'tue', COALESCE(sum(ts.tue), 0.00),"
                "'wed', COALESCE(sum(ts.wed), 0.00), 'thu', COALESCE(sum(ts.thu), 0.00),"
                "'fri', COALESCE(sum(ts.fri), 0.00), 'sat', COALESCE(sum(ts.sat), 0.00),"
                "'sun', COALESCE(sum(ts.sun), 0.00)) "
                "FROM timesheet_self as ts WHERE "
                "ts.sheet_id = timesheet.sheet_id and ts.deleted is not true) AS time_sheet_details "
               "FROM hremploymast as emp_mast JOIN  hremploydetails as emp_det ON "
                "emp_det.hremploymastid = emp_mast.hremploymastid "
                "JOIN department_mast as dept ON emp_det.deptname = dept.deptmastid "
                "JOIN designation_mast as desg ON emp_det.designation = desg.desgmastid "
                "LEFT JOIN timesheet ON timesheet.emp_id = emp_mast.hremploymastid AND timesheet.from_date =:from_date "
                "AND timesheet.to_date =:to_date WHERE "
                "emp_det.idactive = 'YES' and timesheet.deleted is not true  ")

        result = query_to_dict(db_client.engine.execute(
            query,
            from_date=from_date,
            to_date=to_date,
        ))
        return {
            'length': len(result),
            'result': result
        }