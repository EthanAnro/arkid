from openapi.utils import extend_schema_tags

tag = 'password'
path = tag
name = '密码管理'

extend_schema_tags(
    tag,
    name,
    {
        'type': 'table_page',
        'init': {
            'path': '/api/v1/tenant/{tenant_uuid}/password_complexity/',
            'method': 'get'
        },
        'global': {
            'create': {
                'tag': 'password.create'
            }
        },
        'local': {
            'update': {
                'tag': 'password.update'
            },
            'delete': {
                'path': '/api/v1/tenant/{tenant_uuid}/password_complexity/{complexity_uuid}/detail/',
                'method': 'delete'
            }
        }
    }
)

password_create_tag = 'password.create'
password_create_name = '创建新密码规则'

extend_schema_tags(
    password_create_tag,
    password_create_name,
    {
        'type': 'form_page',
        'init': {
            'path': '/api/v1/tenant/{tenant_uuid}/password_complexity/',
            'method': 'post'
        },
        'global': {
            'create': {
                'path': '/api/v1/tenant/{tenant_uuid}/password_complexity/',
                'method': 'post'
            }
        }
    }
)

password_update_tag = 'password.update'
password_update_name = '编辑密码规则'

extend_schema_tags(
    password_update_tag,
    password_update_name,
    {
        'type': 'form_page',
        'init': {
            'path': '/api/v1/tenant/{tenant_uuid}/password_complexity/{complexity_uuid}/detail/',
            'method': 'get'
        },
        'global': {
            'update': {
                'path': '/api/v1/tenant/{tenant_uuid}/password_complexity/{complexity_uuid}/detail/',
                'method': 'patch'
            }
        }
    }
)