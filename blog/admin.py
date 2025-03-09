from django.contrib import admin
from .models import CustomUser, Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'text')
    raw_id_fields = ('author',)
    date_hierarchy = 'created_at'
    ordering = ('created_at',)

admin.site.register(CustomUser)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
