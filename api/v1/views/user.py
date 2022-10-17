from email import message
from typing import Any, Dict, Optional, List
from django.shortcuts import get_object_or_404
from pydantic import Field
from ninja import Schema, Query, ModelSchema
from arkid.core.event import Event, register_event, dispatch_event
from arkid.core.api import api, operation
from arkid.core.models import Tenant, User
from arkid.core.translation import gettext_default as _
from arkid.core.event import CREATE_LOGIN_PAGE_AUTH_FACTOR, CREATE_LOGIN_PAGE_RULES
from arkid.common.logger import logger
from api.v1.schema.user import (
    UserCreateIn, UserCreateOut, UserDeleteOut,
    UserListItemOut, UserListOut, UserListQueryIn,
    UserOut, UserUpdateIn, UserUpdateOut,
    UserFieldsOut, UserPullOut, UserPullItemOut,
)
from arkid.core.error import ErrorCode, ErrorDict
from arkid.core.constants import NORMAL_USER, TENANT_ADMIN, PLATFORM_ADMIN
from arkid.core.pagenation import CustomPagination
from ninja.pagination import paginate
from django.utils import timezone

# ------------- 用户列表接口 --------------        
@api.get("/tenant/{tenant_id}/users/",response=List[UserListItemOut], tags=['用户'])
@operation(UserListOut,roles=[TENANT_ADMIN, PLATFORM_ADMIN])
@paginate(CustomPagination)
def user_list(request, tenant_id: str, query_data: UserListQueryIn=Query(...)):
    from arkid.core.perm.permission_data import PermissionData
    users = User.expand_objects.filter(tenant_id=tenant_id, is_del=False)
    if query_data.username:
        users = users.filter(username__icontains=query_data.username)
    if query_data.order:
        users = users.order_by(query_data.order)
    login_user = request.user
    tenant = request.tenant
    pd = PermissionData()
    users = pd.get_manage_all_user(login_user, tenant, users)
    
    for user in users:
        user['created'] = timezone.localtime(user['created']).strftime('%Y-%m-%d %H:%M:%S')
    
    return list(users)



@api.get("/tenant/{tenant_id}/user_no_super/",response=UserListOut, tags=['用户'])
@operation(UserListOut,roles=[TENANT_ADMIN, PLATFORM_ADMIN])
# @paginate(CustomPagination)
def user_list_no_super(request, tenant_id: str):
    from arkid.core.perm.permission_data import PermissionData
    super_user_id = User.valid_objects.order_by('created').first().id
    users = User.valid_objects.filter(tenant_id=tenant_id).exclude(id=super_user_id)
    # 如果当前登录的用户不是管理员，需要根据用户所拥有的分组进行区分
    login_user = request.user
    tenant = request.tenant
    pd = PermissionData()
    users = pd.get_manage_all_user(login_user, tenant, users)
    return {"data": list(users.all())}

# ------------- 创建用户接口 --------------
@api.post("/tenant/{tenant_id}/users/",response=UserCreateOut, tags=['用户'])
@operation(UserCreateOut,roles=[TENANT_ADMIN, PLATFORM_ADMIN])
def user_create(request, tenant_id: str,data:UserCreateIn):
    tenant = request.tenant
    # user = User.expand_objects.create(tenant=request.tenant,**data.dict())
    if User.objects.filter(tenant=tenant, username=data.username).count():
        return ErrorDict(
            ErrorCode.USERNAME_EXISTS_ERROR
        )
    
    user = User.objects.create(tenant=tenant, username=data.username)
    for key,value in data.dict().items():
        if key=='username':
            continue
        if value:
            setattr(user,key,value)
    user.save()

    tenant.users.add(user)
    tenant.save()
    return {"data":{"user":user.id.hex}}

@api.get("/tenant/{tenant_id}/users/pull/",response=List[UserPullItemOut], tags=['用户'])
@operation(UserPullOut,roles=[PLATFORM_ADMIN])
@paginate(CustomPagination)
def user_pull(request, tenant_id: str):
    '''
    拉取用户
    '''
    users = User.objects.filter(
        tenant_id=tenant_id
    ).order_by('created')
    return users

# ------------- 删除用户接口 --------------    
@api.delete("/tenant/{tenant_id}/users/{id}/",response=UserDeleteOut, tags=['用户'])
@operation(UserDeleteOut,roles=[TENANT_ADMIN, PLATFORM_ADMIN])
def user_delete(request, tenant_id: str,id:str):
    user = get_object_or_404(User.valid_objects,tenant=request.tenant, id=id)
    user.delete()
    return {"error":ErrorCode.OK.value}
        
# ------------- 更新用户接口 --------------
@api.post("/tenant/{tenant_id}/users/{id}/",response=UserUpdateOut, tags=['用户'])
@operation(UserUpdateOut,roles=[TENANT_ADMIN, PLATFORM_ADMIN])
def user_update(request, tenant_id: str,id:str, data:UserUpdateIn):

    user = User.objects.get(id=id)
    for key,value in data.dict().items():
        setattr(user,key,value)
    user.save()
    return {"error":ErrorCode.OK.value}

# ------------- 用户扩展字段列表 --------------
@api.get("/tenant/{tenant_id}/user_fields/", response=UserFieldsOut, tags=['用户'], auth=None)
def user_fields(request, tenant_id: str):
    from arkid.core.expand import field_expand_map
    table_name = User._meta.db_table
    items = []
    verbose_names = []
    if table_name in field_expand_map:
        field_expands = field_expand_map.get(table_name,{})
        for table, field,extension_name,extension_model_cls,extension_table,extension_field  in field_expands:
            for field_item in extension_model_cls._meta.fields:
                verbose_name = field_item.verbose_name
                field_name = field_item.name
                if field_name == field:
                    if verbose_name not in verbose_names:
                        items.append({
                            'id': field,
                            'name': verbose_name,
                        })
                        verbose_names.append(verbose_name)
                    break
    return {"data":items}

# ------------- 获取用户接口 --------------        
@api.get("/tenant/{tenant_id}/users/{id}/",response=UserOut, tags=['用户'])
@operation(UserOut,roles=[TENANT_ADMIN, PLATFORM_ADMIN])
def get_user(request, tenant_id: str,id:str):
    id = id.replace("-", "")
    user = User.expand_objects.get(id=id)
    return {"data":user}
