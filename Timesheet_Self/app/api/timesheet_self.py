import datetime

from flask import request, session
from flask_restx import Resource, abort
# from .. import ipss_db
from ipss_utils.ipss_api_doc import list_api_params, search_params
from ipss_utils.ipss_db import query_to_dict
from sqlalchemy import text, func, distinct, BigInteger
from sqlalchemy.exc import SQLAlchemyError

from ..api_doc import self_fields, search_filter, sheet_params, search_filters
from ..models.timesheet_self import Timesheet, TimesheetSelf,Notification
from ipss_utils.decorators import login_required

from ..routes.timesheet_self import timesheet_api_route, timesheet_list_response, create_timesheet_response, \
    update_timesheet_model, update_timesheet_response, create_ts_model, update_ts_model, create_self_model, \
    timesheet_get_list, timesheet_get, get_timesheet_self_response, update_sheet_model, update_sheet_response, \
    task_list_response, project_get_response
# from sqlalchemy import and_, text
from ..routes.timesheet_self import create_timesheet_model, get_timesheet_response
from .. import ipss_db, db_client

# Primary key name

primary_key = 'sheet_id'


@timesheet_api_route.route('/')
class SelfApi(Resource):
    per_page = 20

    @timesheet_api_route.marshal_with(timesheet_get_list)
    @timesheet_api_route.doc(params=list_api_params)
    @timesheet_api_route.doc(params=search_filter)
    @login_required(permissions="Timesheet_ID.list")
    def get(self):
        """
        List of timesheet_self with pagination
        TODO: Search
        :return:
        """
        current_user = request.args.get('current_user')
        compcode = current_user.get('company_id')
        print("compcode", compcode)
        start_date = request.args.get('start_date')
        print("start_date", start_date)
        end_date = request.args.get('end_date')
        print('end_date', end_date)
        emp_id = request.args.get('employee_id')
        print('emp_id', emp_id)
        manager = request.args.get('manager')
        print('manager', manager)
        # asd = ""
        filters = ""
        if emp_id or start_date or end_date or manager:
            if emp_id:
                filters += "and timesheet.emp_id =:emp_id "
            if start_date:
                filters += "and timesheet.from_date =:start_date "
            if end_date:
                filters += "and timesheet.to_date =:end_date "
            if manager == "YES":
                filters += "and timesheet.send is NOT false "

        paged = int(request.args.get('paged')) if request.args.get('paged') else 1
        results_per_page = int(request.args.get('results_per_page')) if request.args.get(
            'results_per_page') else self.per_page
        offset = (paged - 1) * results_per_page
        sorting = "order by timesheet.created_on desc limit :limit offset :offset"
        sql_query = text('select timesheet.*,emp.empid as emp_company_id,'
                         "CONCAT (emp.fname,' ',emp.lname) as emp_name,"
                         "(select  json_agg( "
                         "json_build_object("
                         "'self_id',timesheet_self.self_id,"
                         "'sheet_id',timesheet_self.sheet_id,"
                         "'emp_id',timesheet_self.emp_id,"
                         "'project_id',timesheet_self.project_id,"
                         "'project',project_mast.project_name,"
                         "'task_id',timesheet_self.task_id,"
                         "'task',main_activities.activity_name,"
                         "'category_id',timesheet_self.category_id,"
                         "'category',task_mast.task_name,"
                         # "'page_id',timesheet_self.page_id,"
                         # "'page',page_config.page_name,"
                         "'description',timesheet_self.description,"
                         "'mon',timesheet_self.mon,"
                         "'tue',timesheet_self.tue,"
                         "'wed',timesheet_self.wed,"
                         "'thu',timesheet_self.thu,"
                         "'fri',timesheet_self.fri,"
                         "'sat',timesheet_self.sat,"
                         "'sun',timesheet_self.sun,"
                         "'hrs_per_task',timesheet_self.hrs_per_task,"
                         "'compcode',timesheet_self.compcode,"
                         "'modified_by',timesheet_self.modified_by,"
                         "'modified_on',timesheet_self.modified_on,"
                         "'created_by',timesheet_self.created_by,"
                         "'created_on',timesheet_self.created_on,"
                         "'deleted',timesheet_self.deleted,"
                         "'deleted_at',timesheet_self.deleted_at"
                         ') ) as "selfLists" '
                         'from timesheet_self '
                         'JOIN project_mast ON '
                         'timesheet_self.project_id=project_mast.project_id '
                         "JOIN main_activities on timesheet_self.task_id = main_activities.activity_id "
                         'JOIN task_mast ON timesheet_self.category_id=task_mast.task_mast_id '
                         # "JOIN page_config on timesheet_self.page_id = page_config.page_id "
                         'where '
                         'timesheet_self.sheet_id=timesheet.sheet_id  '
                         ' AND timesheet_self.deleted is NOT True ) '
                         # 'as "selfLists" '
                         'FROM timesheet '
                         # 'LEFT JOIN timesheet_self ON timesheet.sheet_id=timesheet_self.sheet_id '
                         'JOIN hremploymast as emp ON timesheet.emp_id=emp.hremploymastid '
                         'WHERE timesheet.deleted is NOT True AND  '
                         'timesheet.compcode=:compcode '
                         f'{filters} '
                         'GROUP BY timesheet.sheet_id,emp_company_id,emp_name '
                         f'{sorting}')
        task_list = query_to_dict(db_client.engine.execute(sql_query,
                                                           start_date=start_date,
                                                           end_date=end_date,
                                                           compcode=compcode,
                                                           emp_id=emp_id,
                                                           limit=results_per_page,
                                                           offset=offset))
        print("task_list", task_list)
        # return task_list
        response = {
            'primary_key': primary_key,
            "total_results": len(task_list),
            "page": paged,
            "results_per_page": results_per_page,
            'results': task_list
        }
        print(response)
        return response

    @login_required(permissions="Timesheet_ID.add")
    @timesheet_api_route.expect(create_ts_model)
    # @timesheet_api_route.marshal_with(create_timesheet_response)
    def post(self):
        """
        Create timesheet_self record and return inserted id
        :return:
        """
        current_user = request.args.get('current_user')
        compcode = current_user.get('company_id')
        user_name = current_user.get('username')
        data = request.json
        print("Whole Data", data)
        # remove primary key if exists
        data.pop(primary_key, None)
        emp_id = data.get("emp_id")
        selfLists = data.pop('selfLists', None)
        print("Timesheet table data", data)
        timesheet_result = ipss_db.insert_record(
            model=Timesheet,
            values=data
        )
        print('Timesheet Results', timesheet_result)
        success = True
        if timesheet_result.get('success'):
            sheetId = timesheet_result.get('primary_key_id')
            print('sheetId', sheetId)
            if len(selfLists):
                for selfList in selfLists:
                    selfList['sheet_id'] = sheetId[0]
                    selfList.pop('self_id', None)
                    selfList['emp_id'] = emp_id
                    selfList['compcode'] = compcode
                    selfList['created_by'] = user_name
                    selfList['created_on'] = datetime.datetime.now()
                    selfList['modified_by'] = user_name
                    selfList["modified_on"] = datetime.datetime.now()
                    # Write bulk insert code here USE PROPER TRY CATCH
                error = ""
                s = db_client.session
                try:
                    result = s.bulk_insert_mappings(TimesheetSelf, selfLists)
                    # a = s.commit()
                except SQLAlchemyError as e:
                    error = str(e)
                    # db_client.session.flush()
                    print("error", error)
                success = False if error else True
            if success:
                message = "Record created Successfully"
            else:
                message = "There is an Error"
            db_client.session.commit()
            return {
                'success': success,
                'message': message,
                # 'error': error,
                'inserted_id': sheetId[0],
                'primary_key': primary_key
            }
        else:
            db_client.session.flush()
            abort(success=False, error=timesheet_result.get('error'))


