from ninja import Schema
from pydantic import Field
from ninja import ModelSchema
from django.db.models import Q
from arkid.core.models import App

from arkid.core.api import api, operation
from django.db import transaction
from ninja.pagination import paginate
from arkid.core.error import ErrorCode, ErrorDict
from typing import Union, Literal, List
from django.shortcuts import get_object_or_404
from arkid.core.translation import gettext_default as _
from arkid.core.event import APP_CONFIG_DONE, Event, register_event, dispatch_event
from arkid.core.constants import NORMAL_USER, TENANT_ADMIN, PLATFORM_ADMIN
from arkid.core.event import(
    CREATE_APP_CONFIG, UPDATE_APP_CONFIG, DELETE_APP,
    CREATE_APP, UPDATE_APP, SET_APP_OPENAPI_VERSION,
    APP_SYNC_PERMISSION,
)

import uuid

from arkid.core.pagenation import CustomPagination
from api.v1.schema.app import *


@api.get("/tenant/{tenant_id}/apps/", response=List[AppListItemOut], tags=['应用'])
@operation(AppListOut, roles=[TENANT_ADMIN, PLATFORM_ADMIN])
@paginate(CustomPagination)
def list_apps(request, tenant_id: str,order:str=None, category_id:str=None):
    '''
    app列表
    '''
    apps = App.expand_objects.filter(
        tenant_id=tenant_id,
        is_active=True,
        is_del=False
    )
    
    if category_id and category_id != "" and category_id != "0" and category_id != "-1":
        apps = apps.filter(arkstore_category_id=category_id)
    elif category_id == "-1":
        apps = apps.filter(arkstore_category_id=None, arkstore_app_id=None)
    if order:
        apps = apps.order_by(order)
    else:
        apps = apps.order_by('-created')
    # # 取得请求地址和方式
    # method = request.method
    # url = request.resolver_match.route
    # print('request url:{},method:{}'.format(url,method))

    # from arkid.core.perm.permission_data import PermissionData
    # pd = PermissionData()
    # pd.update_arkid_system_permission()
    return apps


@api.get("/tenant/{tenant_id}/open_apps/", response=List[AppListItemOut], tags=['应用'])
@operation(AppListOut, roles=[TENANT_ADMIN, PLATFORM_ADMIN])
@paginate(CustomPagination)
def list_open_apps(request, tenant_id: str):
    '''
    公开app列表
    '''
    apps = App.valid_objects.filter(
        entry_permission__is_open=True
    )
    return apps


@api.get("/tenant/{tenant_id}/all_apps/", response=List[AppListItemOut], tags=['应用'])
@operation(AppListOut, roles=[TENANT_ADMIN, PLATFORM_ADMIN])
@paginate(CustomPagination)
def list_all_apps(request, tenant_id: str):
    '''
    所有app列表
    '''
    apps = App.valid_objects.filter(
        Q(entry_permission__is_open=True)|Q(tenant_id=tenant_id)
    )
    return apps


@api.get("/tenant/{tenant_id}/all_apps_in_arkid/", response=AppListsOut, tags=['应用'])
@operation(AppListOut, roles=[TENANT_ADMIN, PLATFORM_ADMIN])
def all_apps_in_arkid(request, tenant_id: str, not_arkid: int=None):
    '''
    所有app列表(含arkid)
    '''
    apps = App.valid_objects.filter(
        Q(entry_permission__is_open=True)|Q(tenant_id=tenant_id)
    )
    items = []
    if not_arkid is None:
        items.append({
            'id': 'arkid',
            'name': 'arkid',
            'is_system': True,
        })
    for app in apps:
        items.append({
            'id': str(app.id),
            'name': app.name,
            'is_system': True,
        })
    return {'data':items}

@api.get("/tenant/{tenant_id}/apps/{id}/", response=AppOut, tags=['应用'])
@operation(AppOut, roles=[TENANT_ADMIN, PLATFORM_ADMIN])
def get_app(request, tenant_id: str, id: str):
    '''
    获取app
    '''
    # app = get_object_or_404(App.expand_objects, id=id, is_del=False,is_active=True)
    app = App.expand_objects.get(id=id)
    return {"data":app}


