from blurbs.models import Blurb, Document, Email
from blurbs.utils import send_email
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.contrib.admin.models import LogEntry
import types

class DocumentInline(admin.TabularInline):
    model = Document
    readonly_fields = ['title']

class BlurbAdmin(admin.ModelAdmin):
    inlines = [DocumentInline]
    list_display = ['title', 'contact_info', 'date_submitted',
        'run_until', 'approved']
    list_filter = ['approved', 'run_until']
    readonly_fields = ['comments', 'approved']
    search_fields = ['title']
    fieldsets = [
        ('Blurb', {
            'fields': ['title', 'body', 'run_until', 'comments']
        }),
        ('Contact information', {
            'fields': ['name', 'email']
        }),
        ('Decision', {
            'fields': ['approved']
        }),
    ]
    actions = ['approve', 'reject']

    def approve(self, request, queryset):
        rows = queryset.update(approved=True)
        msg = '%s blurb%s' % (rows, 's' if rows > 1 else '')
        self.message_user(request, '%s successfully approved.' % msg)
        for blurb in [b for b in queryset if b.email]:
            send_email('Blurb approved', 'Approval', blurb.email, blurb=blurb)
    approve.short_description = 'Approve selected blurbs'

    def reject(self, request, queryset):
        rows = queryset.count()
        msg = '%s blurb%s' % (rows, 's' if rows > 1 else '')
        self.message_user(request, '%s successfully rejected.' % msg)
        for blurb in [b for b in queryset if b.email]:
            send_email('Blurb rejected', 'Rejection', blurb.email, blurb=blurb)
        queryset.delete()
    reject.short_description = 'Reject (and delete) selected blurbs'

class EmailAdmin(admin.ModelAdmin):
    fields = ('body',)
    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.unregister(Group)
admin.site.unregister(Site)
admin.site.register(Blurb, BlurbAdmin)
admin.site.register(Email, EmailAdmin)

# unbelievably hacky way to disable admin logging
def no_op(self, *args, **kwargs): return
LogEntry.objects.log_action = types.MethodType(no_op, LogEntry.objects)
