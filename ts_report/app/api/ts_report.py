# import datetime

from flask import request
from flask_restx import Resource
from ipss_utils.decorators import login_required
from ipss_utils.ipss_api_doc import list_api_params
from ipss_utils.ipss_db import query_to_dict
from sqlalchemy import and_, text
from .. import ipss_db, db_client
from ..api_doc import search_params
from ..routes.ts_report import timesheet_report_api_route, timesheet_report_response, project_report_response
from datetime import datetime, timedelta


@timesheet_report_api_route.route('/')
class TimesheetReportApi(Resource):
    @timesheet_report_api_route.marshal_with(timesheet_report_response)
    @timesheet_report_api_route.doc(params=search_params)
    @login_required(permissions='ts_report_id.view')
    # @login_required()
    def get(self):
        current_user = request.args.get('current_user')
        compcode = current_user.get('company_id')
        # compcode = 1
        start_date = request.args.get('from_date')
        date_query = text('select min(from_date),max(to_date) from timesheet where deleted is not true')
        date_list = query_to_dict(db_client.engine.execute(date_query))
        print('date_list', date_list)
        min_from_date = date_list[0].get('min')
        max_to_date = date_list[0].get('max')

        if start_date:
            date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            if date_obj.weekday() != 0:
                print('not monday')
                # days_to_monday1 = (0 - date_obj.weekday()) % 7
                from_date = (date_obj - timedelta(days=date_obj.weekday())).strftime('%Y-%m-%d')
            else:
                from_date = start_date
        else:
            from_date = min_from_date
            start_date = min_from_date

        end_date = request.args.get('to_date')
        if end_date:
            date_object = datetime.strptime(end_date, '%Y-%m-%d').date()
            if date_object.weekday() != 6:
                print('not sunday')
                # days_to_sunday2 = (6 - date_object.weekday()) % 7
                to_date = (date_object + timedelta(days=6 - date_object.weekday())).strftime('%Y-%m-%d')
            else:
                to_date = end_date
        else:
            to_date = max_to_date
            end_date = max_to_date

        print('monday_date', from_date, type(from_date))
        print('sunday_date', to_date, type(to_date))
        print(start_date, end_date)
        activity_id = request.args.get('activity_id').split(',') if request.args.get('activity_id') else ''
        project_id = request.args.get('project_id').split(',') if request.args.get('project_id') else ''
        task_id = request.args.get('task_id').split(',') if request.args.get('task_id') else ''
        # category_id = request.args.get('category_id').split(',') if request.args.get('category_id') else ''
        # page_id = request.args.get('page_id').split(',') if request.args.get('page_id') else ''
        filters = ''
        if from_date and to_date:
            filters += "and (timesheet.from_date between :from_date AND :to_date ) "
        if project_id:
            filters += "and timesheet_self.project_id in :project_id "
        if activity_id:
            filters += "and timesheet_self.task_id in :activity_id "
        if task_id:
            filters += "and timesheet_self.category_id in :task_id "
        # if category_id:
        #     filters += "and timesheet_self.category_id in :category_id "
        # if page_id:
        #     filters += "and timesheet_self.page_id in :page_id "

        query = text("select "
                     "timesheet_self.hrs_per_task,"
                     "timesheet_self.project_id as project_id ,"
                     "project_mast.project_name,"
                     "timesheet_self.task_id as activity_id, "
                     "main_activities.activity_name as activity_name ,"
                     "timesheet_self.category_id as task_id, "
                     "task_mast.task_name,"
                     "timesheet.from_date,"
                     "timesheet.to_date,"
                     " timesheet_self.mon,"
                     "timesheet_self.tue,"
                     " timesheet_self.wed,"
                     " timesheet_self.thu,"
                     " timesheet_self.fri,"
                     " timesheet_self.sat,"
                     " timesheet_self.sun,"
                     "emp.empid as emp_company_id,timesheet.send,timesheet.status,"
                     "CONCAT (emp.fname,' ',emp.lname) as emp_name "
                     "from timesheet join timesheet_self on timesheet.sheet_id = timesheet_self.sheet_id "
                     "JOIN project_mast on project_mast.project_id = timesheet_self.project_id "
                     "JOIN main_activities ON timesheet_self.task_id = main_activities.activity_id "
                     "JOIN task_mast ON timesheet_self.category_id=task_mast.task_mast_id  "
                     # "JOIN category_config on timesheet_self.category_id = category_config.category_mast_id "
                     # "JOIN page_config on timesheet_self.page_id = page_config.page_id "
                     "JOIN hremploymast as emp ON timesheet.emp_id=emp.hremploymastid "
                     "where timesheet.deleted is not true and "
                     "timesheet.send is true and timesheet.status = 'approved' and timesheet.compcode=:compcode "
                     f"{filters}"
                     )

        result = query_to_dict(db_client.engine.execute(
            query,
            from_date=from_date,
            to_date=to_date,
            compcode=compcode,
            project_id=tuple(project_id),
            activity_id=tuple(activity_id),
            task_id=tuple(task_id),
            # category_id=tuple(category_id),
            # page_id=tuple(page_id)
        ))

        series_query = text(' SELECT json_agg(date_str)'
                            "FROM ("
                            " SELECT to_char(dates, 'YYYY-MM-DD') AS date_str "
                            "FROM generate_series(:from_date ::date, :to_date ::date, '1 day'::interval) "
                            "AS dates"
                            ') AS subquery')
        series = query_to_dict(db_client.engine.execute(series_query, from_date=start_date, to_date=end_date))
        print('series', series[0].get('json_agg'))
        result_data = []
        days_list = {'Monday': 'mon', 'Tuesday': 'tue', 'Wednesday': 'wed', 'Thursday': 'thu', 'Friday': 'fri',
                     'Saturday': 'sat', 'Sun': 'sun'}
        print("result", result)
        for date_series in series[0].get('json_agg'):
            for res in result:
                # print(type(date_series), 'date_series', type(res.get('from_date'))) print(res.get(
                # 'from_date').strftime('%Y-%m-%d'), date_series, res.get('to_date').strftime('%Y-%m-%d')) print(
                # res.get('from_date').strftime('%Y-%m-%d') <= date_series <= res.get('to_date').strftime('%Y-%m-%d'))
                if res.get('from_date').strftime('%Y-%m-%d') <= date_series <= res.get('to_date').strftime('%Y-%m-%d'):
                    print('in', date_series)
                    obj = datetime.strptime(date_series, '%Y-%m-%d')
                    day = obj.strftime('%A')
                    print(day)
                    if day in days_list:
                        print('yyy', type(res.get(days_list[day])))
                        if res.get(days_list[day]) != 0.00:
                            var = {
                                'project_name': res.get('project_name'),
                                'project_id': res.get('project_id'),
                                'activity_name': res.get('activity_name'),
                                'activity_id': res.get('activity_id'),
                                'task_name': res.get('task_name'),
                                'task_id': res.get('task_id'),
                                # 'category_name': res.get('category_name'),
                                'from_date': res.get('from_date'),
                                'to_date': res.get('to_date'),
                                'hrs_per_task': res.get(days_list[day]),
                                'emp_name': res.get('emp_name'),
                                'emp_company_id': res.get('emp_company_id')
                            }
                            result_data.append(var)

        # sub_query = text("select "
        #                  "sum(timesheet_self.hrs_per_task) as total_hrs "
        #                  "from timesheet join timesheet_self on timesheet.sheet_id = timesheet_self.sheet_id "
        #                  "JOIN main_activities ON timesheet_self.project_id=main_activities.activity_id "
        #                  "JOIN project_mast on project_mast.project_id = main_activities.project_id "
        #                  "JOIN task_mast ON timesheet_self.task_id=task_mast.task_mast_id "
        #                  "JOIN category_config on timesheet_self.category_id = category_config.category_mast_id "
        #                  # "JOIN page_config on timesheet_self.page_id = page_config.page_id "
        #                  "JOIN hremploymast as emp ON timesheet.emp_id=emp.hremploymastid "
        #                  "where timesheet.deleted is not true and "
        #                  "timesheet.send is true and timesheet.status = 'approved' and timesheet.compcode=:compcode "
        #                  f"{filters}"
        #                  )
        # total_hrs = query_to_dict(db_client.engine.execute(
        #     sub_query,
        #     from_date=from_date,
        #     to_date=to_date,
        #     compcode=compcode,
        #     project_id=tuple(project_id),
        #     activity_id=tuple(activity_id),
        #     task_id=tuple(task_id),
        #     category_id=tuple(category_id),
        #     # page_id=tuple(page_id)
        # ))
        print('result_data', result_data)
        result_dict = {}
        for data in result_data:
            key = (data['project_name'], data['activity_name'], data['task_name'],
                   data['emp_name'], data['emp_company_id'], data['from_date'], data['to_date'])
            if key in result_dict:
                result_dict[key]['hrs_per_task'] += data['hrs_per_task']
            else:
                result_dict[key] = data
        result_data = list(result_dict.values())
        total = 0
        for i in result_data:
            total += float(i.get('hrs_per_task'))
        return {
            'length': len(result_data),
            'total_hrs': "%.2f" % total,
            'result': result_data
        }