@api.get("/tenant/{tenant_id}/apps/{id}/read_secret/", response=AppReadSecretOut, tags=['应用'])
@operation(roles=[TENANT_ADMIN, PLATFORM_ADMIN])
def get_app_read_secret(request, tenant_id: str, id: str):
    '''
    获取应用秘钥
    '''
    from arkid.common.utils import generate_secret
    app = App.valid_objects.get(id=id)
    app.secret = generate_secret()
    app.save()
    return {"data": {"read_secret": app.secret}}

@api.get("/tenant/{tenant_id}/apps/{app_id}/openapi_version/", response=ConfigOpenApiVersionDataSchemaOut, tags=['应用'])
@operation(roles=[TENANT_ADMIN, PLATFORM_ADMIN])
def get_app_openapi_version(request, tenant_id: str, app_id: str):
    '''
    获取app的openapi地址和版本
    '''
    app = get_object_or_404(App, id=app_id, is_del=False)
    app_config = app.config.config

    from arkid.config import get_app_config as ac
    host = ac().get_frontend_host()

    result = {
        'version': app_config.get('version', ''),
        'openapi_uris': app_config.get('openapi_uris', ''),
        'sync_permission_uri': host+'/api/v1/apps/'+app_id+'/sync_permission/'
    }
    # from arkid.core.models import Tenant, User
    # from arkid.core.perm.permission_data import PermissionData
    # tenant, _ = Tenant.objects.get_or_create(
    #   slug='',
    #   name="平台租户",
    # )
    # auth_user, _ = User.objects.get_or_create(
    #     username="hanbin",
    #     tenant=tenant,
    # )
    # tenant.users.add(auth_user)
    # tenant.save()
    # permissiondata = PermissionData()
    # permissiondata.update_single_user_system_permission(tenant.id, auth_user.id)
    return {'data':result}


@api.post("/tenant/{tenant_id}/apps/{app_id}/openapi_version/", tags=['应用'])
@operation(roles=[TENANT_ADMIN, PLATFORM_ADMIN])
def set_app_openapi_version(request, tenant_id: str, app_id: str, data:ConfigOpenApiVersionSchemaOut):
    '''
    设置app的openapi地址和版本
    '''
    app = get_object_or_404(App, id=app_id, is_del=False)
    config = app.config
    app_config = config.config
    if data.version and data.openapi_uris:
        old_version = app_config.get('version', None)
        old_openapi_uris = app_config.get('openapi_uris', None)

        app_config['version'] = data.version
        app_config['openapi_uris'] = data.openapi_uris
        config.save()

        if old_version is None:
            # 只有版本或接口发生变化时才调用事件
            dispatch_event(Event(tag=SET_APP_OPENAPI_VERSION, tenant=request.tenant, request=request, data=app))
        elif data.version != old_version or data.openapi_uris != old_openapi_uris:
            # 只有版本或接口发生变化时才调用事件
            dispatch_event(Event(tag=SET_APP_OPENAPI_VERSION, tenant=request.tenant, request=request, data=app))
    return ErrorDict(ErrorCode.OK)

@api.delete("/tenant/{tenant_id}/apps/{id}/", tags=['应用'])
@operation(roles=[TENANT_ADMIN, PLATFORM_ADMIN])
def delete_app(request, tenant_id: str, id: str):
    '''
    删除app
    '''
    app = App.valid_objects.get(id=id)
    if app.config:
        dispatch_event(Event(tag=DELETE_APP, tenant=request.tenant, packages=app.config.extension.package,request=request, data=app))
    else:
        dispatch_event(Event(tag=DELETE_APP, tenant=request.tenant, request=request, data=app))
    app.delete()
    return ErrorDict(ErrorCode.OK)

@api.post("/tenant/{tenant_id}/apps/{id}/", tags=['应用'])
@operation(AppUpdateOut,roles=[TENANT_ADMIN, PLATFORM_ADMIN])
def update_app(request, tenant_id: str, id: str, data: AppUpdateIn):
    '''
    修改app
    '''
    app = App.valid_objects.get(id=id)
    for attr, value in data.dict().items():
        setattr(app, attr, value)
    app.save()
    dispatch_event(Event(tag=UPDATE_APP, tenant=request.tenant, request=request, data=app))
    return ErrorDict(ErrorCode.OK)