@timesheet_api_route.route('/<sheet_id>/')
class SelfUpdateApi(Resource):
    @timesheet_api_route.marshal_with(timesheet_get)
    @login_required(permissions="Timesheet_ID.view")
    def get(self, sheet_id):
        """
        Read user record / single record for timesheet
        :param sheet_id:
        :return:
        """
        # query1 = Timesheet.query.filter_by(sheet_id=sheet_id).first()
        # print("test1", query1)
        # query2 = TimesheetSelf.query.filter_by(sheet_id=sheet_id).all()
        # print("test2", query2)
        #
        # details = query1.to_dict()
        #
        # return {
        #     **details,
        #     'selfLists': query2
        #
        # }
        current_user = request.args.get('current_user')
        compcode = current_user.get('company_id')
        print("compcode", compcode)
        sql_query = text('select timesheet.*,emp.empid as emp_company_id,'
                         "CONCAT (emp.fname,' ',emp.lname) as emp_name,"
                         "(select  json_agg( "
                         "json_build_object("
                         "'self_id',timesheet_self.self_id,"
                         "'sheet_id',timesheet_self.sheet_id,"
                         "'emp_id',timesheet_self.emp_id,"
                         "'project_id',timesheet_self.project_id,"
                         "'project',project_mast.project_name,"
                         "'task_id',timesheet_self.task_id,"
                         "'task',main_activities.activity_name,"
                         "'category_id',timesheet_self.category_id,"
                         "'category',task_mast.task_name,"
                         # "'page_id',timesheet_self.page_id,"
                         # "'page',page_config.page_name,"
                         "'description',timesheet_self.description,"
                         "'mon',timesheet_self.mon,"
                         "'tue',timesheet_self.tue,"
                         "'wed',timesheet_self.wed,"
                         "'thu',timesheet_self.thu,"
                         "'fri',timesheet_self.fri,"
                         "'sat',timesheet_self.sat,"
                         "'sun',timesheet_self.sun,"
                         "'hrs_per_task',timesheet_self.hrs_per_task,"
                         "'compcode',timesheet_self.compcode,"
                         "'modified_by',timesheet_self.modified_by,"
                         "'modified_on',timesheet_self.modified_on,"
                         "'created_by',timesheet_self.created_by,"
                         "'created_on',timesheet_self.created_on,"
                         "'deleted',timesheet_self.deleted,"
                         "'deleted_at',timesheet_self.deleted_at"
                         ') ) as "selfLists" '
                         'from timesheet_self '
                         'JOIN project_mast ON '
                         'timesheet_self.project_id=project_mast.project_id '
                         "JOIN main_activities on timesheet_self.task_id = main_activities.activity_id "
                         'JOIN task_mast ON timesheet_self.category_id=task_mast.task_mast_id '
                         # "JOIN page_config on timesheet_self.page_id = page_config.page_id "
                         'where '
                         'timesheet_self.sheet_id=timesheet.sheet_id  '
                         ' AND timesheet_self.deleted is NOT True ) '
                         # 'as "selfLists" '
                         'FROM timesheet '
                         # 'LEFT JOIN timesheet_self ON timesheet.sheet_id=timesheet_self.sheet_id '
                         'JOIN hremploymast as emp ON timesheet.emp_id=emp.hremploymastid '
                         'WHERE timesheet.deleted is NOT True AND  '
                         'timesheet.compcode=:compcode '
                         'and timesheet.sheet_id=:sheet_id '
                         'GROUP BY timesheet.sheet_id,emp_company_id,emp_name ')
        task_list = query_to_dict(db_client.engine.execute(sql_query,
                                                           compcode=compcode,
                                                           sheet_id=sheet_id
                                                           ))
        print("task_list", task_list)
        return {} if len(task_list) == 0 else task_list[0]

    @timesheet_api_route.expect(update_ts_model)
    # @timesheet_api_route.marshal_with(update_timesheet_response)
    @login_required(permissions="Timesheet_ID.edit")
    def put(self, sheet_id):
        """
        Partial Update timesheet_self record
        :return:
        """
        current_user = request.args.get('current_user')
        compcode = current_user.get('company_id')
        user_name = current_user.get('username')
        data = request.json
        selfLists = data.pop('selfLists')
        data.pop(primary_key, None)
        emp_id = data.get("emp_id")
        result = ipss_db.update_record(
            model=Timesheet,
            condition=Timesheet.sheet_id == sheet_id,
            values=data
        )
        print(result)
        if result.get('success'):
            delt = text('delete from timesheet_self where "sheet_id"=:id')
            delt1 = db_client.engine.execute(delt, id=sheet_id)
            for selfList in selfLists:
                selfList['sheet_id'] = sheet_id
                selfList.pop('self_id', None)
                selfList['emp_id'] = emp_id
                selfList['created_by'] = user_name
                selfList['compcode'] = compcode
                selfList['modified_by'] = user_name
                selfList["modified_on"] = datetime.datetime.now()
                selfList['created_on'] = datetime.datetime.now()

            error = ""
            s = db_client.session
            try:
                result = s.bulk_insert_mappings(TimesheetSelf, selfLists)
                # a = s.commit()
            except SQLAlchemyError as e:
                error = str(e)
                # db_client.session.flush()
                print("error", error)
            success = False if error else True
            if success:
                message = "Records Updated Successfully"
            else:
                message = "There is an Error"
            db_client.session.commit()
            return {
                'success': success,
                'message': message,
                'error': error,
            }
        else:
            db_client.session.flush()
            abort(str="Something went wrong, try again.")
        return result

    @timesheet_api_route.marshal_with(update_timesheet_response)
    @login_required(permissions="Timesheet_ID.delete")
    def delete(self, sheet_id):
        """
        Soft delete timesheet_self record
        TODO: Make soft delete
        :return:
        """

        result = ipss_db.update_record(
            model=Timesheet,
            condition=Timesheet.sheet_id == sheet_id,

            values={
                'deleted': True,
                'deleted_at': datetime.datetime.now()
            }
        )

        return result

    @timesheet_api_route.marshal_with(update_timesheet_response)
    @login_required(permissions="Timesheet_ID.submit")
    def post(self, sheet_id):
        """
        Submit Timesheet  to Manager
        TODO: Submit to Manager
        :return:
        """
        get_data = SelfUpdateApi.get(self, sheet_id)
        status = get_data.get('status')
        emp_id = get_data.get('emp_id')
        from_date =get_data.get('from_date')
        to_date =get_data.get('to_date')
        current_user = request.args.get('current_user')
        compcode = current_user.get('company_id')
        print('status', status,emp_id)
        data = {
            'send': True,
            'status': 'pending',
            'sent_at': datetime.datetime.now()
        } if status == 'canceled' else {
            'send': True,
            'sent_at': datetime.datetime.now()
        }
        print('data', data)
        result = ipss_db.update_record(
            model=Timesheet,
            condition=Timesheet.sheet_id == sheet_id,
            values=data
        )

        if result.get('success'):
            query = text("SELECT CONCAT(fname,' ',lname) as name, idcardno "
                         " FROM hremploymast WHERE hremploymastid=:emp_id and deleted is not true "
                         "and compcode =:compcode ")
            result_list = query_to_dict(db_client.engine.execute(query,
                                                                 emp_id=emp_id,
                                                                 compcode=compcode))
            emp_name = result_list[0].get('name')
            idcard = result_list[0].get('idcardno')
            sub_query = text('select team_assign.manager_id '
                             # "concat(fname,' ',lname)as name,emp.email "
                             'from team_assign '
                             'join team_members on '
                             'team_members.team_assign_id = team_assign.team_assign_id '
                             'join hremploymast as emp on emp.hremploymastid=team_assign.manager_id '
                             'where team_assign.deleted is not true and team_members.employee_id =:employee_id '
                             'and team_assign.compcode=:compcode '
                             'and emp.deleted is not true ')

            sub_query_list = query_to_dict(db_client.engine.execute(sub_query,
                                                                    employee_id=emp_id,
                                                                    compcode=compcode
                                                                    ))

            action = 'resubmitted' if status == 'canceled' else 'submitted'
            date_obj_1 = datetime.datetime.strptime(from_date, '%Y-%m-%d')
            from_date_obj = date_obj_1.strftime('%d-%m-%Y')
            date_obj_2 = datetime.datetime.strptime(to_date, '%Y-%m-%d')
            to_date_obj = date_obj_2.strftime('%d-%m-%Y')
            manager_id = sub_query_list[0].get('manager_id')
            notification_data= {
                    'user_id': manager_id,
                    'type': 'Timesheet',
                    'action': f'{emp_name}-{idcard} successfully {action} the timesheet for the {from_date_obj} to {to_date_obj}.'
                }
            print('notification_data',notification_data)
            ipss_db.insert_record(
                model=Notification,
                values=notification_data
            )
        return result


