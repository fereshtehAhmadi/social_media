from django.contrib import admin
from accounts.models import User, Validation, Request, Follower


admin.site.register(User)
admin.site.register(Validation)
admin.site.register(Request)
admin.site.register(Follower)
