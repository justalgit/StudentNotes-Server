from django.contrib import admin
import main.models

admin.site.register(main.models.User)
admin.site.register(main.models.Group)
admin.site.register(main.models.Event)
admin.site.register(main.models.Request)
admin.site.register(main.models.UserGroupRelation)