@timesheet_api_route.route('/update/<self_id>/')
class UpdateApi2(Resource):
    @staticmethod
    def update_record(data, self_id):
        data.pop('self_id', None)

        result = ipss_db.update_record(
            model=TimesheetSelf,
            condition=TimesheetSelf.self_id == self_id,
            values=data
        )

        return result

    # @timesheet_api_route.expect(create_self_model)
    # @timesheet_api_route.marshal_with(update_timesheet_response)
    # @login_required()
    # def patch(self, self_id):
    #     """
    #     Soft delete self record
    #     TODO: Make soft delete
    #     :return:
    #     """
    #     data = request.json
    #     result = ipss_db.update_record(
    #         model=TimesheetSelf,
    #         condition=TimesheetSelf.self_id == self_id,
    #         values=data
    #     )
    #     return result

    @timesheet_api_route.marshal_with(get_timesheet_self_response)
    @login_required(permissions="Timesheet_ID.view")
    def get(self, self_id):
        """
        Read user record / single record for task
        :param self_id:
        :return:
        """
        query = TimesheetSelf.query.filter_by(self_id=self_id).first()
        return query

    @timesheet_api_route.marshal_with(update_timesheet_response)
    @timesheet_api_route.doc(params=sheet_params)
    @login_required(permissions="Timesheet_ID.delete")
    def delete(self, self_id):
        """
        Soft delete task record
        TODO: Make soft delete
        :return:
        """

        result = ipss_db.update_record(
            model=TimesheetSelf,
            condition=TimesheetSelf.self_id == self_id,

            values={
                'deleted': True,
                'deleted_at': datetime.datetime.now()
            }
        )
        response = result.get('success')
        sheet_id = request.args.get('sheet_id')
        hrs = request.args.get('hours')

        if response:
            sql_query = text('update timesheet set total_hrs=total_hrs-:hrs  where timesheet.sheet_id=:sheet_id')
            task_list = (db_client.engine.execute(sql_query, sheet_id=sheet_id, hrs=float(hrs)))
            print("update_list", task_list)
        return result


