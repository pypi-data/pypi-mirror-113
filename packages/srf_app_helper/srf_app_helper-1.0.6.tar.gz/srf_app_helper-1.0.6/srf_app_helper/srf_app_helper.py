"""
@Author：WangYuXiang
@E-mile：Hill@3io.cc
@CreateTime：2021/4/22 9:53
@DependencyLibrary：无
@MainFunction：无
@FileDoc： 
    app_helper.py
    文件说明
@ChangeHistory:
    datetime action why
    example:
    2021/4/22 9:53 change 'Fix bug'
        
"""
import json
import logging
import os
from functools import partial
from importlib import import_module

from sanic_plugin_toolkit import SanicPlugin

from sanic_rest_framework.constant import ALL_METHOD


def get_module_urls(module_path) -> list:
    """
    得到app中的urls
    :param module_path:
    :return:
    """
    return getattr(import_module('%s.urls' % module_path), 'urls')


def get_module_models(module_path):
    """
    得到app中的models
    :param module_path:
    :return:
    """
    return '%s.models' % module_path


def get_module_blueprint(module_path, module_name):
    """
    得到app的蓝图
    :param module_path:
    :param module_name:
    :return:
    """
    return getattr(import_module(module_path, module_name), module_name)


class AppsHelper(SanicPlugin):
    def __init__(self, apps_folder_path=None, expand_apps: dict = None, *args, **kwargs):
        """
        初始化
        :param apps_folder_path: apps文件地址，相对于调用方的相对地址
        :param expand_apps: 加载不存在于 apps_path 中的app
        {‘app_name’:{'module_path':'xxx.xx.xx','apps_path':os.path.join(os.getcwd(),'xxx','xxx','xx')}}
        """
        super(AppsHelper, self).__init__(*args, **kwargs)
        self.base_path = os.getcwd()
        self.apps_path = self.get_apps_folder_abs_path(apps_folder_path)
        self._expand_app = {} if expand_apps is None else expand_apps
        self.apps = self.get_apps()
        self.routers = {}
        self.models = {}

    def on_registered(self, context, reg, *args, **kwargs):
        """插件注册后进行加载"""
        info = partial(context.log, logging.INFO)
        info('Start load app.')
        for app_name, app_info in self.apps.items():
            info('{}{}{}'.format('-' * 15, app_name, '-' * 15))

            module_path = app_info['module_path']
            blueprint = get_module_blueprint(
                module_path=module_path, module_name=app_name)
            info('\t\tBlueprint finish')
            routes = get_module_urls(module_path)
            info('\t\tUrls finish')
            self.models[app_name] = [get_module_models(module_path)]
            info('\t\tModels finish')
            # 注册路由
            for route in routes:
                is_base = route.pop('is_base', False)
                if is_base:
                    self.add_route(context.app, route)
                else:
                    self.add_route(blueprint, route)
            info('\t\tRegistered route finish')
            context.app.blueprint(blueprint)
        info('Done')

    def get_apps_folder_abs_path(self, apps_path):
        """得到app文件夹的绝对路径"""
        if apps_path is None:
            return os.path.join(self.base_path, 'apps')
        return os.path.join(self.base_path, apps_path)

    def get_apps(self):
        """
        得到所有符合要求的App
        被认定为APP的必要条件
            存在 models.py
            存在 urls.py
            存在 __init__.py
        其中 __init__.py 内应该存在于 app_name 一致的蓝图
        """
        apps = {}
        folder_names = os.listdir(self.apps_path)
        for folder_name in folder_names:
            app_path = os.path.join(self.apps_path, folder_name)
            models_path = os.path.join(app_path, 'models.py')
            urls_path = os.path.join(app_path, 'urls.py')
            blueprint_path = os.path.join(app_path, '__init__.py')
            if all([os.path.isdir(app_path), os.path.exists(models_path), os.path.exists(urls_path),
                    os.path.exists(blueprint_path)]):
                apps[folder_name] = {
                    'module_path': 'apps.%s' % folder_name,
                    'apps_path': app_path,
                }
        apps.update(self._expand_app)
        return apps

    def add_route(self, spot, route):
        """为urls中的methods提供缺省参数"""
        if 'methods' not in route:
            route['methods'] = ALL_METHOD
        spot.add_route(**route)

    def get_permissions(self, file_name='permission.json'):
        """得到初始化的权限权限"""
        for app_name, app_info in self.apps.items():
            path = os.path.join(app_info['apps_path'], file_name)
            if not os.path.exists(path):
                continue
            with open(path, 'r', encoding='utf8') as f:
                permission_dict = json.loads(f.read())
                for classify_code, classify_info in permission_dict.items():
                    classify_name = classify_info['label']
                    permissions = classify_info['permissions']
                    for code, name in permissions.items():
                        yield code, name, classify_code, classify_name


apps_helper = AppsHelper()
__all__ = ['apps_helper', 'AppsHelper']
