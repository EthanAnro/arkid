import json
from datetime import datetime
from pydantic import UUID4
from typing import Optional, List
from ninja import Field, Schema
from arkid.core.api import GlobalAuth, operation
from arkid.core.constants import *
from arkid.core.extension import create_extension_schema
from arkid.core.translation import gettext_default as _
from arkid.config import get_app_config
from arkid.core.extension.logging import LoggingExtension
from arkid.core import pages,actions, routers
from ninja.pagination import paginate
from arkid.core.pagenation import CustomPagination
from arkid.core.schema import ResponseSchema
from arkid.core.models import User
from .models import Log, TenantLogConfig


class LogItemOut(Schema):

    id: UUID4
    created: datetime = Field(title=_("Time", "时间"))
    username: str = Field(title=_("username", "用户名"))
    ip_address: str = Field(title=_("IP Address", "IP地址"))
    method: str = Field(title=_("HTTP Action Type", "HTTP请求类型"))
    endpoint: str = Field(title=_("HTTP Rquest URL", "HTTP请求URL"))
    status_code: int = Field(title=_("HTTP Status Code", "HTTP状态码"))
    exec_time: str = Field(title=_("Excuete Time in Seconds", "执行时间(单位秒)"))

    @staticmethod
    def resolve_username(obj):
        if obj.user:
            return obj.user.username
        else:
            return ''

    @staticmethod
    def resolve_ip_address(obj):
        if obj.data:
            return obj.data.get("remote_address", "")
        else:
            return ''

    @staticmethod
    def resolve_method(obj):
        if obj.data:
            return obj.data.get("method", "")
        else:
            return ''

    @staticmethod
    def resolve_endpoint(obj):
        if obj.data:
            return obj.data.get("endpoint", "")
        else:
            return ''

    @staticmethod
    def resolve_status_code(obj):
        if obj.data:
            return obj.data.get("response_code", "")
        else:
            return 0

    @staticmethod
    def resolve_exec_time(obj):
        if obj.data:
            return str(obj.data.get("exec_time", "") / 1000)
        else:
            return ""

class LogDetailItemOut(LogItemOut):
    request_body: str = Field(title=_("Request Body", "请求内容"))
    response_body: str = Field(title=_("Response Body", "返回内容"))

    @staticmethod
    def resolve_request_body(obj):
        if obj.data:
            return obj.data.get("body_request", "")
        else:
            return ""

    @staticmethod
    def resolve_response_body(obj):
        if obj.data:
            return obj.data.get("body_response", "")
        else:
            return ""

class LogItemResponseOut(ResponseSchema):
    data: LogDetailItemOut

class LogListOut(ResponseSchema):
    data: List[LogItemOut]

class LogConfigSchema(Schema):
    log_retention_period: int = Field(title=_("Log Retention Days", "日志保存天数"))
    log_path: str = Field(title=_("Log Path", "获取日志路径"), readonly=True)

class LogConfigResponseOut(ResponseSchema):
    data: LogConfigSchema


class MysqlLoggingExtension(LoggingExtension):

    def load(self):
        self.register_extension_api()
        self.register_pages()
        super().load()

    def save(self, event, **kwargs):
        tenant = event.tenant
        request = event.request
        response = event.response
        user = request.user
        # AnonymousUser
        if not isinstance(user, User):
            user = None
        data = event.data
        # print("request and response logging data: ", data)
        try:
            is_tenant_admin = tenant.has_admin_perm(user)
        except Exception as e:
            is_tenant_admin = False
        
        Log.objects.create(
            tenant=tenant,
            user=user,
            is_tenant_admin=is_tenant_admin,
            data=data
        )

    def register_extension_api(self):
        self.log_detail_path = self.register_api(
            '/log/{id}/', 
            'GET', 
            self.get_log, 
            response=LogItemResponseOut, 
            tenant_path=True
        )

        self.user_log_path = self.register_api(
            '/user_log/', 
            'GET', 
            self.list_user_logs, 
            response=List[LogItemOut], 
            tenant_path=True
        )
        
        self.manager_log_path = self.register_api(
            '/manager_log/', 
            'GET', 
            self.list_manager_logs, 
            response=List[LogItemOut], 
            tenant_path=True
        )

        self.list_log_path = self.register_api(
            '/log/', 
            'GET', 
            self.list_logs, 
            response=List[LogItemOut], 
            tenant_path=True
        )

        self.get_log_config_path = self.register_api(
            '/log_config/', 
            'GET', 
            self.get_log_config, 
            response=LogConfigResponseOut, 
            tenant_path=True
        )

        self.update_log_config_path = self.register_api(
            '/log_config/', 
            'POST', 
            self.update_log_config, 
            response=LogConfigResponseOut, 
            tenant_path=True
        )

    def register_pages(self):
        from .log_pages import log_config, manager_log, user_log
        from api.v1.pages.log_manage import router

        self.register_front_pages([
            log_config.page, 
            manager_log.page, manager_log.detail_page,
            user_log.page, user_log.detail_page,
        ])

        self.register_front_routers(log_config.router, router)
        self.register_front_routers(manager_log.router, router)
        self.register_front_routers(user_log.router, router)

    @operation(roles=[TENANT_ADMIN, PLATFORM_ADMIN])
    def get_log(self, request, tenant_id:str, id: str):
        log = Log.active_objects.filter(tenant=request.tenant, id=id).first()
        return {"data": log}

    @operation(LogListOut, roles=[TENANT_ADMIN, PLATFORM_ADMIN])
    @paginate(CustomPagination)
    def list_user_logs(self, request, tenant_id:str):
        logs = Log.active_objects.filter(tenant=request.tenant, is_tenant_admin=False).order_by("-created")
        return logs

    @operation(LogListOut, roles=[TENANT_ADMIN, PLATFORM_ADMIN])
    @paginate(CustomPagination)
    def list_manager_logs(self, request, tenant_id:str):
        logs = Log.active_objects.filter(tenant=request.tenant, is_tenant_admin=True).order_by("-created")
        return logs

    @operation(LogListOut, roles=[TENANT_ADMIN, PLATFORM_ADMIN])
    @paginate(CustomPagination)
    def list_logs(self, request, tenant_id:str):
        logs = Log.active_objects.filter(tenant=request.tenant).order_by("-created")
        return logs

    @operation(roles=[TENANT_ADMIN, PLATFORM_ADMIN])
    def get_log_config(self, request, tenant_id: str):
        """ 获取日志配置
        """
        config, created = TenantLogConfig.active_objects.get_or_create(tenant=request.tenant)
        config.log_path = get_app_config().get_host() + self.list_log_path.replace('{tenant_id}', tenant_id)
        return {"data": config}

    @operation(roles=[TENANT_ADMIN, PLATFORM_ADMIN])
    def update_log_config(self, request, tenant_id: str, data: LogConfigSchema):
        """ 更新日志配置
        """
        config = TenantLogConfig.active_objects.filter(tenant=request.tenant).first()
        for attr, value in data.dict().items():
            if attr != 'log_path':
                setattr(config, attr, value)
        config.save()
        config.log_path = get_app_config().get_host() + self.list_log_path.replace('{tenant_id}', tenant_id)
        return {"data": config}

extension = MysqlLoggingExtension()