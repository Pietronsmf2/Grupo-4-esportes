from django.db import models

# Create your models here.
import uuid
from django.db import models


#CHOICES===

class Choices:
    CATEGORIA = [('coletivo', 'Coletivo'), ('individual', 'Individual'), ('aquatico', 'Aquático')]
    PRIVACIDADE = [('aberto', 'Aberto'), ('fechado', 'Fechado')]
    PAPEL = [('admin', 'Admin'), ('membro', 'Membro')]
    STATUS_MEMBRO = [('pendente', 'Pendente'), ('aprovado', 'Aprovado'), ('bloqueado', 'Bloqueado')]
    STATUS_EVENTO = [('aberto', 'Aberto'), ('lotado', 'Lotado'), ('cancelado', 'Cancelado'), ('encerrado', 'Encerrado')]
    STATUS_PRESENCA = [('confirmado', 'Confirmado'), ('cancelado', 'Cancelado'), ('lista_espera', 'Lista de Espera')]
    NIVEL = [('iniciante', 'Iniciante'), ('intermediario', 'Intermediário'), ('avancado', 'Avançado')]


# TABELAS DO BANCO)

class Usuario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha_hash = models.CharField(max_length=255) # O Django tem sistemas próprios de senha, mas mantive o campo solicitado
    foto_url = models.URLField(blank=True, null=True)
    localizacao = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.DecimalField(max_length=9, decimal_places=6, blank=True, null=True, max_digits=9)
    longitude = models.DecimalField(max_length=9, decimal_places=6, blank=True, null=True, max_digits=9)
    bio = models.TextField(blank=True, null=True)
    verificado = models.BooleanField(default=False)
    nota_media = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Modalidade(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100, unique=True)
    icone = models.CharField(max_length=255, blank=True, null=True)
    categoria = models.CharField(max_length=20, choices=Choices.CATEGORIA)

    def __str__(self):
        return self.nome


class Grupo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    modalidade = models.ForeignKey(Modalidade, on_delete=models.RESTRICT)
    admin = models.ForeignKey(Usuario, on_delete=models.RESTRICT)
    localizacao = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.DecimalField(max_length=9, decimal_places=6, blank=True, null=True, max_digits=9)
    longitude = models.DecimalField(max_length=9, decimal_places=6, blank=True, null=True, max_digits=9)
    privacidade = models.CharField(max_length=10, choices=Choices.PRIVACIDADE, default='aberto')
    max_membros = models.IntegerField(default=50)
    nivel = models.CharField(max_length=20, choices=Choices.NIVEL)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class MembroGrupo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    papel = models.CharField(max_length=10, choices=Choices.PAPEL, default='membro')
    status = models.CharField(max_length=15, choices=Choices.STATUS_MEMBRO, default='pendente')
    entrou_em = models.DateTimeField(auto_now_add=True)


class Evento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    criador = models.ForeignKey(Usuario, on_delete=models.RESTRICT)
    titulo = models.CharField(max_length=150)
    descricao = models.TextField(blank=True, null=True)
    data_hora = models.DateTimeField()
    local_nome = models.CharField(max_length=150)
    local_endereco = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_length=9, decimal_places=6, blank=True, null=True, max_digits=9)
    longitude = models.DecimalField(max_length=9, decimal_places=6, blank=True, null=True, max_digits=9)
    max_participantes = models.IntegerField()
    status = models.CharField(max_length=15, choices=Choices.STATUS_EVENTO, default='aberto')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class PresencaEvento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=Choices.STATUS_PRESENCA, default='confirmado')
    confirmado_em = models.DateTimeField(auto_now_add=True)


class Mensagem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    topico = models.CharField(max_length=100, blank=True, null=True)
    conteudo = models.TextField()
    enviado_em = models.DateTimeField(auto_now_add=True)


class Avaliacao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    avaliador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='avaliacoes_feitas')
    avaliado = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='avaliacoes_recebidas')
    nota = models.IntegerField() # Você pode validar de 1 a 5 na View do Python depois
    comentario = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)


class PreferenciaUsuario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    modalidade = models.ForeignKey(Modalidade, on_delete=models.CASCADE)
    nivel = models.CharField(max_length=20, choices=Choices.NIVEL)


class Notificacao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    titulo = models.CharField(max_length=150)
    conteudo = models.TextField()
    lida = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)