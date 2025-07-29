from django.contrib import admin
from .models import UploadGroup, UploadFile, UploadGroup1, UploadFile1

# Inline for UploadFile (linked to UploadGroup)
class UploadFileInline(admin.TabularInline):
    model = UploadFile
    extra = 0
    readonly_fields = ['file']

# Inline for UploadFile1 (linked to UploadGroup1)
class UploadFile1Inline(admin.TabularInline):
    model = UploadFile1
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

@admin.register(UploadGroup1)
class UploadGroup1Admin(admin.ModelAdmin):
    list_display = ['id', 'user', 'note', 'created_at']
    search_fields = ['note', 'user__username']
    list_filter = ['user', 'created_at']
    inlines = [UploadFile1Inline]

@admin.register(UploadFile1)
class UploadFile1Admin(admin.ModelAdmin):
    list_display = ['id', 'group', 'file']
    search_fields = ['file']
