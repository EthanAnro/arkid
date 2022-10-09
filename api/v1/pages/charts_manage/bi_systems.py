from arkid.core import routers, pages, actions
from arkid.core.translation import gettext_default as _

tag = 'bi_system'
name = '分析系统'


page = pages.TablePage(tag=tag, name=name)
edit_page = pages.FormPage(name=_("编辑BI系统"))


pages.register_front_pages(page)
pages.register_front_pages(edit_page)


router = routers.FrontRouter(
    path=tag,
    name=name,
    page=page,
    icon='bi_system',
)

page.create_actions(
    init_action=actions.DirectAction(
        path='/api/v1/tenant/{tenant_id}/bi_systems/',
        method=actions.FrontActionMethod.GET,
    ),
    global_actions={
        'create': actions.CreateAction(
            path='/api/v1/tenant/{tenant_id}/bi_systems/',
        )
    },
    local_actions={
        "edit": actions.EditAction(
            page=edit_page,
        ),
        "delete":actions.DeleteAction(
            path="/api/v1/tenant/{tenant_id}/bi_systems/{id}/",
        )
    },
)

edit_page.create_actions(
    init_action=actions.DirectAction(
        path='/api/v1/tenant/{tenant_id}/bi_systems/{id}/',
        method=actions.FrontActionMethod.GET
    ),
    global_actions={
       'confirm': actions.ConfirmAction(
            path="/api/v1/tenant/{tenant_id}/bi_systems/{id}/"
        ),
    }
)


