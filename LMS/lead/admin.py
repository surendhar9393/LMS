from django.contrib import admin
from .models import Lead, LeadUser, DocumentType, Document
from LMS.common.fsm_mixins import FSMTransitionMixin


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0
    fields = ('number', 'document_type', 'file')
    readonly_fields = fields


class LeadAdmin(FSMTransitionMixin, admin.ModelAdmin):
    fields = ('name', 'phone_number', 'status', 'age', 'occupation', 'income', 'city', 'source', 'action_owner',)
    list_display = fields
    inlines = [DocumentInline]
    fsm_field = ['status', ]
    readonly_fields = ('status',)
    list_filter = ['city', 'source', 'status']
    search_fields = ['city__name', 'name', 'phone_number']


admin.site.register(Lead, LeadAdmin)


class LeadUserAdmin(admin.ModelAdmin):
    fields = ('name', 'phone_number',)
    list_display = fields
    search_fields = ['name', 'phone_number']


admin.site.register(LeadUser, LeadUserAdmin)


class DocumentTypeAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = fields
    search_fields = ['name']


admin.site.register(DocumentType, DocumentTypeAdmin)


class DocumentAdmin(admin.ModelAdmin):
    fields = ('number', 'document_type', 'file')
    list_display = fields
    search_fields = ['name']


admin.site.register(Document, DocumentAdmin)
