from django.contrib import admin
from .models import UploadGroup, UploadFile

class UploadFileInline(admin.TabularInline):
    model = UploadFile
    extra = 0
    readonly_fields = ['file']

@admin.register(UploadGroup)
class UploadGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'note', 'created_at']
    search_fields = ['note', 'user__username']
    list_filter = ['user', 'created_at']
    inlines = [UploadFileInline]

@admin.register(UploadFile)
class UploadFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'file']
    search_fields = ['file']
