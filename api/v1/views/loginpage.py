from enum import Enum
from logging.config import listen
from typing import Any, Dict, Optional, List
from pydantic import Field
from ninja import Schema, Query, ModelSchema
from arkid.core.event import Event, register_event, dispatch_event
from arkid.core.api import api, operation
from arkid.core.models import Tenant
from arkid.core.extension.auth_factor import AuthFactorExtension
from arkid.core.translation import gettext_default as _
from arkid.core.event import CREATE_LOGIN_PAGE_AUTH_FACTOR, CREATE_LOGIN_PAGE_RULES
from arkid.common.logger import logger
from arkid.extension.models import TenantExtensionConfig
from arkid.core.extension.external_idp import ExternalIdpExtension


class ButtonRedirectSchema(Schema):
    url: str = Field(title=_('URL', '重定向地址'))
    params: Optional[dict] = Field(title=_('params', '重定向参数'))


class ButtonHttpSchema(Schema):
    url: str = Field(title=_('url', 'http请求地址'))
    method: str = Field(title=_('method', 'http请求方法'))
    params: Optional[dict] = Field(title=_('params', 'http请求参数'))


class ButtonAgreementSchema(Schema):
    title: str = Field(title=_('title', '标题'))
    content: str = Field(title=_('content', '内容'))


class ButtonSchema(Schema):
    prepend: Optional[str] = Field(title=_('prepend', '前置文字'))
    title: Optional[str] = Field(title=_('title', '标签文字'))
    tooltip: Optional[str] = Field(title=_('tooltip', '提示文字'))
    long: Optional[bool] = Field(title=_('long button', '是否为长按钮'))
    img: Optional[str] = Field(title=_('image url', '图片地址'))
    gopage: Optional[str] = Field(title=_('gopage', '跳转的页面名字'))
    redirect: Optional[ButtonRedirectSchema] = Field(title=_('redirect', '重定向'))
    http: Optional[ButtonHttpSchema] = Field(title=_('http', 'http请求'))
    delay: Optional[int] = Field(title=_('delay', '点击后延时（单位：秒）'))
    agreement: Optional[ButtonAgreementSchema] = Field(title=_('agreement', '隐私声明'))


class LOGIN_FORM_ITEM_TYPES(str, Enum):
    text = _('text', '普通文本框')
    password = _('password', '密码')
    checkbox = _('checkbox', '复选框')
    hidden = _('hidden', '隐藏')


class LoginFormItemSchema(Schema):
    value: Any
    type: LOGIN_FORM_ITEM_TYPES = Field(title=_('type', '种类'))
    placeholder: Optional[str] = Field(title=_('placeholder', '文字提示'))
    name: str = Field(title=_('name', '名字'))
    append: Optional[ButtonSchema] = Field(title=_('append', '扩展按钮'))
    http: Optional[ButtonHttpSchema] = Field(title=_('http', 'http请求'))
    content: Optional[str] = Field(title=_('content', '内容'))


class LoginFormSchema(Schema):
    label: str = Field(title=_('label', '表单名'))
    items: List[LoginFormItemSchema] = Field(title=_('items', '表单项'))
    submit: ButtonSchema = Field(title=_('submit', '表单提交'))


class LoginPageExtendSchema(Schema):
    title: Optional[str] = Field(title=_('title', '页面扩展标题'))
    buttons: Optional[List[ButtonSchema]] = Field(title=_('buttons', '扩展按钮'))


class LoginPageSchema(Schema):
    name: str = Field(title=_('page name', '页面名字'))
    forms: List[LoginFormSchema] = Field(title=_('forms', '表单'))
    bottoms: Optional[List[ButtonSchema]] = Field(title=_('bottoms', '表单下按钮'))
    extend: Optional[LoginPageExtendSchema] = Field(title=_('extend', '扩展'))


class LoginPageTenantSchema(ModelSchema):
    class Config:
        model = Tenant
        model_fields = ['id', 'name', 'slug', 'icon']
        # validate = False
        
    is_platform_tenant:bool = Field(
        title=_("是否是平台租户")
    )

class LoginPageOut(Schema):
    data: Dict[str, Optional[LoginPageSchema]]
    tenant: LoginPageTenantSchema


@api.get(
    "/tenant/{tenant_id}/login_page/", response=LoginPageOut, tags=['登录与注册'], auth=None
)
@operation(LoginPageOut)
def login_page(request, tenant_id: str):
    tenant = request.tenant
    login_pages = []
    responses = dispatch_event(
        Event(tag=CREATE_LOGIN_PAGE_AUTH_FACTOR, tenant=tenant, request=request)
    )
    for useless, response in responses:
        logger.info(response)
        login_pages.append(response)

    dispatch_event(
        Event(
            tag=CREATE_LOGIN_PAGE_RULES,
            tenant=tenant,
            request=request,
            data=login_pages,
        )
    )

    data = {}
    for login_page, ext in login_pages:

        if not login_page:
            continue

        for confg_data in login_page.values():
            for k, v in confg_data.items():
                if not data.get(k):
                    data[k] = v
                else:
                    if not data[k].get('bottoms'):
                        data[k]['bottoms'] = v.get('bottoms', [])
                    else:
                        data[k]['bottoms'].extend(v.get('bottoms', []))
                    if not data[k].get('forms'):
                        data[k]['forms'] = v.get('forms', [])
                    else:
                        data[k]['forms'].extend(v.get('forms', []))
                    if not data[k].get('extend'):
                        data[k]['extend'] = v.get('extend') if v.get('extend') else None
                    else:
                        data[k]['extend']['buttons'].extend(
                            v.get('extend', {}).get('buttons', [])
                        )
                if not data[k].get('name'):
                    data[k]['name'] = k

    if data.get(AuthFactorExtension.RESET_PASSWORD):
        if len(data.get(AuthFactorExtension.RESET_PASSWORD)['forms']) > 0:
            bottom = {
                "label": _("忘记密码"),
                "title": _("忘记密码"),
                "gopage": AuthFactorExtension.RESET_PASSWORD,
            }
            data[AuthFactorExtension.LOGIN]['bottoms'].insert(0, bottom)

        bottom = {
            "prepend": _("已有账号，"),
            "label": _("立即登录"),
            "title": _("立即登录"),
            "gopage": AuthFactorExtension.LOGIN,
        }
        data[AuthFactorExtension.RESET_PASSWORD]['bottoms'].insert(0, bottom)

    if data.get(AuthFactorExtension.REGISTER):
        bottom = {
            "prepend": _("还没有账号，"),
            "label": _("立即注册"),
            "title": _("立即注册"),
            "gopage": AuthFactorExtension.REGISTER,
        }
        data[AuthFactorExtension.LOGIN]['bottoms'].insert(0, bottom)
        bottom = {
            "prepend": _("已有账号，"),
            "label": _("立即登录"),
            "title": _("立即登录"),
            "gopage": AuthFactorExtension.LOGIN,
        }
        data[AuthFactorExtension.REGISTER]['bottoms'].insert(0, bottom)

    if data.get(AuthFactorExtension.REGISTER) and data.get(
        AuthFactorExtension.RESET_PASSWORD
    ):
        bottom = {
            "prepend": _("还没有账号，"),
            "label": _("立即注册"),
            "title": _("立即注册"),
            "gopage": AuthFactorExtension.REGISTER,
        }
        data[AuthFactorExtension.RESET_PASSWORD]['bottoms'].insert(0, bottom)

    return {
        'tenant': tenant,
        'data': data,
    }
