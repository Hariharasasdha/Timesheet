import datetime

from flask import request, session
from flask_restx import Resource
# from .. import ipss_db
from ipss_utils.ipss_api_doc import list_api_params, search_params
from ipss_utils.ipss_db import query_to_dict
from sqlalchemy import text, func, distinct, BigInteger
from ..api_doc import task_fields, get_all_messages
from ..models.task import TaskMast
from ipss_utils.decorators import login_required

from ..routes.task import task_api_route, task_list_response, create_task_response, \
    update_task_model, update_task_response
# from sqlalchemy import and_, text
from ..routes.task import create_task_model, get_task_response
from .. import ipss_db, db_client

# Primary key name

primary_key = 'task_mast_id'


@task_api_route.route('/')
class TaskApi(Resource):
    per_page = 20

    @task_api_route.marshal_with(task_list_response)
    @task_api_route.doc(params=list_api_params)
    @login_required(permissions='Task_Config_ID.list')
    def get(self):
        """
        List of Task with pagination
        TODO: Search
        :return:
        """
        task_list = TaskMast.query.order_by(TaskMast.created_on.desc())
        response = ipss_db.paginated_results(
            model=TaskMast,
            query=task_list,
            primary_key=primary_key
        )
        return response

    @login_required(permissions='Task_Config_ID.add')
    @task_api_route.expect(create_task_model)
    @task_api_route.marshal_with(create_task_response)
    def post(self):
        """
        Create Task Master record and return inserted id
        :return:
        """
        data = request.json
        # remove primary key if exists
        data.pop(primary_key, None)
        current_user = request.args.get('current_user')
        compcode = current_user.get('company_id')
        task_name = data.get('task_name')
        query = text("select * from task_mast where lower(task_name) =:task_name and compcode =:compcode "
                     "and deleted is not true "
                     "LIMIT 1")
        query_list = query_to_dict(db_client.engine.execute(
            query,
            task_name=task_name.lower(),
            compcode=compcode
        ))
        if len(query_list):
            return {
                       'success': False,
                       'message': "This task name is already exists",
                   }, 409

        result = ipss_db.insert_record(
            model=TaskMast,
            values=data
        )

        return ipss_db.created_response(
            result=result,
            message="Record has been created successfully",
            primary_key=primary_key
        )


@task_api_route.route('/<task_mast_id>/')
class TaskUpdateApi(Resource):
    @staticmethod
    def update_record(data, task_mast_id):
        data.pop('task_mast_id', None)
        # task_name = data.get('task_name')
        # current_user = request.args.get('current_user')
        # compcode = current_user.get('company_id')
        # query = text("select * from task_mast where lower(task_name) =:task_name and deleted is not true "
        #              "and compcode =:compcode "
        #              "LIMIT 1")
        # query_list = query_to_dict(db_client.engine.execute(
        #     query,
        #     task_name=task_name.lower(),
        #     compcode=compcode
        # ))
        # if len(query_list):
        #     return {
        #                'success': False,
        #                'message': "This task name is already exists",
        #            }, 409

        result = ipss_db.update_record(
            model=TaskMast,
            condition=TaskMast.task_mast_id == task_mast_id,
            values=data
        )
        return result

    @task_api_route.marshal_with(get_task_response)
    @login_required(permissions='Task_Config_ID.view')
    def get(self, task_mast_id):
        """
        Read user record / single record
        :param task_mast_id:
        :return:
        """

        user = TaskMast.query.filter_by(task_mast_id=int(task_mast_id)).first()
        return user

    @task_api_route.expect(update_task_model)
    @task_api_route.marshal_with(update_task_response)
    @login_required(permissions='Task_Config_ID.edit')
    def put(self, task_mast_id):
        """
        Update Task Master record
        :return:
        """
        data = request.json
        response = self.update_record(data, task_mast_id)
        return response

    @task_api_route.expect(update_task_model)
    @task_api_route.marshal_with(update_task_response)
    @login_required(permissions='Task_Config_ID.edit')
    def patch(self, task_mast_id):
        """
        Partial Update Task Master record
        :return:
        """
        data = request.json
        response = self.update_record(data, task_mast_id)
        return response

    @task_api_route.marshal_with(update_task_response)
    @login_required(permissions='Task_Config_ID.delete')
    def delete(self, task_mast_id):
        """
        Soft delete Task Master record
        TODO: Make soft delete
        :return:
        """

        result = ipss_db.update_record(
            model=TaskMast,
            condition=TaskMast.task_mast_id == task_mast_id,

            values={
                'deleted': True,
                'deleted_at': datetime.datetime.now()
            }
        )
        return result

@task_api_route.route('/task_list')
class TaskListApi(Resource):
    per_page = 20

    @task_api_route.marshal_with(task_list_response)
    @task_api_route.doc(params=list_api_params)
    @login_required()
    def get(self):
        """
        List of Task drop down with pagination
        TODO: Search
        :return:
        """
        task_list = TaskMast.query.order_by(TaskMast.created_on.desc())
        response = ipss_db.paginated_results(
            model=TaskMast,
            query=task_list,
            primary_key=primary_key
        )
        return response
######################################################################