@timesheet_api_route.route('/approve/<sheet_id>/')
class ManagerApproveApi(Resource):
    @staticmethod
    def update_record(data, sheet_id):
        data.pop('sheet_id', None)

        result = ipss_db.update_record(
            model=Timesheet,
            condition=Timesheet.sheet_id == sheet_id,
            values=data
        )

        return result

    @timesheet_api_route.expect(update_sheet_model)
    @timesheet_api_route.marshal_with(update_sheet_response)
    @login_required(permissions="Timesheet_Reportees_ID.approve")
    def patch(self, sheet_id):
        """
        Manager Approval
        TODO: Make soft delete
        :return:
        """
        # current_user = request.args.get('current_user')
        # compcode = current_user.get('company_id')
        # manager_id = current_user.get('emp_id')
        get_data = SelfUpdateApi.get(self, sheet_id)
        emp_id = get_data.get('emp_id')
        from_date = get_data.get('from_date')
        to_date = get_data.get('to_date')
        data = request.json
        status = data.get('status')
        reason = 'Reason-'+"'"+data.get('reason')+"'."if data.get('reason') else ''
        patch_data = {'status': status.lower(),
                      'status_at': datetime.datetime.now(),
                      'send': False} if status.lower() == 'canceled' else {'status': status.lower(),
                                                                           'status_at': datetime.datetime.now()}
        print('patch_data', patch_data)
        result = ipss_db.update_record(
            model=Timesheet,
            condition=Timesheet.sheet_id == sheet_id,
            values=patch_data
        )
        if result.get('success') and status:
            action = 'rejected' if status.lower() == 'canceled' else 'approved'
            date_obj_1 = datetime.datetime.strptime(from_date, '%Y-%m-%d')
            from_date_obj = date_obj_1.strftime('%d-%m-%Y')
            date_obj_2 = datetime.datetime.strptime(to_date, '%Y-%m-%d')
            to_date_obj = date_obj_2.strftime('%d-%m-%Y')

            notification_data = {
                'user_id': emp_id,
                'type': 'Timesheet',
                'action': f'Your timesheet for the {from_date_obj} to {to_date_obj} period has been {action}.{reason}'
            }
            print('notification_data', notification_data,reason)
            ipss_db.insert_record(
                model=Notification,
                values=notification_data
            )


        return result


