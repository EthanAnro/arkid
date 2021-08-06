from openapi.utils import extend_schema_tags

tag = 'extension'
path = tag
name = '插件配置'

extend_schema_tags(
    tag,
    name,
    {
        'type':'table_page',
        'init': {
            'path': '/api/v1/tenant/{parent_lookup_tenant}/extension/',
            'method': 'get'
        },
        'global': {
            'create': {
                'tag': 'extension.create'
            }
        },
        'local': {
            'update': {
                'tag': 'extension.update'
            },
            'delete': {
                'path': '/api/v1/tenant/{parent_lookup_tenant}/extension/{id}/',
                'method': 'delete'
            }
        }
    }
)

extension_create_tag = 'extension.create'
extension_create_name = '创建插件'

extend_schema_tags(
    extension_create_tag,
    extension_create_name,
    {
        'type': 'form_page',
        'init': {
            'path': '/api/v1/tenant/{parent_lookup_tenant}/extension/',
            'method': 'post'
        },
        'global': {
            'create': {
                'path': '/api/v1/tenant/{parent_lookup_tenant}/extension/',
                'method': 'post'
            }
        }
    }
)

extension_update_tag = 'extension.update'
extension_update_name = '编辑插件'

extend_schema_tags(
    extension_update_tag,
    extension_update_name,
    {
        'type': 'form_page',
        'init': {
            'path': '/api/v1/tenant/{parent_lookup_tenant}/extension/{id}/',
            'method': 'get'
        },
        'global': {
            'update': {
                'path': '/api/v1/tenant/{parent_lookup_tenant}/extension/{id}/',
                'method': 'put'
            }
        }
    }
)