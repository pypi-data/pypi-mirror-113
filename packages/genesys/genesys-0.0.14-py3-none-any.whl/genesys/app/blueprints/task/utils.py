import os
from genesys.app.services import files_service, svn_service
from genesys.app.config import SVN_PARENT_PATH, SVN_PARENT_URL, TEMPLATE_FILES_DIR
from configparser import NoOptionError
from genesys.app.utils import config_helpers
from configparser import ConfigParser
from genesys.app.config import (SVN_PARENT_PATH,
                                SVN_PARENT_URL,
                                FILE_MAP,
                                LOGIN_NAME)

def create_task_file(project_name, base_file_directory, base_svn_directory, all_persons, task_type):
    file_map_parser = ConfigParser()
    acl_parser = ConfigParser()
    svn_authz_path = os.path.join(SVN_PARENT_PATH, project_name, 'conf/authz')
    blend_file_url = os.path.join(SVN_PARENT_URL, base_file_directory)
    all_users = [person[LOGIN_NAME] for person in all_persons]
    file_map_url = os.path.join(SVN_PARENT_URL, project_name, '.conf/file_map')

    config_helpers.load_file_map(file_map_url, file_map_parser)
    config_helpers.load_config(svn_authz_path, acl_parser)


    file_folder_url = os.path.dirname(blend_file_url)
    try:
        task_type_map = file_map_parser.get('file_map', task_type).lower()
        if task_type_map == 'base':
            if not svn_service.is_svn_url(file_folder_url):
                svn_service.svn_make_dirs(file_folder_url, log_message=f'created {file_folder_url}')
            if not svn_service.is_svn_url(f'{blend_file_url}.blend'):
                svn_service.svn_import(path=os.path.join(TEMPLATE_FILES_DIR,'blender.blend'),
                                        repo_url=f'{blend_file_url}.blend',
                                        log_message=f'create {blend_file_url}.blend')
        elif task_type_map == 'none':
            pass
        else:
            if not svn_service.is_svn_url(file_folder_url):
                svn_service.svn_make_dirs(file_folder_url, log_message=f'created {file_folder_url}')
            if not svn_service.is_svn_url(f'{blend_file_url}_{task_type_map}.blend'):
                svn_service.svn_import(path=os.path.join(TEMPLATE_FILES_DIR,'blender.blend'),
                                        repo_url=f'{blend_file_url}_{task_type_map}.blend',
                                        log_message=f'create {blend_file_url}.blend')
    except NoOptionError:
        if not svn_service.is_svn_url(file_folder_url):
            svn_service.svn_make_dirs(file_folder_url, log_message=f'created {file_folder_url}')
        if not svn_service.is_svn_url(f'{blend_file_url}_{task_type}.blend'):
            svn_service.svn_import(path=os.path.join(TEMPLATE_FILES_DIR,'blender.blend'),
                                        repo_url=f'{blend_file_url}_{task_type}.blend',
                                        log_message=f'create {blend_file_url}.blend')
        file_map_parser.set('file_map', task_type, task_type)
    

    #TODO create acl fo new task
    create_new_task_acl(all_users=all_users,
                        base_svn_directory=base_svn_directory,
                        acl_parser=acl_parser,
                        file_map_parser=file_map_parser,
                        task_type=task_type)

    config_helpers.write_file_map(file_map_url, file_map_parser)
    config_helpers.write_config(svn_authz_path, acl_parser)

def create_new_task_acl(all_users, base_svn_directory, acl_parser, file_map_parser, task_type):
    try:
        task_type_map = file_map_parser.get('file_map', task_type).lower()
        if task_type_map == 'base':
            svn_directory = f'{base_svn_directory}.blend'
            if svn_directory in acl_parser:
                pass
            else:
                for user in all_users:
                    if svn_directory in acl_parser:
                        acl_parser.set(svn_directory, user, '')
                    else:
                        acl_parser[svn_directory] = {
                            '@admin':'rw',
                            user:''
                        }
        elif task_type_map == 'none':
            pass
        else:
            svn_directory = f'{base_svn_directory}_{task_type_map}.blend'
            if svn_directory in acl_parser:
                pass
            else:
                for user in all_users:
                    if svn_directory in acl_parser:
                        acl_parser.set(svn_directory, user, '')
                    else:
                        acl_parser[svn_directory] = {
                            '@admin':'rw',
                            user:''
                        }
    except NoOptionError:
        svn_directory = f'{base_svn_directory}_{task_type}.blend'
        if svn_directory in acl_parser:
            pass
        else:
            for user in all_users:
                if svn_directory in acl_parser:
                    acl_parser.set(svn_directory, user, '')
                else:
                    acl_parser[svn_directory] = {
                        '@admin':'rw',
                        user:''
                    }

def delete_task_file(project_name, base_file_directory, task_type):
    file_map_parser = ConfigParser()
    acl_parser = ConfigParser()
    svn_authz_path = os.path.join(SVN_PARENT_PATH, project_name, 'conf/authz')
    # if asset_task['entity_type'] == 'asset':
    #     new_blend_file_url = os.path.join(os.path.dirname(blend_file_url), asset_task['new_file_name'])
    # elif asset_task['entity_type'] == 'shot':
    #     shot_folder = os.path.join(os.path.dirname(os.path.dirname(blend_file_url)), \
    #         asset_task['new_file_name'].rsplit('_', 1)[1])
    #     new_blend_file_url = os.path.join(shot_folder, asset_task['new_file_name'])
    #     print('shot', new_blend_file_url)
    #     print(shot_folder)
    blend_file_url = os.path.join(SVN_PARENT_URL, base_file_directory)
    file_map_url = os.path.join(SVN_PARENT_URL, project_name, '.conf/file_map')

    config_helpers.load_file_map(file_map_url, file_map_parser)
    # config_helpers.load_config(svn_authz_path, acl_parser)

    try:
        task_type_map = file_map_parser.get('file_map', task_type).lower()
        if task_type_map == 'base':
            if svn_service.is_svn_url(f'{blend_file_url}.blend'):
                svn_service.svn_delete(f'{blend_file_url}.blend', log_message=f'created {blend_file_url}.blend')
        elif task_type_map == 'none':
            pass
        else:
            if svn_service.is_svn_url(f'{blend_file_url}_{task_type_map}.blend'):
                svn_service.svn_delete(f'{blend_file_url}_{task_type_map}.blend', log_message=f'created {blend_file_url}_{task_type_map}.blend')
    except NoOptionError:
        if svn_service.is_svn_url(f'{blend_file_url}_{task_type}.blend'):
            svn_service.svn_delete(f'{blend_file_url}_{task_type}.blend', log_message=f'created {blend_file_url}_{task_type}.blend')
        # file_map_parser.set('file_map', task_type, task_type)
    
    # config_helpers.write_file_map(file_map_url, file_map_parser)
    # config_helpers.write_config(svn_authz_path, acl_parser)