from django.contrib import admin
from .models import(
    User, UserGroup, Tenant,
    App, AppGroup, Permission,
    ExpiringToken, GroupPermissionResult,
    UserPermissionResult, SystemPermission, ApproveAction,
    ApproveRequest, AppPermissionResult,
)

admin.site.register(Tenant)
admin.site.register(User)
admin.site.register(UserGroup)
admin.site.register(App)
admin.site.register(AppGroup)
admin.site.register(Permission)
admin.site.register(ApproveAction)
admin.site.register(ApproveRequest)
admin.site.register(ExpiringToken)
admin.site.register(SystemPermission)
admin.site.register(UserPermissionResult)
admin.site.register(GroupPermissionResult)
admin.site.register(AppPermissionResult)
