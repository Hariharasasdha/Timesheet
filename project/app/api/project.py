import datetime

from flask import request, session
from flask_restx import Resource
# from .. import ipss_db
from ipss_utils.ipss_api_doc import list_api_params, search_params
from ipss_utils.ipss_db import query_to_dict
from sqlalchemy import text, func, distinct, BigInteger
from ..api_doc import project_fields, get_all_messages, filter_params, params_search
from ..models.project import ProjectMast, MainActivities
from ipss_utils.decorators import login_required

from ..routes.project import project_api_route, project_list_response, create_project_response, \
    update_project_model, update_project_response, activity_list_response, create_activity_model, \
    create_activity_response, get_activity_response, update_activity_model, \
    update_activity_response, activity_api_route, activity_get_response
# from sqlalchemy import and_, text
from ..routes.project import create_project_model, get_project_response
from .. import ipss_db, db_client

# Primary key name

primary_key = 'project_id'


@project_api_route.route('/')
class ProjectApi(Resource):
    per_page = 20

    @project_api_route.marshal_with(project_list_response)
    @project_api_route.doc(params=list_api_params)
    @login_required()
    # @login_required()
    def get(self):
        """
        List of Project with pagination
        TODO: Search
        :return:
        """
        # current_user = request.args.get('current_user')
        # # print('current_user', current_user)
        # user_name = current_user.get('username')
        # # print('user_name', user_name)
        # user_role = current_user.get('user_roles')
        # # print('user_roles', user_role)
        # project_list = ProjectMast.query.order_by(ProjectMast.created_on.desc())
        # if 'Super Admin' not in user_role:
        #     project_list = project_list.filter_by(created_by=user_name)
        # response = ipss_db.paginated_results(
        #     model=ProjectMast,
        #     query=project_list,
        #     primary_key=primary_key
        # )
        # return response
        results_per_page = int(request.args.get('results_per_page')) if request.args.get(
            'results_per_page') else self.per_page
        paged = int(request.args.get('paged')) if request.args.get('paged') else 1
        offset = (paged - 1) * results_per_page
        current_user = request.args.get('current_user')
        compcode = current_user.get('company_id')

        user_name = current_user.get('username')
        user_role = current_user.get('user_roles')
        print(compcode, user_name, user_role)
        filters = ''
        if 'Super Admin' not in user_role:
            filters += f' and project_mast.created_by =:user_name '

        query = text(
            'SELECT '
            "project_mast.*,concat(hremploymast.idcardno,' - ',hremploymast.fname,' ',hremploymast.lname) as "
            "created_username "
            'from project_mast join hremploymast on lower(hremploymast.email)=lower(project_mast.created_by) '
            ' where project_mast. deleted is not true and project_mast.compcode= :compcode '
            f'{filters} '
            'ORDER BY project_mast.created_on DESC '
            'LIMIT :limit OFFSET :offset'
        )

        results = query_to_dict(db_client.engine.execute(query,
                                                         compcode=compcode,
                                                         user_name=user_name,
                                                         limit=results_per_page,
                                                         offset=offset))

        return {
            'primary_key': primary_key,
            'total_results': len(results),
            'page': paged,
            'results_per_page': results_per_page,
            'results': results
        }

    @login_required(permissions='Project_Config_ID.add')
    @project_api_route.expect(create_project_model)
    @project_api_route.marshal_with(create_project_response)
    def post(self):
        """
        Create Project Master record and return inserted id
        :return:
        """
        data = request.json
        # remove primary key if exists
        current_user = request.args.get('current_user')
        compcode = current_user.get('company_id')
        data.pop(primary_key, None)
        project_name = data.get('project_name')
        query = text("select * from project_mast where lower(project_name) =:project_name and compcode =:compcode "
                     "and deleted is not true "
                     "LIMIT 1")
        query_list = query_to_dict(db_client.engine.execute(
            query,
            project_name=project_name.lower(),
            compcode=compcode
        ))
        if len(query_list):
            return {
                       'success': False,
                       'message': "This project name is already exists",
                   }, 409
        result = ipss_db.insert_record(
            model=ProjectMast,
            values=data
        )

        return ipss_db.created_response(
            result=result,
            message="Record has been created successfully",
            primary_key=primary_key
        )


