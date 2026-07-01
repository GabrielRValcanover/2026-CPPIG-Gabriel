
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioPersonalizado
class CustomUserAdmin(UserAdmin):
    model = UsuarioPersonalizado
    list_display = ['username', 'email', 'first_name', 'tipoUsuario', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Escolares e Controle', {
            'fields': ('nome', 'tipoUsuario', 'foto', 'bloqueado_ate')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Escolares', {
            'fields': ('nome', 'tipoUsuario', 'foto', 'bloqueado_ate'),
        }),
    )

admin.site.register(UsuarioPersonalizado, CustomUserAdmin)