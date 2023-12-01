from django.contrib import admin
from .models import Tags, Blog, Comments
# Register your models here.

admin.site.register(Tags)
admin.site.register(Blog)
admin.site.register(Comments)