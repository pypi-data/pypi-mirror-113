from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from genesys.app.config import (SVN_PARENT_PATH,
                                SVN_PARENT_URL,
                                FILE_MAP,
                                LOGIN_NAME)
from genesys.app.blueprints.task.utils import create_task_file, create_new_task_acl, delete_task_file
from genesys.app.services import svn_service, queue_store
from genesys.app.utils import config_helpers
import os
from configparser import ConfigParser
from genesys.app import config

task = Blueprint('task', __name__)
api = Api(task)

def update_svn_acl(data, project_name):
    file_map_parser = ConfigParser()
    acl_parser = ConfigParser()

    file_map_url = os.path.join(SVN_PARENT_URL, project_name, '.conf/file_map')
    svn_authz_path = os.path.join(SVN_PARENT_PATH, project_name, 'conf/authz')
    config_helpers.load_file_map(file_map_url, file_map_parser)
    config_helpers.load_config(svn_authz_path, acl_parser)

    svn_service.svn_update_acl(
        base_svn_directory=data['base_svn_directory'],
        acl_parser=acl_parser,
        file_map_parser=file_map_parser,
        task_type=data['task_type'],
        person=data['person'][LOGIN_NAME],
        permission=data['permission']
    )
    if data['permission'] == 'rw':
        for i in data['dependencies']:
            svn_service.svn_update_acl(
                base_svn_directory=i,
                acl_parser=acl_parser,
                file_map_parser=file_map_parser,
                task_type='modeling',
                person=data['person'][LOGIN_NAME],
                permission='r'
            )
    elif data['permission'] == 'none':
        for i in data['dependencies']:
            svn_service.svn_update_acl(
                base_svn_directory=i,
                acl_parser=acl_parser,
                file_map_parser=file_map_parser,
                task_type='modeling',
                person=data['person'][LOGIN_NAME],
                permission='d'
            )

    config_helpers.write_file_map(file_map_url, file_map_parser)
    config_helpers.write_config(svn_authz_path, acl_parser)

class Task(Resource):
    def post(self, project_name):
        data = request.get_json()
        project_repo_url = os.path.join(SVN_PARENT_URL, project_name)
        project = (data['project'])
        root = os.path.join(project['file_tree']['working']['mountpoint'], project['file_tree']['working']['root'],'')
        # replacing file tree mount point with genesys config mount point
        base_file_directory = data['base_file_directory'].split(root,1)[1]
        if config.ENABLE_JOB_QUEUE:
            queue_store.job_queue.enqueue(
                create_task_file,
                args=(project_name, base_file_directory, data['base_svn_directory'], data['all_persons'], data['task_type']),
                job_timeout=10,
            )
            return {"job": "running"}
        else:
            create_task_file(project_name=project_name,
                                base_file_directory=base_file_directory,
                                base_svn_directory=data['base_svn_directory'],
                                all_persons=data['all_persons'],
                                task_type=data['task_type'],
                                )
            return jsonify(message=f'task created')

    def delete(self, project_name):
        data = request.get_json()
        project_repo_url = os.path.join(SVN_PARENT_URL, project_name)
        project = (data['project'])
        root = os.path.join(project['file_tree']['working']['mountpoint'], project['file_tree']['working']['root'],'')
        # replacing file tree mount point with genesys config mount point
        base_file_directory = data['base_file_directory'].split(root,1)[1]
        if config.ENABLE_JOB_QUEUE:
            queue_store.job_queue.enqueue(
                delete_task_file,
                args=(project_name, base_file_directory, data['task_type']),
                job_timeout=10,
            )
            return {"job": "running"}
        else:
            delete_task_file(project_name, base_file_directory, task_type=data['task_type'])
            return jsonify(message=f'task deleted')


class Task_File_Access_Control(Resource):
    def put(self, project_name):
        data = request.get_json()
        if config.ENABLE_JOB_QUEUE:
            queue_store.job_queue.enqueue(
                update_svn_acl,
                args=(data, project_name),
                job_timeout=10,
            )
            return {"job": "running"}
        else:
            update_svn_acl(data, project_name)
            project_repo_url = os.path.join(SVN_PARENT_URL, project_name)
            return jsonify(message=f'project created', project_name=project_name, svn_url=project_repo_url)


api.add_resource(Task, '/task/<string:project_name>')
api.add_resource(Task_File_Access_Control, '/task_acl/<string:project_name>')