@timesheet_api_route.route('/reportees')
class ReporteesApi(Resource):
    per_page = 20

    @timesheet_api_route.marshal_with(timesheet_get_list)
    @timesheet_api_route.doc(params=list_api_params)
    @timesheet_api_route.doc(params=search_filter)
    @login_required(permissions="Timesheet_Reportees_ID.reportees")
    def get(self):
        """
        List of reportees with pagination
        TODO: Search
        :return:
        """
        current_user = request.args.get('current_user')
        compcode = current_user.get('company_id')
        print("compcode", compcode)
        start_date = request.args.get('start_date')
        print("start_date", start_date)
        end_date = request.args.get('end_date')
        print('end_date', end_date)
        emp_id = request.args.get('employee_id')
        print('emp_id', emp_id)
        manager = request.args.get('manager')
        print('manager', manager)
        # asd = ""
        filters = ""
        if emp_id or start_date or end_date or manager:
            if emp_id:
                filters += "and timesheet.emp_id =:emp_id "
            if start_date:
                filters += "and timesheet.from_date =:start_date "
            if end_date:
                filters += "and timesheet.to_date =:end_date "
            if manager == "YES":
                filters += "and timesheet.send is NOT false "

        paged = int(request.args.get('paged')) if request.args.get('paged') else 1
        results_per_page = int(request.args.get('results_per_page')) if request.args.get(
            'results_per_page') else self.per_page
        offset = (paged - 1) * results_per_page
        sorting = "order by timesheet.created_on desc limit :limit offset :offset"
        sql_query = text('select timesheet.*,emp.empid as emp_company_id,'
                         "CONCAT (emp.fname,' ',emp.lname) as emp_name,"
                         "(select  json_agg( "
                         "json_build_object("
                         "'self_id',timesheet_self.self_id,"
                         "'sheet_id',timesheet_self.sheet_id,"
                         "'emp_id',timesheet_self.emp_id,"
                         "'project_id',timesheet_self.project_id,"
                         "'project',project_mast.project_name,"
                         "'task_id',timesheet_self.task_id,"
                         "'task',main_activities.activity_name,"
                         "'category_id',timesheet_self.category_id,"
                         "'category',task_mast.task_name,"
                         # "'page_id',timesheet_self.page_id,"
                         # "'page',page_config.page_name,"
                         "'description',timesheet_self.description,"
                         "'mon',timesheet_self.mon,"
                         "'tue',timesheet_self.tue,"
                         "'wed',timesheet_self.wed,"
                         "'thu',timesheet_self.thu,"
                         "'fri',timesheet_self.fri,"
                         "'sat',timesheet_self.sat,"
                         "'sun',timesheet_self.sun,"
                         "'hrs_per_task',timesheet_self.hrs_per_task,"
                         "'compcode',timesheet_self.compcode,"
                         "'modified_by',timesheet_self.modified_by,"
                         "'modified_on',timesheet_self.modified_on,"
                         "'created_by',timesheet_self.created_by,"
                         "'created_on',timesheet_self.created_on,"
                         "'deleted',timesheet_self.deleted,"
                         "'deleted_at',timesheet_self.deleted_at"
                         ') ) as "selfLists" '
                         'from timesheet_self '
                         'JOIN project_mast ON '
                         'timesheet_self.project_id=project_mast.project_id '
                         "JOIN main_activities on timesheet_self.task_id = main_activities.activity_id "
                         'JOIN task_mast ON timesheet_self.category_id=task_mast.task_mast_id '
                         # "JOIN page_config on timesheet_self.page_id = page_config.page_id "
                         'where '
                         'timesheet_self.sheet_id=timesheet.sheet_id  '
                         ' AND timesheet_self.deleted is NOT True ) '
                         # 'as "selfLists" '
                         'FROM timesheet '
                         # 'LEFT JOIN timesheet_self ON timesheet.sheet_id=timesheet_self.sheet_id '
                         'JOIN hremploymast as emp ON timesheet.emp_id=emp.hremploymastid '
                         'WHERE timesheet.deleted is NOT True AND  '
                         'timesheet.compcode=:compcode '
                         f'{filters} '
                         'GROUP BY timesheet.sheet_id,emp_company_id,emp_name '
                         f'{sorting}')
        task_list = query_to_dict(db_client.engine.execute(sql_query,
                                                           start_date=start_date,
                                                           end_date=end_date,
                                                           compcode=compcode,
                                                           emp_id=emp_id,
                                                           limit=results_per_page,
                                                           offset=offset))
        print("task_list", task_list)
        # return task_list
        response = {
            'primary_key': primary_key,
            "total_results": len(task_list),
            "page": paged,
            "results_per_page": results_per_page,
            'results': task_list
        }
        print(response)
        return response


