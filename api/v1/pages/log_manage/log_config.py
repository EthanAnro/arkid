from arkid.core import routers, pages, actions

tag = 'log_config'
name = '日志配置'

page = pages.FormPage(tag = tag, name = name)

pages.register_front_pages(page)

router = routers.FrontRouter(
    path=tag,
    name=name,
    page=page,
    icon='log_config',
)

page.create_actions(
    init_action=actions.DirectAction(
        path="/api/v1/tenant/{tenant_id}/log_config/",
        method=actions.FrontActionMethod.GET,
    ),
    global_actions = {
        "confirm": actions.ConfirmAction(
            path="/api/v1/tenant/{tenant_id}/log_config/"
        ),
    }
)