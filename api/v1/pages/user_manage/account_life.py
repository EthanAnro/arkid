from arkid.core import routers, pages, actions
from arkid.core.translation import gettext_default as _

tag = 'account_life'
name = '账号生命周期'


page = pages.TablePage(tag=tag, name=name)
edit_page = pages.FormPage(name=_("编辑账号生命周期设置"))
create_page = pages.FormPage(name=_("创建一个新的账号生命周期设置"))

pages.register_front_pages(page)
pages.register_front_pages(edit_page)
pages.register_front_pages(create_page)

router = routers.FrontRouter(
    path=tag,
    name=name,
    page=page,
)

page.create_actions(
    init_action=actions.DirectAction(
        path='/api/v1/tenant/{tenant_id}/account_lifes/',
        method=actions.FrontActionMethod.GET,
    ),
    global_actions=[
        actions.CreateAction(
            page=create_page,
        )
    ],
    local_actions=[
        actions.EditAction(
            page=edit_page,
        ),
        actions.DeleteAction(
            path="/api/v1/tenant/{tenant_id}/account_lifes/{id}/",
        )
    ],
)

edit_page.create_actions(
    init_action=actions.DirectAction(
        path='/api/v1/tenant/{tenant_id}/account_lifes/{id}/',
        method=actions.FrontActionMethod.GET
    ),
    global_actions=[
        actions.ConfirmAction(path="/api/v1/tenant/{tenant_id}/account_lifes/{id}/"),

    ]
)

create_page.create_actions(
    init_action=actions.DirectAction(
        path='/api/v1/tenant/{tenant_id}/account_lifes/',
        method=actions.FrontActionMethod.POST
    ),
    global_actions=[
        actions.ConfirmAction(
            path="/api/v1/tenant/{tenant_id}/account_lifes/",
        ),

    ]
)