@api.post("/tenant/{tenant_id}/apps/{id}/config/", tags=['应用'])
@operation(roles=[TENANT_ADMIN, PLATFORM_ADMIN])
def set_app_config(request, tenant_id: str, id: str, data:AppProtocolConfigIn):
    '''
    配置应用协议
    '''
    app = get_object_or_404(App.active_objects, id=id)
    tenant = request.tenant
    config = app.config
    data = data.dict()
    data["app"] = app
    if config:
        # 更新应用协议配置
        results = dispatch_event(Event(tag=UPDATE_APP_CONFIG, tenant=tenant, request=request, data=data, packages=[data["package"]]))
        for func, (result, extension) in results:
            # 修改app信息
            if result:
                app.type = data["app_type"]
                app.package = data["package"]
                app.save()
                # 修改config
                extension.update_tenant_config(app.config.id, data["config"], app.name, data["app_type"])
                dispatch_event(Event(tag=APP_CONFIG_DONE, tenant=tenant, request=request, data=app, packages=[data["package"]]))
                break
    else:
        # 创建应用协议配置
        results = dispatch_event(Event(tag=CREATE_APP_CONFIG, tenant=tenant, request=request, data=data, packages=[data["package"]]))
        flag = False
        for func, (result, extension) in results:
            if result:
                flag = True
                # 创建config
                config = extension.create_tenant_config(tenant, data["config"], app.name, data["app_type"])
                # 创建app
                app.type = data["app_type"]
                app.package = data["package"]
                app.config = config
                app.save()
                # 创建app完成进行事件分发
                dispatch_event(Event(tag=APP_CONFIG_DONE, tenant=tenant, request=request, data=app, packages=[data["package"]]))
                break
        if flag is False:
            return ErrorDict(ErrorCode.PLUG_IN_NOT_HIRE)
    return ErrorDict(ErrorCode.OK)

@api.get("/tenant/{tenant_id}/apps/{id}/config/", response=AppProtocolConfigOut,tags=['应用'])
@operation(AppProtocolConfigOut, roles=[TENANT_ADMIN, PLATFORM_ADMIN])
def get_app_config(request, tenant_id: str, id: str):
    '''
    获取应用协议数据
    '''
    app = get_object_or_404(App.active_objects, id=id)
    result = {
        'id': app.id.hex,
        'name': app.name,
        'url': app.url,
        'logo': app.logo,
        'description': app.description,
        'type': app.type or 'OIDC',
        'app_type': app.type or 'OIDC',
        'package': app.package or "com.longgui.app.protocol.oidc",
        'config': app.config.config if app.config else {
            "skip_authorization":False,
            "redirect_uris":"",
            "client_type":"confidential",
            "grant_type":"authorization-code",
            "algorithm":"RS256",
            "client_id":"",
            "client_secret":"",
            "authorize":"",
            "token":"",
            "userinfo":"",
            "logout":""
        }
    }
    return {"data":result}


@api.get("/apps/{id}/sync_permission/", tags=['应用'], auth=None)
@operation(roles=[TENANT_ADMIN, PLATFORM_ADMIN])
def sync_app_permission(request, id: str):
    '''
    同步应用权限
    '''
    app = App.valid_objects.filter(id=id).first()
    if app:
        dispatch_event(Event(tag=APP_SYNC_PERMISSION, tenant=app.tenant, request=request, data=id))
    return ErrorDict(ErrorCode.OK)

@api.post("/tenant/{tenant_id}/apps/", tags=['应用'],response=CreateAppOut)
@operation(CreateAppOut, roles=[TENANT_ADMIN, PLATFORM_ADMIN])
def create_app(request, tenant_id: str, data:CreateAppIn):
    '''
    创建应用
    '''
    app = App.objects.create(tenant=request.tenant, url=data.url)
    for key,value in data.dict().items():
        setattr(app,key,value)
    app.save()
    dispatch_event(Event(tag=CREATE_APP, tenant=request.tenant, request=request, data=app))

    return ErrorDict(ErrorCode.OK)
