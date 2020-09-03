from django.contrib import admin
from .models import Post
from .models import SyainTable
from .models import KojinTourokuTable

admin.site.register(Post)
admin.site.register(SyainTable)
admin.site.register(KojinTourokuTable)