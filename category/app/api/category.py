import datetime

from flask import request, session
from flask_restx import Resource
# from .. import ipss_db
from ipss_utils.ipss_api_doc import list_api_params, search_params
from ipss_utils.ipss_db import query_to_dict
from sqlalchemy import text, func, distinct, BigInteger
from ..api_doc import category_fields, get_all_messages
from ..models.category import CategoryConfigMast
from ipss_utils.decorators import login_required

from ..routes.category import category_config_api_route, category_config_list_response, create_category_config_response, \
    update_category_config_model, update_category_config_response
# from sqlalchemy import and_, text
from ..routes.category import create_category_config_model, get_category_config_response
from .. import ipss_db, db_client

# Primary key name

primary_key = 'category_mast_id'


@category_config_api_route.route('/')
class CategoryConfigApi(Resource):
    per_page = 20

    @category_config_api_route.marshal_with(category_config_list_response)
    @category_config_api_route.doc(params=list_api_params)
    @login_required(permissions='Category_Config_ID.list')
    def get(self):
        """
        List of Category with pagination
        TODO: Search
        :return:
        """
        category_list = CategoryConfigMast.query.order_by(CategoryConfigMast.created_on.desc())
        response = ipss_db.paginated_results(
            model=CategoryConfigMast,
            query=category_list,
            primary_key=primary_key
        )
        return response

    @login_required(permissions='Category_Config_ID.add')
    @category_config_api_route.expect(create_category_config_model)
    @category_config_api_route.marshal_with(create_category_config_response)
    def post(self):
        """
        Create Category Master record and return inserted id
        :return:
        """
        data = request.json
        # remove primary key if exists
        current_user = request.args.get('current_user')
        compcode = current_user.get('company_id')
        data.pop(primary_key, None)
        category_name = data.get('category_name')
        query = text("select * from category_config where lower(category_name) =:category_name and compcode =:compcode "
                     "and deleted is not true "
                     "LIMIT 1")
        query_list = query_to_dict(db_client.engine.execute(
            query,
            category_name=category_name.lower(),
            compcode=compcode
        ))
        if len(query_list):
            return {
                       'success': False,
                       'message': "This category name is already exists",
                   }, 409
        result = ipss_db.insert_record(
            model=CategoryConfigMast,
            values=data
        )

        return ipss_db.created_response(
            result=result,
            message="Record has been created successfully",
            primary_key=primary_key
        )


@category_config_api_route.route('/<category_mast_id>/')
class CategoryConfigUpdateApi(Resource):
    @staticmethod
    def update_record(data, category_mast_id):
        data.pop('category_mast_id', None)
        category_name = data.get('category_name')
        current_user = request.args.get('current_user')
        compcode = current_user.get('company_id')
        query = text("select * from category_config where lower(category_name) =:category_name and deleted is not true "
                     "and compcode =:compcode "
                     "LIMIT 1")
        query_list = query_to_dict(db_client.engine.execute(
            query,
            category_name=category_name.lower(),
            compcode=compcode
        ))
        if len(query_list):
            return {
                       'success': False,
                       'message': "This category name is already exists",
                   }, 409

        result = ipss_db.update_record(
            model=CategoryConfigMast,
            condition=CategoryConfigMast.category_mast_id == category_mast_id,
            values=data
        )
        return result

    @category_config_api_route.marshal_with(get_category_config_response)
    @login_required(permissions='Category_Config_ID.view')
    def get(self, category_mast_id):
        """
        Read user record / single record
        :param category_mast_id:
        :return:
        """

        user = CategoryConfigMast.query.filter_by(category_mast_id=int(category_mast_id)).first()
        return user

    @category_config_api_route.expect(update_category_config_model)
    @category_config_api_route.marshal_with(update_category_config_response)
    @login_required(permissions='Category_Config_ID.edit')
    def put(self, category_mast_id):
        """
        Update Category Master record
        :return:
        """
        data = request.json
        response = self.update_record(data, category_mast_id)
        return response

    @category_config_api_route.expect(update_category_config_model)
    @category_config_api_route.marshal_with(update_category_config_response)
    @login_required(permissions='Category_Config_ID.edit')
    def patch(self, category_mast_id):
        """
        Partial Update Category Master record
        :return:
        """
        data = request.json
        response = self.update_record(data, category_mast_id)
        return response

    @category_config_api_route.marshal_with(update_category_config_response)
    @login_required(permissions='Category_Config_ID.delete')
    def delete(self, category_mast_id):
        """
        Soft delete Category Master record
        TODO: Make soft delete
        :return:
        """

        result = ipss_db.update_record(
            model=CategoryConfigMast,
            condition=CategoryConfigMast.category_mast_id == category_mast_id,

            values={
                'deleted': True,
                'deleted_at': datetime.datetime.now()
            }
        )
        return result

@category_config_api_route.route('/category_list')
class CategoryListApi(Resource):
    per_page = 20

    @category_config_api_route.marshal_with(category_config_list_response)
    @category_config_api_route.doc(params=list_api_params)
    @login_required()
    def get(self):
        """
        List of Category drop down with pagination
        TODO: Search
        :return:
        """
        category_list = CategoryConfigMast.query.order_by(CategoryConfigMast.created_on.desc())
        response = ipss_db.paginated_results(
            model=CategoryConfigMast,
            query=category_list,
            primary_key=primary_key
        )
        return response

######################################################################
