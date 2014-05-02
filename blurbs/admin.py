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

    def _action(self, request, queryset, action, label, email):
        rows_affected = action()
        msg = '%s blurb%s' % (rows_affected, 's' if rows_affected > 1 else '')
        self.message_user(request, '%s successfully %s.' % (msg, label))
        for blurb in queryset:
            if blurb.email:
                send_email('Blurb %s' % label, email, blurb.email, blurb=blurb)

    def approve(self, request, queryset):
        self._action(request, queryset,
                     lambda: queryset.update(approved=True),
                     'approved', 'Approval')
    approve.short_description = 'Approve selected blurbs'

    def reject(self, request, queryset):
        self._action(request, queryset,
                     lambda: (queryset.count(), queryset.delete())[0],
                     'rejected', 'Rejection')
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
