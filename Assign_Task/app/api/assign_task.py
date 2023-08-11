import datetime

from flask import request, session
from flask_restx import Resource
# from .. import ipss_db
from ipss_utils.ipss_api_doc import list_api_params, search_params
from ipss_utils.ipss_db import query_to_dict
from sqlalchemy import text, func, distinct, BigInteger
from sqlalchemy.exc import SQLAlchemyError

from ..api_doc import search_filter
from ..models.assign_task import AssignTask
from ipss_utils.decorators import login_required

from ..routes.assign_task import task_api_route, task_list_response, create_task_response, \
    update_task_model, update_task_response, bulk_post_response
# from sqlalchemy import and_, text
from ..routes.assign_task import create_task_model, get_task_response
from .. import ipss_db, db_client

# Primary key name

primary_key = 'task_id'


@task_api_route.route('/')
class AssignTaskApi(Resource):
    per_page = 20

    @task_api_route.marshal_with(task_list_response)
    @task_api_route.doc(params=list_api_params)
    @task_api_route.doc(params=search_filter)
    @login_required(permissions='Assign_Task_ID.list')
    def get(self):
        """
        List of AssignTask with pagination
        TODO: Search
        :return:
        """
        current_user = request.args.get('current_user')
        compcode = current_user.get("company_id")
        # manager_id = current_user.get('emp_id')
        # print('manager_id', manager_id)
        manager_id = request.args.get('manager_id')
        print('manager_id', manager_id)
        start_date = request.args.get('start_date')
        print("start_date", start_date)
        end_date = request.args.get('end_date')
        print('end_date', end_date)
        emp_id = request.args.get('employee_id')
        print('emp_id', emp_id)
        filters = ""
        if emp_id or start_date or end_date or manager_id:
            if emp_id:
                filters += "assign_task.emp_id =:emp_id and "
            if manager_id:
                filters += "assign_task.manager_id =:manager_id and "
            if start_date and end_date is None:
                filters += "assign_task.from_date =:start_date and "
            if start_date is None and end_date:
                filters += "assign_task.to_date =:end_date and "
            if start_date and end_date:
                filters += "assign_task.from_date >=:start_date and assign_task.to_date <=:end_date and "

        paged = int(request.args.get('paged')) if request.args.get('paged') else 1
        results_per_page = int(request.args.get('results_per_page')) if request.args.get(
            'results_per_page') else self.per_page
        offset = (paged - 1) * results_per_page
        sorting = "order by assign_task.created_on desc limit :limit offset :offset"
        query = text(
            "select assign_task.*,emp.empid as emp_company_id,"
            # "cast(assign_task.from_date as DATE) as from_date,cast(assign_task.to_date as DATE) as to_date,"
            "CONCAT (emp.fname,' ',emp.lname) as emp_name,"
            "project_mast.project_name as project_name "
            # "task_mast.task_name as task_name,"
            # "category_config.category_name as category_name,page_config.page_name as page_name"
            " from assign_task "
            "JOIN hremploymast as emp ON assign_task.emp_id=emp.hremploymastid "
            "JOIN project_mast on assign_task.project_id = project_mast.project_id "
            # "JOIN task_mast on assign_task.task_mast_id = task_mast.task_mast_id "
            # "JOIN category_config on assign_task.category_mast_id = category_config.category_mast_id "
            # "JOIN page_config on assign_task.page_id = page_config.page_id "
            "WHERE assign_task.deleted is not true and "
            f"{filters} assign_task.compcode =:cc "
            f"{sorting}")
        task_list = query_to_dict(db_client.engine.execute(query, start_date=start_date,
                                                           end_date=end_date,
                                                           cc=compcode,
                                                           manager_id=manager_id,
                                                           emp_id=emp_id,
                                                           limit=results_per_page,
                                                           offset=offset))
        print("task_list", task_list)

        return {
            'primary_key': primary_key,
            "total_results": len(task_list),
            "page": paged,
            "results_per_page": results_per_page,
            'results': task_list
        }

    # @login_required(permissions='Assign_Task_ID.add')
    @login_required()
    @task_api_route.expect(bulk_post_response)
    # @task_api_route.marshal_with(create_task_response)
    def post(self):
        """
        Create AssignTask record and return inserted id
        :return:
        """
        data = request.json
        # # remove primary key if exists
        # current_user = request.args.get('current_user')
        # # manager_id = current_user.get('emp_id')
        # # print('manager_id', manager_id)
        # data.pop(primary_key, None)
        # # data['manager_id'] = manager_id
        # result = ipss_db.insert_record(
        #     model=AssignTask,
        #     values=data
        # )
        #
        # return ipss_db.created_response(
        #     result=result,
        #     message="Record has been created successfully",
        #     primary_key=primary_key
        # )
        post_data = data.get('data')
        current_user = request.args.get('current_user')
        for i in post_data:
            i['compcode'] = current_user.get("company_id")
            i['created_on'] = datetime.datetime.now()
            i['created_by'] = current_user.get('username')
            i['modified_on'] = datetime.datetime.now()
            i['modified_by'] = current_user.get('username')
        error = ""
        try:
            s = db_client.session
            result = s.bulk_insert_mappings(AssignTask, post_data)
            a = s.commit()

        except SQLAlchemyError as e:
            error = str(e)
            db_client.session.flush()
        success = False if error else True
        if success:
            message = "Records Created Successfully"
        else:
            message = "There is an Error"

        return {
            'success': success,
            'message': message,
            'error': error,
            'primary_key': primary_key
        }


@task_api_route.route('/<task_id>/')
class AssignTaskUpdateApi(Resource):
    @staticmethod
    def update_record(data, task_id):
        data.pop('task_id', None)

        result = ipss_db.update_record(
            model=AssignTask,
            condition=AssignTask.task_id == task_id,
            values=data
        )
        return result

    @task_api_route.marshal_with(get_task_response)
    @login_required(permissions='Assign_Task_ID.view')
    def get(self, task_id):
        """
        Read user record / single record
        :param task_id:
        :return:
        """

        user = AssignTask.query.filter_by(task_id=int(task_id)).first()
        return user

    @task_api_route.expect(update_task_model)
    @task_api_route.marshal_with(update_task_response)
    @login_required(permissions='Assign_Task_ID.edit')
    def put(self, task_id):
        """
        Update AssignTask record
        :return:
        """
        data = request.json
        response = self.update_record(data, task_id)
        return response

    @task_api_route.expect(update_task_model)
    @task_api_route.marshal_with(update_task_response)
    @login_required(permissions='Assign_Task_ID.edit')
    def patch(self, task_id):
        """
        Partial Update AssignTask record
        :return:
        """
        data = request.json
        response = self.update_record(data, task_id)
        return response

    @task_api_route.marshal_with(update_task_response)
    @login_required(permissions='Assign_Task_ID.delete')
    def delete(self, task_id):
        """
        Soft delete AssignTask record
        TODO: Make soft delete
        :return:
        """

        result = ipss_db.update_record(
            model=AssignTask,
            condition=AssignTask.task_id == task_id,

            values={
                'deleted': True,
                'deleted_at': datetime.datetime.now()
            }
        )
        return result

######################################################################
