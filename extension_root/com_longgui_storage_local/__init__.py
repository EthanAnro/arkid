from pathlib import Path
from typing import Optional
import uuid
from django.urls import reverse
from ninja import Field
from arkid.core.extension import Extension, create_extension_schema
from arkid.core.event import SAVE_FILE
from arkid.core.translation import gettext_default as _
from arkid.config import get_app_config
from arkid.core.extension.storage import StorageExtension
from . import views

ProfileSchema = create_extension_schema(
    "LocalStorageProfileSchema",
    __file__,
    fields = [
        ('storage_path', Optional[str], Field(title=_("Storage Path", "存储路径"))),
    ]
)


class LocalStorageExtension(StorageExtension):

    def load(self):
        self.register_profile_schema(ProfileSchema)
        super().load()

    def save_file(self, file, f_key, *args, **kwargs):
        extension = self.model
        storage_path = extension.profile.get('storage_path','./storage/')
        
        p = Path(storage_path) / f_key

        if not p.parent.exists():
            p.parent.mkdir(parents=True)

        with open(p, 'wb') as fp:
            for chunk in file.chunks():
                fp.write(chunk)
                
    def resolve(self, f_key, tenant, *args, **kwargs):
        host = get_app_config().get_frontend_host()
        return f'{host}/api/v1/tenant/{tenant.id}/localstorage/{f_key}'
    
    


extension = LocalStorageExtension()