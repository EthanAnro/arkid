from enum import Enum
from uuid import UUID
from ninja import Field
from ninja import Schema
from ninja import ModelSchema
from typing import List, Optional
from arkid.core import pages,actions
from arkid.core.translation import gettext_default as _
from arkid.core.models import Permission, SystemPermission

select_app_page = pages.TreePage(select=True,name=_("选择应用"))

pages.register_front_pages(select_app_page)

select_app_page.create_actions(
    init_action=actions.DirectAction(
        path='/api/v1/tenant/{tenant_id}/apps/',
        method=actions.FrontActionMethod.GET
    )
)

class PermissionListSchemaOut(ModelSchema):

    app_id: UUID = Field(default=None)

    class Config:
        model = Permission
        model_fields = ['id', 'name', 'category', 'is_system']


class PermissionSchemaOut(Schema):
    permission_id: str


class PermissionCategory(str, Enum):
    entry = 'entry'
    api = 'api'
    data = 'data'
    group = 'group'
    ui = 'ui'
    other = 'other'

class PermissionCreateSchemaIn(ModelSchema):

    app_id: UUID = Field(
        field="id",
        page=select_app_page.tag,
        link="app",
        default=None,
        title=_("应用")
    )

    category: PermissionCategory = 'other'

    class Config:
        model = Permission
        model_fields = ['name']


class PermissionEditSchemaIn(ModelSchema):

    class Config:
        model = Permission
        model_fields = ['name', 'category']


class PermissionDetailSchemaOut(ModelSchema):

    app_id: UUID = Field(default=None)
    parent_id: UUID = Field(default=None)

    class Config:
        model = Permission
        model_fields = ['id', 'name', 'category']


class PermissionStrSchemaOut(Schema):
    result: str


class PermissionBatchSchemaIn(Schema):
    data: List[str]
