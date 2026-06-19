from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Sport(models.Model):
    """Modalidade esportiva (corrida, futebol, vôlei...)."""

    name = models.CharField("nome", max_length=60)
    slug = models.SlugField(unique=True)
    tagline = models.CharField("chamada", max_length=120, blank=True)
    description = models.TextField("descrição", blank=True)
    image = models.CharField(
        "imagem (caminho em static/)",
        max_length=200,
        blank=True,
        help_text="ex.: images/sport-corrida.jpg",
    )
    order = models.PositiveIntegerField("ordem", default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "modalidade"
        verbose_name_plural = "modalidades"

    def __str__(self):
        return self.name

    @property
    def group_count(self):
        return self.groups.count()


class Member(models.Model):
    """Usuário / atleta da comunidade."""

    LEVELS = [
        ("iniciante", "Iniciante"),
        ("intermediario", "Intermediário"),
        ("avancado", "Avançado"),
    ]

    name = models.CharField("nome", max_length=120)
    email = models.EmailField("e-mail", unique=True)
    city = models.CharField("cidade", max_length=80, blank=True)
    bio = models.TextField("bio", blank=True)
    avatar = models.FileField(
        "foto (PNG)",
        upload_to="avatars/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["png"])],
    )
    password = models.CharField("senha (hash)", max_length=128, blank=True, default="")
    level = models.CharField("nível", max_length=20, choices=LEVELS, default="iniciante")
    favorite_sports = models.ManyToManyField(
        Sport, related_name="fans", blank=True, verbose_name="esportes de preferência"
    )
    connections = models.ManyToManyField(
        "self", blank=True, verbose_name="pessoas que já conheceu"
    )
    joined_at = models.DateField("entrou em", default=timezone.localdate)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "usuário"
        verbose_name_plural = "usuários"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("member_detail", args=[self.pk])

    @property
    def initials(self):
        parts = [p for p in self.name.split() if p]
        if not parts:
            return "?"
        if len(parts) == 1:
            return parts[0][:2].upper()
        return (parts[0][0] + parts[-1][0]).upper()

    @property
    def first_name(self):
        return self.name.split()[0] if self.name.strip() else self.name

    @property
    def participation_count(self):
        return self.participations.count()

    @property
    def connection_count(self):
        return self.connections.count()

    @property
    def group_count(self):
        return self.sport_groups.count()

    def sports_breakdown(self):
        """Retorna [(Sport, nº de participações)] ordenado do maior para o menor."""
        rows = (
            self.participations.values("sport")
            .annotate(total=models.Count("id"))
            .order_by("-total")
        )
        sports = {s.id: s for s in Sport.objects.filter(id__in=[r["sport"] for r in rows])}
        return [(sports[r["sport"]], r["total"]) for r in rows if r["sport"] in sports]

    @property
    def top_sport(self):
        breakdown = self.sports_breakdown()
        return breakdown[0][0] if breakdown else None


class SportGroup(models.Model):
    """Grupo de uma modalidade (ex.: Corredores do Aterro)."""

    name = models.CharField("nome", max_length=120)
    sport = models.ForeignKey(
        Sport, on_delete=models.CASCADE, related_name="groups", verbose_name="modalidade"
    )
    description = models.TextField("descrição", blank=True)
    neighborhood = models.CharField("bairro", max_length=80, blank=True)
    schedule = models.CharField("agenda", max_length=80, blank=True)
    is_free = models.BooleanField("gratuito", default=True)
    members = models.ManyToManyField(
        Member, related_name="sport_groups", blank=True, verbose_name="membros"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "grupo"
        verbose_name_plural = "grupos"

    def __str__(self):
        return self.name

    @property
    def member_count(self):
        return self.members.count()


class Event(models.Model):
    """Evento aberto (corrida, torneio, pedal...)."""

    title = models.CharField("título", max_length=160)
    sport = models.ForeignKey(
        Sport, on_delete=models.CASCADE, related_name="events", verbose_name="modalidade"
    )
    group = models.ForeignKey(
        SportGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
    )
    date = models.DateField("data")
    time_label = models.CharField("horário", max_length=40, blank=True)
    location = models.CharField("local", max_length=160, blank=True)
    attendees = models.ManyToManyField(
        Member, related_name="events_joined", blank=True, verbose_name="inscritos"
    )

    class Meta:
        ordering = ["date"]
        verbose_name = "evento"
        verbose_name_plural = "eventos"

    def __str__(self):
        return self.title


class Participation(models.Model):
    """Registro de uma participação do usuário (base da métrica de frequência)."""

    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="participations", verbose_name="usuário"
    )
    sport = models.ForeignKey(
        Sport, on_delete=models.CASCADE, related_name="participations", verbose_name="modalidade"
    )
    event = models.ForeignKey(
        Event, on_delete=models.SET_NULL, null=True, blank=True, related_name="participations"
    )
    group = models.ForeignKey(
        SportGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name="participations"
    )
    date = models.DateField("data", default=timezone.localdate)
    note = models.CharField("nota", max_length=160, blank=True)

    class Meta:
        ordering = ["-date"]
        verbose_name = "participação"
        verbose_name_plural = "participações"

    def __str__(self):
        return f"{self.member} · {self.sport} · {self.date:%d/%m/%Y}"


class Testimonial(models.Model):
    """Depoimento exibido na landing."""

    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="testimonials", verbose_name="usuário"
    )
    sport = models.ForeignKey(Sport, on_delete=models.SET_NULL, null=True, blank=True)
    quote = models.TextField("depoimento")

    class Meta:
        verbose_name = "depoimento"
        verbose_name_plural = "depoimentos"

    def __str__(self):
        return f"Depoimento de {self.member}"
