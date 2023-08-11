import datetime

from flask import request, session
from flask_restx import Resource
# from .. import ipss_db
from ipss_utils.ipss_api_doc import list_api_params, search_params
from ipss_utils.ipss_db import query_to_dict
from sqlalchemy import text, func, distinct, BigInteger
from ..api_doc import page_fields, get_all_messages
from ..models.page import PageMast
from ipss_utils.decorators import login_required

from ..routes.page import page_api_route, page_list_response, create_page_response, \
    update_page_model, update_page_response
# from sqlalchemy import and_, text
from ..routes.page import create_page_model, get_page_response
from .. import ipss_db, db_client

# Primary key name

primary_key = 'page_id'


@page_api_route.route('/')
class PageConfigApi(Resource):
    per_page = 20

    @page_api_route.marshal_with(page_list_response)
    @page_api_route.doc(params=list_api_params)
    @login_required(permissions='Page_Config_ID.list')
    def get(self):
        """
        List of Page Master with pagination
        TODO: Search
        :return:
        """
        page_list = PageMast.query.order_by(PageMast.created_on.desc())
        response = ipss_db.paginated_results(
            model=PageMast,
            query=page_list,
            primary_key=primary_key
        )
        return response

    @login_required(permissions='Page_Config_ID.add')
    @page_api_route.expect(create_page_model)
    @page_api_route.marshal_with(create_page_response)
    def post(self):
        """
        Create Page Master record and return inserted id
        :return:
        """
        data = request.json
        # remove primary key if exists
        data.pop(primary_key, None)
        current_user = request.args.get('current_user')
        compcode = current_user.get('company_id')
        page_name = data.get('page_name')
        query = text("select * from page_config where lower(page_name) =:page_name and compcode =:compcode "
                     "and deleted is not true "
                     "LIMIT 1")
        query_list = query_to_dict(db_client.engine.execute(
            query,
            page_name=page_name.lower(),
            compcode=compcode
        ))
        if len(query_list):
            return {
                       'success': False,
                       'message': "This page name is already exists",
                   }, 409
        result = ipss_db.insert_record(
            model=PageMast,
            values=data
        )

        return ipss_db.created_response(
            result=result,
            message="Record has been created successfully",
            primary_key=primary_key
        )


@page_api_route.route('/<page_id>/')
class PageUpdateApi(Resource):
    @staticmethod
    def update_record(data, page_id):
        data.pop('page_id', None)
        current_user = request.args.get('current_user')
        compcode = current_user.get('company_id')
        page_name = data.get('page_name')
        query = text("select * from page_config where lower(page_name) =:page_name and compcode =:compcode "
                     "and deleted is not true "
                     "LIMIT 1")
        query_list = query_to_dict(db_client.engine.execute(
            query,
            page_name=page_name.lower(),
            compcode=compcode
        ))
        if len(query_list):
            return {
                       'success': False,
                       'message': "This page name is already exists",
                   }, 409

        result = ipss_db.update_record(
            model=PageMast,
            condition=PageMast.page_id == page_id,
            values=data
        )
        return result

    @page_api_route.marshal_with(get_page_response)
    @login_required(permissions='Page_Config_ID.view')
    def get(self, page_id):
        """
        Read user record / single record
        :param page_id:
        :return:
        """

        user = PageMast.query.filter_by(page_id=int(page_id)).first()
        return user

    @page_api_route.expect(update_page_model)
    @page_api_route.marshal_with(update_page_response)
    @login_required(permissions='Page_Config_ID.edit')
    def put(self, page_id):
        """
        Update Page Master record
        :return:
        """
        data = request.json
        response = self.update_record(data, page_id)
        return response

    @page_api_route.expect(update_page_model)
    @page_api_route.marshal_with(update_page_response)
    @login_required(permissions='Page_Config_ID.edit')
    def patch(self, page_id):
        """
        Partial Update Page Master record
        :return:
        """
        data = request.json
        response = self.update_record(data, page_id)
        return response

    @page_api_route.marshal_with(update_page_response)
    @login_required(permissions='Page_Config_ID.delete')
    def delete(self, page_id):
        """
        Soft delete Page Master record
        TODO: Make soft delete
        :return:
        """

        result = ipss_db.update_record(
            model=PageMast,
            condition=PageMast.page_id == page_id,

            values={
                'deleted': True,
                'deleted_at': datetime.datetime.now()
            }
        )
        return result


@page_api_route.route('/page_list')
class PageListApi(Resource):
    per_page = 20

    @page_api_route.marshal_with(page_list_response)
    @page_api_route.doc(params=list_api_params)
    @login_required()
    def get(self):
        """
        List of Page drop down with pagination
        TODO: Search
        :return:
        """
        page_list = PageMast.query.order_by(PageMast.created_on.desc())
        response = ipss_db.paginated_results(
            model=PageMast,
            query=page_list,
            primary_key=primary_key
        )
        return response
######################################################################
