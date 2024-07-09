from django.contrib import admin
from bot.models import *
from app.models import UserPromoCode
from django.utils.html import format_html
from django.urls import reverse
from solo.admin import SingletonModelAdmin
from django.db.models import Count

class UserPromoCodeInline(admin.TabularInline):
    model = UserPromoCode
    extra = 0  # This removes the extra blank forms
    readonly_fields = ['promo_code', 'entered_at', 'ticket_id']
    def ticket_id(self, obj):
        return obj.pk
    ticket_id.short_description = 'Bilet raqami'
    can_delete = False

class Bot_userAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        list_display = ['name', 'phone', 'region', 'address', 'date', 'tickets']
        # if request.user.is_superuser:
        if True:
            list_display.append('edit_button')
        return list_display
    search_fields = ['name', 'username', 'phone', 'address', 'region']
    list_filter = ['date', 'region']
    list_display_links = None
    sortable_by = ['date', 'tickets']
    inlines = [UserPromoCodeInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(tickets_count=Count('userpromocode'))
        return qs
    
    def tickets(self, obj):
        return obj.tickets_count
    tickets.short_description = 'Biletlar'
    tickets.admin_order_field = 'tickets_count'

    def edit_button(self, obj):
        change_url = reverse('admin:bot_bot_user_change', args=[obj.id])
        return format_html('<a class="btn btn-primary" href="{}"><i class="fas fa-edit"></i></a>', change_url)
    edit_button.short_description = ''

    def get_fieldsets(self, request, obj):
        if request.user.is_superuser:
            fieldsets = super().get_fieldsets(request, obj)
        else:
            fieldsets = (
                ('Asosiy', {
                    'fields': ['name', 'username', 'phone', 'region', 'address'],
                }),
            )
        return fieldsets

class MesageAdmin(admin.ModelAdmin):
    list_display = ['bot_users_name', 'small_text', 'open_photo', 'open_video', 'open_file', 'date']
    list_display_links = None
    fieldsets = (
        ('', {
            'fields': ['bot_users', 'text', 'photo', 'video', 'file'],
            'description': 'Выберите пользователей, которым вы хотите отправить сообщение, или просто оставьте поле пустым, чтобы отправить всем пользователям.', 
        }),

    )
    
    def bot_users_name(self, obj):
        result = ''
        if users:=obj.bot_users.all():
            for user in users:
                result += f'{user.name} {user.phone} | '
        else:
            result = 'Все'
        return result
    bot_users_name.short_description = 'Пользователи бота'

    def small_text(self, obj):
        cut_text = obj.text[:20] + ' ...' if len(obj.text) >= 20 else obj.text
        return format_html(f'<p title={obj.text}>{cut_text}</p>')
    small_text.short_description = 'Текст'

    def open_photo(self, obj):
        if obj.photo:
            change_url = f'/files/{obj.photo}'
            return format_html('<a target="_blank" class="btn btn-success" href="{}"><i class="fas fa-eye"></i> Открыть</a>', change_url)
        return None
    open_photo.short_description = 'Фото'

    def open_video(self, obj):
        if obj.video:
            change_url = f'/files/{obj.video}'
            return format_html('<a target="_blank" class="btn btn-warning" href="{}"><i class="fas fa-eye"></i> Открыть</a>', change_url)
        return None
    open_video.short_description = 'Видео'

    def open_file(self, obj):
        if obj.file:
            change_url = f'/files/{obj.file}'
            return format_html('<a target="_blank" class="btn btn-primary" href="{}"><i class="fas fa-eye"></i> Открыть</a>', change_url)
        return None
    open_file.short_description = 'Файл'

    def get_form(self, request, obj=None, **kwargs):
        form = super(MesageAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['bot_users'].widget.attrs['style'] = 'width: 20em;'
        return form

admin.site.register(Bot_user, Bot_userAdmin)
admin.site.register(Message, MesageAdmin)
admin.site.register(ProductsFile, SingletonModelAdmin)
admin.site.register(Diler, SingletonModelAdmin)
admin.site.register(TermOfElectric, SingletonModelAdmin)
admin.site.register(TermOfBusinessman, SingletonModelAdmin)
admin.site.register(Prize, SingletonModelAdmin)