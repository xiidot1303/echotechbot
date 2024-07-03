from django.contrib import admin
from django.urls import reverse, path
from app.views.promocode import *

class Default(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

class PromoCodeAdmin(admin.ModelAdmin):
    change_list_template = 'admin/promocode/promocode_change_list.html'
    list_display = ['code', 'created_at', 'used']
    search_fields = ['code', 'used']

class UserPromoCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'promo_code', 'entered_at']
    search_fields = ['user__username', 'promo_code__code']


admin.site.register(PromoCode, PromoCodeAdmin)
admin.site.register(UserPromoCode, UserPromoCodeAdmin)

admin.site.site_header = 'EchoTech'
admin.site.site_title = 'EchoTech Admin'