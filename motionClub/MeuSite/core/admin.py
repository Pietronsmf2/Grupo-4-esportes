from django.contrib import admin
from .models import (
    Usuario, Modalidade, Grupo, MembroGrupo, 
    Evento, PresencaEvento, Mensagem, Avaliacao, 
    PreferenciaUsuario, Notificacao
)

# Registrando todas as tabelas para aparecerem no painel
admin.site.register(Usuario)
admin.site.register(Modalidade)
admin.site.register(Grupo)
admin.site.register(MembroGrupo)
admin.site.register(Evento)
admin.site.register(PresencaEvento)
admin.site.register(Mensagem)
admin.site.register(Avaliacao)
admin.site.register(PreferenciaUsuario)
admin.site.register(Notificacao)