######################################################################


# @timesheet_api_route.route('/assign_task')
# class AssignTaskApi(Resource):
#     per_page = 20
#
#     @timesheet_api_route.marshal_with(task_list_response)
#     @timesheet_api_route.doc(params=list_api_params)
#     @timesheet_api_route.doc(params=search_filters)
#     @login_required()
#     def get(self):
#         """
#         List of AssignTask with pagination
#         TODO: Search
#         :return:
#         """
#         current_user = request.args.get('current_user')
#         compcode = current_user.get("company_id")
#         # manager_id = current_user.get('emp_id')
#         # print('manager_id', manager_id)
#         manager_id = request.args.get('manager_id')
#         print('manager_id', manager_id)
#         start_date = request.args.get('start_date')
#         print("start_date", start_date)
#         end_date = request.args.get('end_date')
#         print('end_date', end_date)
#         emp_id = request.args.get('employee_id')
#         print('emp_id', emp_id)
#         filters = ""
#         if emp_id or start_date or end_date or manager_id:
#             if emp_id:
#                 filters += "assign_task.emp_id =:emp_id and "
#             if manager_id:
#                 filters += "assign_task.manager_id =:manager_id and "
#             if start_date and end_date is None:
#                 filters += "assign_task.from_date =:start_date and "
#             if start_date is None and end_date:
#                 filters += "assign_task.to_date =:end_date and "
#             if start_date and end_date:
#                 filters += "assign_task.from_date >=:start_date and assign_task.to_date <=:end_date and "
#
#         paged = int(request.args.get('paged')) if request.args.get('paged') else 1
#         results_per_page = int(request.args.get('results_per_page')) if request.args.get(
#             'results_per_page') else self.per_page
#         offset = (paged - 1) * results_per_page
#         sorting = "order by assign_task.created_on desc limit :limit offset :offset"
#         query = text(
#             "select assign_task.*,emp.empid as emp_company_id,"
#             # "cast(assign_task.from_date as DATE) as from_date,cast(assign_task.to_date as DATE) as to_date,"
#             "CONCAT (emp.fname,' ',emp.lname) as emp_name,"
#             "project_mast.project_name as project_name,task_mast.task_name as task_name,"
#             "category_config.category_name as category_name,page_config.page_name as page_name"
#             " from assign_task "
#             "JOIN hremploymast as emp ON assign_task.emp_id=emp.hremploymastid "
#             "JOIN project_mast on assign_task.project_id = project_mast.project_id "
#             "JOIN task_mast on assign_task.task_mast_id = task_mast.task_mast_id "
#             "JOIN category_config on assign_task.category_mast_id = category_config.category_mast_id "
#             "JOIN page_config on assign_task.page_id = page_config.page_id "
#             "WHERE assign_task.deleted is not true and "
#             f"{filters} assign_task.compcode =:cc "
#             f"{sorting}")
#         task_list = query_to_dict(db_client.engine.execute(query, start_date=start_date,
#                                                            end_date=end_date,
#                                                            cc=compcode,
#                                                            manager_id=manager_id,
#                                                            emp_id=emp_id,
#                                                            limit=results_per_page,
#                                                            offset=offset))
#         print("task_list", task_list)
#
#         return {
#             'primary_key': 'task_id',
#             "total_results": len(task_list),
#             "page": paged,
#             "results_per_page": results_per_page,
#             'results': task_list
#         }


