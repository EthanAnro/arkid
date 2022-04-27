from typing import List
from ninja import ModelSchema, Query, Schema
from arkid.core.api import api, operation
from arkid.core.models import Tenant
from arkid.core.translation import gettext_default as _

class TenantListQueryIn(Schema):
    pass
        
class TenantListOut(ModelSchema):
    class Config:
        model = Tenant
        model_fields = ["name", "slug", "icon"]

@api.get("/tenants/", response=List[TenantListOut],tags=[_("租户管理")])
@operation(List[TenantListOut])
def get_tenant_list(request,query_data:TenantListQueryIn=Query(...)):
    """ 获取租户列表
    """

    tenants = Tenant.active_objects.all()

    return tenants

class TenantQueryIn(Schema):
    pass
        
class TenantOut(ModelSchema):
    class Config:
        model = Tenant
        model_fields = ["name"]

@api.get("/tenants/{id}/", response=TenantOut,tags=[_("租户管理")])
@operation(TenantOut)
def get_tenant(request, id: str,query_data:TenantQueryIn=Query(...)):
    """ 获取租户
    """
    tenant = Tenant.active_objects.get(id=id)
    return tenant

class TenantCreateIn(ModelSchema):
    class Config:
        model = Tenant
        model_fields = ["name"]

class TenantCreateQueryIn(Schema):
    pass
        
class TenantCreateOut(Schema):
    pass

@api.post("/tenants/",response=TenantCreateOut,tags=[_("租户管理")])
@operation(TenantCreateOut)
def create_tenant(request, tenant_id: str,data:TenantCreateIn,query_data:TenantCreateQueryIn=Query(...)):
    """ 创建租户
    """

    tenant = Tenant.valid_objects.create(**data)

    return {}

class TenantUpdateIn(ModelSchema):
    class Config:
        model = Tenant
        model_fields = ["name","slug","icon"]

class TenantUpdateQueryIn(Schema):
    pass
        
class TenantUpdateOut(Schema):
    pass

@api.put("/tenants/{id}/", response=TenantUpdateOut,tags=[_("租户管理")])
@operation(TenantUpdateOut)
def update_tenant(request, id: str,data:TenantUpdateIn,query_data:TenantUpdateQueryIn=Query(...)):
    """ 编辑租户
    """
    tenant = Tenant.active_objects.get(id=id)
    tenant.update(**data)
    return {}

class TenantDeleteQueryIn(Schema):
    pass
        
class TenantDeleteOut(Schema):
    pass

@api.delete("/tenants/{id}/", response=TenantDeleteOut, tags=[_("租户管理")])
@operation(TenantDeleteOut)
def delete_tenant(request, id: str, query_data:TenantDeleteQueryIn=Query(...)):
    """ 删除租户
    """
    tenant = Tenant.active_objects.get(id=id)
    tenant.delete()
    return {}


class TenantConfigQueryIn(Schema):
    pass
        
class TenantConfigOut(Schema):
    pass

@api.get("/tenants/{id}/config/", response=TenantConfigOut, tags=[_("租户管理")])
@operation(TenantConfigOut)
def get_tenant_config(request, id: str,query_data:TenantConfigQueryIn=Query(...)):
    """ 获取租户配置,TODO
    """
    return {}

class TenantConfigUpdateQueryIn(Schema):
    pass

class TenantConfigUpdateIn(Schema):
    pass
        
class TenantConfigUpdateOut(Schema):
    pass

@api.post("/tenants/{id}/config/", response=TenantConfigUpdateOut,tags=[_("租户管理")])
@operation(TenantConfigUpdateOut)
def update_tenant_config(request, id: str,data:TenantConfigUpdateIn,query_data:TenantConfigUpdateQueryIn=Query(...)):
    """ 编辑租户配置,TODO
    """
    return {}