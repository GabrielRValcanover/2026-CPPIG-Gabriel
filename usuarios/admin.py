# from django.contrib import admin
# from django.utils.html import format_html
# from django.contrib.auth.admin import UserAdmin
# from .models import UsuarioPersonalizado
# admin.site.register(UsuarioPersonalizado, UserAdmin)
#
# from .models import Usuario
#
# @admin.register(Usuario)
# class UsuarioAdmin(admin.ModelAdmin):
#     list_display = ('nome', 'email', 'senha', 'tipoUsuario', 'foto')
#     search_fields = ('nome', 'email', 'senha')
#     readonly_fields = ['fotografia']
#     search_fields=('nome', 'email')
#
#
#     def fotografia(self, obj):
#         if obj.foto:
#             return format_html('<img width="75px" src="{}" />', obj.foto.url)
#         pass

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