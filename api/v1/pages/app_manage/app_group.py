from arkid.core import routers, pages, actions
from arkid.core.translation import gettext_default as _

tag = 'app_group'
name = '应用分组'


page = pages.TreePage(tag=tag,name=name)
group_apps_page = pages.TablePage(name=_("组内应用"))
edit_apps_page = pages.TablePage(name=_("更新组内应用"))
edit_page = pages.FormPage(name=_("编辑应用分组"))


pages.register_front_pages(page)
pages.register_front_pages(group_apps_page)
pages.register_front_pages(edit_apps_page)
pages.register_front_pages(edit_page)

router = routers.FrontRouter(
    path=tag,
    name=name,
    page=page,
    icon='app_group',
)

page.create_actions(
    init_action=actions.DirectAction(
        path='/api/v1/tenant/{tenant_id}/app_groups/',
        method=actions.FrontActionMethod.GET,
    ),
    global_actions={
        'create':actions.CreateAction(
            path='/api/v1/tenant/{tenant_id}/app_groups/'
        )
    },
    local_actions={
        "edit": actions.EditAction(
            page=edit_page,
        ),
        "delete": actions.DeleteAction(
            path="/api/v1/tenant/{tenant_id}/app_groups/{id}/",
        )
    },
    node_actions=[
        actions.DirectAction(
            path='/api/v1/tenant/{tenant_id}/app_groups/?parent_id={id}',
            method=actions.FrontActionMethod.GET,
        ),
        actions.CascadeAction(
            page=group_apps_page
        )
    ]
)

group_apps_page.create_actions(
    init_action=actions.DirectAction(
        path='/api/v1/tenant/{tenant_id}/app_groups/{app_group_id}/apps/',
        method=actions.FrontActionMethod.GET
    ),
    global_actions={
        "update":actions.OpenAction(
            name=_("添加应用"),
            page=edit_apps_page,
        )
    },
    local_actions={
        "delete":actions.DeleteAction(
            path="/api/v1/tenant/{tenant_id}/app_groups/{app_group_id}/apps/{id}/",
            icon="icon-delete",
        )
    },
)


edit_apps_page.create_actions(
    init_action=actions.DirectAction(
        path='/api/v1/tenant/{tenant_id}/app_groups/{app_group_id}/exclude_apps/',
        method=actions.FrontActionMethod.GET,
    ),
    select=True,
    global_actions={
       'confirm': actions.ConfirmAction(
            path="/api/v1/tenant/{tenant_id}/app_groups/{app_group_id}/apps/"
        ),
    }
)


edit_page.create_actions(
    init_action=actions.DirectAction(
        path='/api/v1/tenant/{tenant_id}/app_groups/{id}/',
        method=actions.FrontActionMethod.GET
    ),
    global_actions={
       'confirm': actions.ConfirmAction(
            path="/api/v1/tenant/{tenant_id}/app_groups/{id}/"
        ),
    }
)
