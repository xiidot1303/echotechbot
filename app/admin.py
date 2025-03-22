from django.contrib import admin
from django.urls import reverse, path
from app.views.promocode import *
from django.utils.html import format_html
from django.shortcuts import redirect

class Default(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

class PromoCodeAdmin(admin.ModelAdmin):
    change_list_template = 'admin/promocode/promocode_change_list.html'
    list_display = ['code', 'created_at', 'used']
    search_fields = ['code', 'used']

class UserPromoCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'promo_code', 'entered_at']
    search_fields = ['user__username', 'user__name', 'user__name', 'promo_code__code', 'id']
    list_filter = ['user']

class StatementAdmin(admin.ModelAdmin):
    list_display = ['bot_user', 'promocode', 'photo', 'confirmed', 'datetime', 'accept_button', 'cancel_button']
    search_fields = ['bot_user__username', 'bot_user__name', 'promocode__code', 'id']
    list_filter = ['confirmed', 'datetime']

    def accept_button(self, obj):
        if not obj.confirmed:
            return format_html(
                '<a class="btn btn-success" href="{}" title="Accept"><i class="fas fa-check"></i></a>',
                reverse('admin:accept_statement', args=[obj.pk])
            )
        return ""
    accept_button.short_description = ''

    def cancel_button(self, obj):
        if not obj.confirmed:
            return format_html(
                '<a class="btn btn-danger" href="{}" title="Cancel"><i class="fas fa-times"></i></a>',
                reverse('admin:cancel_statement', args=[obj.pk])
            )
        return ""
    cancel_button.short_description = ''

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('accept/<int:statement_id>/', self.admin_site.admin_view(self.accept_statement), name='accept_statement'),
            path('cancel/<int:statement_id>/', self.admin_site.admin_view(self.cancel_statement), name='cancel_statement'),
        ]
        return custom_urls + urls

    def accept_statement(self, request, statement_id):
        statement = self.get_object(request, statement_id)
        statement.confirmed = True
        statement.save()
        self.message_user(request, "Statement accepted successfully.")
        return redirect(request.META.get('HTTP_REFERER', '..'))

    def cancel_statement(self, request, statement_id):
        statement = self.get_object(request, statement_id)
        statement.delete()
        self.message_user(request, "Statement cancelled successfully.")
        return redirect(request.META.get('HTTP_REFERER', '..'))

admin.site.register(PromoCode, PromoCodeAdmin)
admin.site.register(UserPromoCode, UserPromoCodeAdmin)
admin.site.register(Statement, StatementAdmin)

admin.site.site_header = 'EcoTech'
admin.site.site_title = 'EcoTech Admin'