@timesheet_report_api_route.route('/project_report')
class ProjectReportApi(Resource):
    def build_hierarchy_tree(self, employees, manager_id=None, visited=None):
        if visited is None:
            visited = set()
        nodes = []
        for employee in employees:
            if employee['emp_id'] in visited:
                continue
            if employee['manager_id'] == manager_id:
                visited.add(employee['emp_id'])
                node = {
                    'emp_id': employee['emp_id'],
                    'emp_name': employee['emp_name'],
                    'children': self.build_hierarchy_tree(employees, employee['emp_id'], visited)
                }
                nodes.append(node)
        return nodes

    def find_node(self, node, target_id):
        if node["emp_id"] == target_id:
            return node
        for child in node["children"]:
            found_node = self.find_node(child, target_id)
            if found_node is not None:
                return found_node
        return None

    def get_children_info(self, node):
        children_info = []
        for child in node["children"]:
            child_info = {"emp_name": child["emp_name"], "emp_id": child["emp_id"]}
            children_info.append(child_info)
            children_info.extend(self.get_children_info(child))
        return children_info

    def find_internal_children_root_ids(self, root):
        children = root.get('children', [])
        internal_children_root_ids = []
        for child in children:
            if child.get('children'):
                internal_children_root_ids.append(child['emp_id'])
            internal_children_root_ids.extend(self.find_internal_children_root_ids(child))
        return internal_children_root_ids

    @timesheet_report_api_route.marshal_with(project_report_response)
    # @timesheet_report_api_route.doc(params=search_params)
    @login_required(permissions='ts_report_id.view')
    # @login_required()
    def get(self):
        current_user = request.args.get('current_user')
        compcode = current_user.get('company_id')
        node_id = current_user.get('emp_id')
        print('node_id', node_id)
        user_name = current_user.get('username')
        print('user_name', user_name)
        # query for employee with manager_id
        query = text('select team_members.employee_id as emp_id,'
                     "concat(hremploymast.fname,' ',hremploymast.lname) as emp_name,"
                     'team_members.manager_id as manager_id '
                     'from team_members join hremploymast on '
                     'team_members.employee_id = hremploymast.hremploymastid '
                     'where team_members.deleted is not true and team_members.compcode=:compcode ')
        manager_id_list = query_to_dict(db_client.engine.execute(query, compcode=compcode))

        # query for find root node of the tree
        sub_query = text("select distinct(team_assign.manager_id) as emp_id,"
                         "concat(hremploymast.fname,' ',hremploymast.lname) as emp_name "
                         "from team_assign join hremploymast on  team_assign.manager_id = hremploymast.hremploymastid "
                         'where team_assign.compcode=:compcode and '
                         'team_assign.manager_id not in (select employee_id from team_members where team_members.deleted is '
                         'not true) '
                         'and team_assign.deleted is not true')

        sub_query_list = query_to_dict(db_client.engine.execute(sub_query, compcode=compcode))

        if len(sub_query_list) == 1:

            sub_query_list[0].update({'manager_id': None})

            employees = sub_query_list + manager_id_list

            hierarchy = self.build_hierarchy_tree(employees)

            target_id = node_id  # ID of the node whose children's info we want to get
            target_node = self.find_node(hierarchy[0], target_id)
            if target_node is not None:
                print('target_node', target_node)
                children_root_ids = self.find_internal_children_root_ids(target_node)
                if len(children_root_ids):
                    print('children_root_ids', children_root_ids)
                    children_root_ids.append(target_id)
                    print('children_root_ids', children_root_ids)
                    employee_id = children_root_ids
                else:
                    children_info = self.get_children_info(target_node)
                    print('children_info', children_info)
                    if len(children_info):
                        employee_id = [target_id]
                        print('if', employee_id)
                    else:
                        employee_id = [0]
                        print('else', employee_id)
                    # children_root_ids.append(target_id)
                    # print('children_root_ids2', children_root_ids)
                    # employee_id = children_root_ids
            else:
                employee_id = [0]
        else:
            employee_id = [0]

        user_query = text('select json_agg(email) as username from hremploymast where hremploymastid in :employee_id '
                          'and compcode=:compcode')
        user_list = query_to_dict(db_client.engine.execute(user_query,
                                                           compcode=compcode,
                                                           employee_id=tuple(employee_id)))
        print('user_list', user_list)
        if user_list[0].get('username') is not None:
            print('user_list', user_list)
            username_list = user_list[0].get('username')
            print('username_list', username_list)
        else:
            username_list = ['']

        project_query = text('select * from project_mast where deleted is not true and compcode=:compcode '
                             'and created_by in :username_list ')

        project_list = query_to_dict(db_client.engine.execute(project_query,
                                                              compcode=compcode,
                                                              username_list=tuple(username_list)))

        print('project_list', project_list)
        return {
            'length': len(project_list),
            'results': project_list
        }
