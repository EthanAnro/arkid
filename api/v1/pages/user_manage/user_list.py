from arkid.core import routers, pages, actions
from arkid.core.translation import gettext_default as _

tag = 'user_list'
name = '用户列表'


page = pages.TablePage(tag=tag, name=name)
edit_page = pages.FormPage(name=_("编辑用户"))


pages.register_front_pages(page)
pages.register_front_pages(edit_page)


router = routers.FrontRouter(
    path=tag,
    name=name,
    icon='user_list',
    page=page,
)

page.create_actions(
    init_action=actions.DirectAction(
        path='/api/v1/tenant/{tenant_id}/users/',
        method=actions.FrontActionMethod.GET,
    ),
    global_actions={
        'create': actions.CreateAction(
            path='/api/v1/tenant/{tenant_id}/users/',
        ),
        "order_username":actions.OrderAction(
            up="/api/v1/tenant/{tenant_id}/users/?order=username",
            down="/api/v1/tenant/{tenant_id}/users/?order=-username",
            method=actions.FrontActionMethod.GET,
            order_parm="username"
        ),
        "order_created":actions.OrderAction(
            up="/api/v1/tenant/{tenant_id}/users/?order=created",
            down="/api/v1/tenant/{tenant_id}/users/?order=-created",
            method=actions.FrontActionMethod.GET,
            order_parm="created"
        )
    },
    local_actions={
        "edit": actions.EditAction(
            page=edit_page,
        ),
        "delete":actions.DeleteAction(
            path="/api/v1/tenant/{tenant_id}/users/{id}/",
        )
    },
)

edit_page.create_actions(
    init_action=actions.DirectAction(
        path='/api/v1/tenant/{tenant_id}/users/{id}/',
        method=actions.FrontActionMethod.GET
    ),
    global_actions={
       'confirm': actions.ConfirmAction(
            path="/api/v1/tenant/{tenant_id}/users/{id}/"
        ),
    }
)


