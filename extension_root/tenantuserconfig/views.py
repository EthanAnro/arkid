from drf_spectacular.utils import extend_schema
from django.urls import reverse
from rest_framework.generics import GenericAPIView
from .provider import TenantUserConfigIdpProvider
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticated
from rest_framework_expiring_authtoken.authentication import ExpiringTokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from openapi.utils import extend_schema
from extension_root.tenantuserconfig.serializers import(
    TenantUserConfigSerializer,
)
from extension_root.tenantuserconfig.models import TenantUserConfig
from tenant.models import Tenant


@extend_schema(roles=['tenant admin', 'global admin'], tags=['tenant'])
class TenantUserConfigView(generics.RetrieveUpdateAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication]

    serializer_class = TenantUserConfigSerializer

    def get_object(self):
        tenant_uuid = self.kwargs['tenant_uuid']
        tenant = Tenant.active_objects.get(uuid=tenant_uuid)
        config = TenantUserConfig.active_objects.filter(
            tenant=tenant
        ).first()
        if config is None:
            config = TenantUserConfig()
            config.tenant = tenant
            config.data = {
                'is_edit_fields': [
                    {'name':'用户名', 'is_edit': True},
                    {'name':'姓名', 'is_edit': True},
                    {'name':'电话', 'is_edit': True},
                    {'name':'邮箱', 'is_edit': True},
                    {'name':'职位', 'is_edit': True},
                ],
                'is_logout': False,
                'is_look_token': False,
                'is_manual_overdue_token': False,
                'is_logging_ip': True,
                'is_logging_device': True,
            }
            config.save()
        return config