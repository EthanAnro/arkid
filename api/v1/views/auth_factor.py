from distutils.command.build_ext import extension_name_re
from distutils.command.config import config
from typing import List
from ninja import Field, ModelSchema, Schema
from ninja.pagination import paginate
from arkid.core.api import api, operation
from arkid.core.constants import *
from arkid.core.translation import gettext_default as _
from arkid.core.extension.auth_factor import AuthFactorExtension
from arkid.extension.models import Extension, TenantExtensionConfig
from arkid.core.error import ErrorCode, ErrorDict
from api.v1.schema.auth_factor import AuthFactorCreateIn, AuthFactorCreateOut, AuthFactorDeleteOut, AuthFactorListItemOut, AuthFactorListOut, AuthFactorOut, AuthFactorUpdateIn, AuthFactorUpdateOut
from arkid.core.pagenation import CustomPagination

@api.get("/tenant/{tenant_id}/auth_factors/", response=List[AuthFactorListItemOut], tags=[_("认证因素")])
@operation(List[AuthFactorListItemOut], roles=[TENANT_ADMIN, PLATFORM_ADMIN])
@paginate(CustomPagination)
def get_auth_factors(request, tenant_id: str,order:str=None):
    """ 认证因素列表
    """
    extensions = Extension.active_objects.filter(
        type=AuthFactorExtension.TYPE)
    configs = TenantExtensionConfig.active_objects.filter(
        tenant__id=tenant_id, extension__in=extensions)
    
    if order:
        configs = configs.order_by(order)
    
    configs = configs.all()
    
    return [
        {
            "id": config.id.hex,
            "type": config.type,
            "name": config.name,
            "extension_name": config.extension.name,
            "extension_package": config.extension.package,
        } for config in configs
    ]


@api.get("/tenant/{tenant_id}/auth_factors/{id}/", response=AuthFactorOut, tags=["认证因素"])
@operation(AuthFactorOut, roles=[TENANT_ADMIN, PLATFORM_ADMIN])
def get_auth_factor(request, tenant_id: str, id: str):
    """ 获取认证因素
    """
    config = TenantExtensionConfig.active_objects.get(
        tenant__id=tenant_id,
        id=id
    )
    return {
        "data": {
            "id": config.id.hex,
            "type": config.type,
            "package": config.extension.package,
            "name": config.name,
            "config": config.config
        }
    }


@api.post("/tenant/{tenant_id}/auth_factors/", response=AuthFactorCreateOut, tags=["认证因素"])
@operation(AuthFactorCreateOut, roles=[TENANT_ADMIN, PLATFORM_ADMIN])
def create_auth_factor(request, tenant_id: str, data: AuthFactorCreateIn):
    """ 创建认证因素
    """
    config = TenantExtensionConfig()
    config.tenant = request.tenant
    config.extension = Extension.active_objects.get(package=data.package)
    config.config = data.config.dict()
    config.name = data.dict()["name"]
    config.type = data.type
    config.save()
    
    return ErrorDict(ErrorCode.OK)


@api.post("/tenant/{tenant_id}/auth_factors/{id}/", response=AuthFactorUpdateOut, tags=["认证因素"])
@operation(AuthFactorUpdateOut, roles=[TENANT_ADMIN, PLATFORM_ADMIN])
def update_auth_factor(request, tenant_id: str, id: str, data: AuthFactorUpdateIn):
    """ 编辑认证因素
    """
    config = TenantExtensionConfig.active_objects.get(
        tenant__id=tenant_id, id=id)
    for attr, value in data.dict().items():
        if attr == "id":
            continue
        setattr(config, attr, value)
    config.save()
    return ErrorDict(ErrorCode.OK)


@api.delete("/tenant/{tenant_id}/auth_factors/{id}/", response=AuthFactorDeleteOut, tags=["认证因素"])
@operation(AuthFactorDeleteOut, roles=[TENANT_ADMIN, PLATFORM_ADMIN])
def delete_auth_factor(request, tenant_id: str, id: str):
    """ 删除认证因素
    """
    config = TenantExtensionConfig.active_objects.get(
        tenant__id=tenant_id, id=id
    )
    config.delete()
    return ErrorDict(ErrorCode.OK)