@timesheet_api_route.route('/activity_dropdown')
class ActivityApi(Resource):
    @timesheet_api_route.marshal_with(project_get_response)
    @login_required()
    def get(self):
        current_user = request.args.get('current_user')
        compcode = current_user.get("company_id")
        emp_id = current_user.get('emp_id')
        query = text('select project_id from assign_task where deleted is not true and emp_id =:emp_id and '
                     'compcode=:compcode ')
        query_list = query_to_dict(db_client.engine.execute(query,
                                                            emp_id=emp_id,
                                                            compcode=compcode))
        if len(query_list):
            # project_id = []
            # for res in query_list:
            #     project_id.append(res.get('project_id'))
            project_id = list(map(lambda project: project.get('project_id'), query_list))
            print('project_id', project_id)
            sub_query = text('select * from project_mast where deleted is not true and project_id in :project_id '
                             'and compcode=:compcode ')
            sub_query_list = query_to_dict(db_client.engine.execute(sub_query,
                                                                    project_id=tuple(project_id),
                                                                    compcode=compcode
                                                                    ))
            print('sub_query_list', sub_query_list)
            print(datetime.datetime.today().date())
            today_date = datetime.datetime.today().date()
            # result = []
            # for i in sub_query_list:
            #     if i.get('from_date') <= today_date <= i.get('to_date'):
            #         activity = text(
            #             'select * from main_activities where deleted is not true and project_id =:project_id ')
            #         activity_list = query_to_dict(db_client.engine.execute(activity,
            #                                                                project_id=i.get('project_id')
            #                                                                ))
            #         print(activity_list)
            #         result = result + activity_list
            result = (
                list(filter(lambda data: data.get('from_date') <= today_date <= data.get('to_date'), sub_query_list)))
            print("result", result)
            return {
                'length': len(result),
                'result': result
            }
        return {
            'length': len(query_list),
            'result': query_list
        }