@project_api_route.route('/<project_id>/')
class ProjectUpdateApi(Resource):
    @staticmethod
    def update_record(data, project_id):
        data.pop('project_id', None)
        # project_name = data.get('project_name')
        # current_user = request.args.get('current_user')
        # compcode = current_user.get('company_id')
        # query = text("select * from project_mast where lower(project_name) =:project_name and deleted is not true "
        #              "and compcode =:compcode "
        #              "LIMIT 1")
        # query_list = query_to_dict(db_client.engine.execute(
        #     query,
        #     project_name=project_name.lower(),
        #     compcode=compcode
        # ))
        # if len(query_list):
        #     return {
        #                'success': False,
        #                'message': "This project name is already exists",
        #            }, 409

        result = ipss_db.update_record(
            model=ProjectMast,
            condition=ProjectMast.project_id == project_id,
            values=data
        )
        return result

    @project_api_route.marshal_with(get_project_response)
    @login_required(permissions='Project_Config_ID.view')
    def get(self, project_id):
        """
        Read user record / single record
        :param project_id:
        :return:
        """

        user = ProjectMast.query.filter_by(project_id=int(project_id)).first()
        return user

    @project_api_route.expect(update_project_model)
    @project_api_route.marshal_with(update_project_response)
    @login_required(permissions='Project_Config_ID.edit')
    def put(self, project_id):
        """
        Update Project Master record
        :return:
        """
        data = request.json
        response = self.update_record(data, project_id)
        return response

    @project_api_route.expect(update_project_model)
    @project_api_route.marshal_with(update_project_response)
    @login_required(permissions='Project_Config_ID.edit')
    def patch(self, project_id):
        """
        Partial Update Project Master record
        :return:
        """
        data = request.json
        response = self.update_record(data, project_id)
        return response

    @project_api_route.marshal_with(update_project_response)
    @login_required(permissions='Project_Config_ID.delete')
    def delete(self, project_id):
        """
        Soft delete Project Master record
        TODO: Make soft delete
        :return:
        """

        result = ipss_db.update_record(
            model=ProjectMast,
            condition=ProjectMast.project_id == project_id,

            values={
                'deleted': True,
                'deleted_at': datetime.datetime.now()
            }
        )
        return result


@project_api_route.route('/project_list')
class ProjectListApi(Resource):
    per_page = 20

    @project_api_route.marshal_with(project_list_response)
    @project_api_route.doc(params=list_api_params)
    @login_required()
    def get(self):
        """
        List of Project drop down with pagination
        TODO: Search
        :return:
        """
        current_user = request.args.get('current_user')
        # print('current_user', current_user)
        user_name = current_user.get('username')
        # print('user_name', user_name)
        user_role = current_user.get('user_roles')
        # print('user_roles', user_role)
        project_list = ProjectMast.query.order_by(ProjectMast.created_on.desc())
        if 'Super Admin' not in user_role:
            project_list = project_list.filter_by(created_by=user_name)
        response = ipss_db.paginated_results(
            model=ProjectMast,
            query=project_list,
            primary_key=primary_key
        )
        return response


######################################################################
# Primary key name

primary_key_1 = 'activity_id'


@activity_api_route.route('/')
class MainActivityApi(Resource):
    per_page = 20

    @activity_api_route.marshal_with(activity_list_response)
    @activity_api_route.doc(params=list_api_params)
    @activity_api_route.doc(params=filter_params)
    @login_required(permissions='Activity_ID.list')
    def get(self):
        """
        List of Activities with pagination
        TODO: Search
        :return:
        """
        project_id = request.args.get('project_id')
        activity_list = MainActivities.query.order_by(MainActivities.created_on.desc())
        if project_id:
            activity_list = activity_list.filter_by(project_id=project_id)
        response = ipss_db.paginated_results(
            model=MainActivities,
            query=activity_list,
            primary_key=primary_key_1
        )
        return response

    @login_required(permissions='Activity_ID.add')
    @activity_api_route.expect(create_activity_model)
    @activity_api_route.marshal_with(create_activity_response)
    def post(self):
        """
        Create Activities record and return inserted id
        :return:
        """
        data = request.json
        # remove primary key if exists
        current_user = request.args.get('current_user')
        compcode = current_user.get('company_id')
        data.pop(primary_key_1, None)
        # duplication control
        # project_id = data.get('project_id')
        # activity_name = data.get('activity_name')
        # query = text("select * from main_activities where ((lower(activity_name) =:activity_name and "
        #              "project_id=:project_id) or lower(activity_name) =:activity_name) "
        #              "and compcode =:compcode "
        #              "and deleted is not true  "
        #              "LIMIT 1")
        # query_list = query_to_dict(db_client.engine.execute(
        #     query,
        #     project_id=project_id,
        #     activity_name=activity_name.lower(),
        #     compcode=compcode
        # ))
        # if len(query_list):
        #     return {
        #                'success': False,
        #                'message': "This activity name is already exists",
        #            }, 409
        result = ipss_db.insert_record(
            model=MainActivities,
            values=data
        )

        return ipss_db.created_response(
            result=result,
            message="Record has been created successfully",
            primary_key=primary_key_1
        )


