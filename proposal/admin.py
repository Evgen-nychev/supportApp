from django.contrib import admin
from .models import Status,Tema,Vajnost,Otdel,User,Tip,SupportRecuest,Message,Spec
from .forms import AdminUserAddForm, AdminUserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

# Register your models here.
class UserAdmin(BaseUserAdmin):
    form = AdminUserChangeForm
    raw_id_fields = ('otdel',)
    add_form = AdminUserAddForm
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2', 'otdel')}
        ),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name',
            'last_name',
            'email',
            'otdel'

        )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

class StatusAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id','name')
class TemaAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id','name')
class VajnostAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id','name')
class OtdelAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id','name')



admin.site.register(User, UserAdmin)
admin.site.register(Status,StatusAdmin)
admin.site.register(Tema,TemaAdmin)
admin.site.register(Vajnost,VajnostAdmin)
admin.site.register(Otdel,VajnostAdmin)
admin.site.register(Tip)
admin.site.register(SupportRecuest)
admin.site.register(Message)
admin.site.register(Spec)