@activity_api_route.route('/<activity_id>/')
class ActivityUpdateApi(Resource):
    @staticmethod
    def update_record(data, activity_id):
        data.pop('activity_id', None)
        # duplication control
        # current_user = request.args.get('current_user')
        # compcode = current_user.get('company_id')
        # project_id = data.get('project_id')
        # activity_name = data.get('activity_name')
        # query = text("select * from main_activities where ((lower(activity_name) =:activity_name and "
        #              "project_id=:project_id) or lower(activity_name) =:activity_name) "
        #              "and compcode =:compcode "
        #              "and deleted is not true  "
        #              "LIMIT 1")
        # query_list = query_to_dict(db_client.engine.execute(
        #     query,
        #     project_id=project_id,
        #     activity_name=activity_name.lower(),
        #     compcode=compcode
        # ))
        # if len(query_list):
        #     return {
        #                'success': False,
        #                'message': "This activity name is already exists",
        #            }, 409

        result = ipss_db.update_record(
            model=MainActivities,
            condition=MainActivities.activity_id == activity_id,
            values=data
        )
        return result

    @activity_api_route.marshal_with(get_activity_response)
    @login_required(permissions='Activity_ID.view')
    def get(self, activity_id):
        """
        Read user record / single record
        :param activity_id:
        :return:
        """

        user = MainActivities.query.filter_by(activity_id=int(activity_id)).first()
        return user

    @activity_api_route.expect(update_activity_model)
    @activity_api_route.marshal_with(update_activity_response)
    @login_required(permissions='Activity_ID.edit')
    def put(self, activity_id):
        """
        Update Activity record
        :return:
        """
        data = request.json
        response = self.update_record(data, activity_id)
        return response

    @activity_api_route.expect(update_activity_model)
    @activity_api_route.marshal_with(update_activity_response)
    @login_required(permissions='Activity_ID.edit')
    def patch(self, activity_id):
        """
        Partial Update Activity record
        :return:
        """
        data = request.json
        response = self.update_record(data, activity_id)
        return response

    @activity_api_route.marshal_with(update_activity_response)
    @login_required(permissions='Activity_ID.delete')
    def delete(self, activity_id):
        """
        Soft delete Activity record
        TODO: Make soft delete
        :return:
        """

        result = ipss_db.update_record(
            model=MainActivities,
            condition=MainActivities.activity_id == activity_id,

            values={
                'deleted': True,
                'deleted_at': datetime.datetime.now()
            }
        )
        return result


@activity_api_route.route('/activity_list')
class ActivityDropDown(Resource):
    @activity_api_route.marshal_with(activity_get_response)
    # @activity_api_route.doc(params=list_api_params)
    @activity_api_route.doc(params=params_search)
    @login_required()
    def get(self):
        """
        List of Activities drop down with pagination
        TODO: Search
        :return:
        """
        current_user = request.args.get('current_user')
        print('current_user', current_user)
        compcode = current_user.get('company_id')
        project_id = request.args.get('project_id').split(',') if request.args.get('project_id') else ''
        filters = ''
        if project_id:
            filters += 'and project_id in :project_id '

        activity_list = text('select * from main_activities where deleted is not true and compcode=:compcode '
                             f'{filters}'
                             'order by created_on desc  ')
        result = query_to_dict(db_client.engine.execute(activity_list,
                                                        compcode=compcode,
                                                        project_id=tuple(project_id)))
        return {
            'length': len(result),
            'result': result
        }
        # activity_list = MainActivities.query.order_by(MainActivities.created_on.desc())
        # if project_id:
        #     activity_list = activity_list.filter_by(project_id=project_id)
        # response = ipss_db.paginated_results(
        #     model=MainActivities,
        #     query=activity_list,
        #     primary_key=primary_key
        # )
        # return response
######################################################################
