"""
Popula o banco de dados com uma comunidade de exemplo do Motion Club.

Uso:
    python manage.py seed

É idempotente: limpa os dados das tabelas do app e recria tudo do zero.
"""
import calendar
import random
import unicodedata
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from core.models import (
    Event,
    Member,
    Participation,
    Sport,
    SportGroup,
    Testimonial,
)

# (nome, slug, chamada, imagem em static/)
SPORTS = [
    ("Corrida", "corrida", "Do 5K à maratona", "images/sport-corrida.png"),
    ("Futebol", "futebol", "Peladas e society", "images/sport-futebol.png"),
    ("Vôlei", "volei", "Quadra e praia", "images/sport-volei.png"),
    ("Beach Tennis", "beach-tennis", "Areia o ano todo", "images/sport-beachtennis.png"),
    ("Basquete", "basquete", "Streetball e quadra", "images/sport-basquete.png"),
    ("Yoga em grupo", "yoga", "Respira e conecta", "images/sport-yoga.png"),
    ("Funcional", "funcional", "Força ao ar livre", "images/sport-funcional.png"),
    ("Trilha", "trilha", "Montanha e natureza", "images/sport-trilha.png"),
    ("Musculação", "musculacao", "Treino de força", "images/sport-musculacao.png"),
    ("Ciclismo", "ciclismo", "Estrada e urbano", "images/sport-ciclismo.png"),
    ("Natação", "natacao", "Piscina e mar", "images/sport-natacao.png"),
    ("Escalada", "escalada", "Indoor e rocha", "images/sport-escalada.png"),
]

# (nome, slug do esporte, bairro, agenda, gratuito, descrição)
GROUPS = [
    ("Corredores do Aterro", "corrida", "Flamengo", "Ter & Qui · 6h", True,
     "Treinos coletivos no Aterro do Flamengo, do iniciante ao avançado."),
    ("BT Barra Norte", "beach-tennis", "Barra da Tijuca", "Sáb · 8h", False,
     "Rachas e clínicas de beach tennis na areia, para todos os níveis."),
    ("Pedal Zona Sul", "ciclismo", "Zona Sul", "Dom · 6h30", True,
     "Pedais de estrada e urbanos pela orla, em ritmo colaborativo."),
    ("Pelada da Quinta", "futebol", "Tijuca", "Qui · 20h", False,
     "Futebol society toda quinta, espírito coletivo e sem panela."),
    ("Yoga ao Ar Livre", "yoga", "Ipanema", "Sáb · 17h", True,
     "Práticas de vinyasa e respiração ao pôr do sol, na praia."),
    ("Treino Funcional Outdoor", "funcional", "Lagoa", "Seg, Qua, Sex · 7h", True,
     "Circuitos de força e mobilidade ao ar livre, sempre em grupo."),
]

# (título, slug do esporte, dias a partir de hoje, local, horário)
EVENTS = [
    ("Corrida do Aterro — 5K e 10K", "corrida", 5, "Aterro do Flamengo", "6h"),
    ("Torneio Aberto de Beach Tennis", "beach-tennis", 12, "Barra da Tijuca", "9h"),
    ("Pedal Orla Completa — Barra ao Centro", "ciclismo", 23, "Largada na Barra", "6h30"),
    ("Jogo Aberto de Vôlei de Praia", "volei", 30, "Praia de Copacabana", "16h"),
    ("Trilha da Pedra Bonita ao Nascer do Sol", "trilha", 18, "São Conrado", "5h30"),
    ("Treino Funcional Coletivo na Lagoa", "funcional", 9, "Parque da Lagoa", "7h"),
]

# Membros com nome e e-mail próprios (autores de depoimento + o Pietro)
NAMED_MEMBERS = [
    ("Pietro Flumignan", "pietroflumignan@gmail.com", "Rio de Janeiro", "avancado",
     ["corrida", "ciclismo", "musculacao"],
     "Apaixonado por endurance. Sempre buscando o próximo desafio sobre duas pernas ou duas rodas."),
    ("Marina Alves", "marina.alves@exemplo.com", "Rio de Janeiro", "intermediario",
     ["corrida", "funcional"],
     "Voltei a correr no Motion Club e não parei mais."),
    ("Rafael Costa", "rafael.costa@exemplo.com", "Niterói", "iniciante",
     ["beach-tennis", "volei"],
     "Descobri o beach tennis aos 30 e virou meu fim de semana."),
    ("Juliana Reis", "juliana.reis@exemplo.com", "Rio de Janeiro", "avancado",
     ["ciclismo", "trilha"],
     "Pedalar com gente boa mudou minha relação com a cidade."),
]

TESTIMONIALS = [
    ("marina.alves@exemplo.com", "corrida",
     "Eu queria voltar a correr, mas sempre desistia sozinha. No Motion Club "
     "encontrei pessoas com o mesmo ritmo e isso mudou minha rotina completamente."),
    ("rafael.costa@exemplo.com", "beach-tennis",
     "Comecei no beach tennis sem nunca ter jogado. O grupo foi super acolhedor "
     "e hoje é o ponto alto do meu fim de semana."),
    ("juliana.reis@exemplo.com", "ciclismo",
     "Entrei para o grupo de ciclismo e saí com amigos de verdade. A plataforma "
     "é simples, o resultado é real. Recomendo pra todo mundo."),
]

FIRST_NAMES = [
    "Ana", "Bruno", "Camila", "Diego", "Eduarda", "Felipe", "Gabriela", "Henrique",
    "Isabela", "João", "Larissa", "Lucas", "Mariana", "Nicolas", "Patrícia", "Rodrigo",
    "Sofia", "Thiago", "Vanessa", "Vitor", "Beatriz", "Caio", "Daniela", "Gustavo",
    "Helena", "Igor", "Júlia", "Leonardo", "Natália", "Otávio", "Renata", "Samuel",
]
LAST_NAMES = [
    "Silva", "Santos", "Oliveira", "Souza", "Lima", "Pereira", "Carvalho", "Gomes",
    "Ribeiro", "Martins", "Rocha", "Almeida", "Nunes", "Mendes", "Barbosa", "Freitas",
    "Cardoso", "Teixeira", "Moraes", "Pinto",
]
CITIES = [
    "Rio de Janeiro", "Niterói", "São Gonçalo", "Duque de Caxias",
    "Nova Iguaçu", "Petrópolis", "Maricá", "Rio de Janeiro", "Rio de Janeiro",
]
LEVELS = ["iniciante", "intermediario", "avancado"]
BIOS = [
    "Treina pela leveza de fazer parte de algo.",
    "Acredita que esporte é melhor em comunidade.",
    "Sempre topa um treino novo no fim de semana.",
    "Do sofá ao primeiro 5K — e seguindo.",
    "Conheceu metade dos amigos atuais num grupo de treino.",
    "Coleciona nascer do sol em treino ao ar livre.",
    "",
]


def deaccent(text):
    return (
        unicodedata.normalize("NFKD", text)
        .encode("ascii", "ignore")
        .decode("ascii")
    )


class Command(BaseCommand):
    help = "Popula o banco com a comunidade de exemplo do Motion Club."

    @transaction.atomic
    def handle(self, *args, **options):
        random.seed(42)
        today = timezone.localdate()

        self.stdout.write("Limpando dados existentes…")
        Participation.objects.all().delete()
        Testimonial.objects.all().delete()
        Event.objects.all().delete()
        SportGroup.objects.all().delete()
        Member.objects.all().delete()
        Sport.objects.all().delete()

        # ---- Sports ----
        sports = {}
        for i, (name, slug, tagline, image) in enumerate(SPORTS):
            sports[slug] = Sport.objects.create(
                name=name, slug=slug, tagline=tagline, image=image, order=i,
                description=f"Grupos e eventos de {name.lower()} pela cidade.",
            )

        # ---- Members ----
        members = []
        used_emails = set()

        def add_member(name, email, city, level, sport_slugs, bio):
            member = Member.objects.create(
                name=name, email=email, city=city, level=level, bio=bio,
                joined_at=today - timedelta(days=random.randint(20, 720)),
            )
            member.favorite_sports.set([sports[s] for s in sport_slugs])
            members.append(member)
            used_emails.add(email)
            return member

        for name, email, city, level, slugs, bio in NAMED_MEMBERS:
            add_member(name, email, city, level, slugs, bio)

        slug_list = list(sports.keys())
        target_total = 42
        i = 0
        while len(members) < target_total:
            first = FIRST_NAMES[i % len(FIRST_NAMES)]
            last = LAST_NAMES[(i // len(FIRST_NAMES) + i) % len(LAST_NAMES)]
            name = f"{first} {last}"
            email = f"{deaccent(first).lower()}.{deaccent(last).lower()}{i}@exemplo.com"
            i += 1
            if email in used_emails:
                continue
            n_sports = random.randint(1, 3)
            slugs = random.sample(slug_list, n_sports)
            add_member(
                name, email, random.choice(CITIES), random.choice(LEVELS),
                slugs, random.choice(BIOS),
            )

        # ---- Connections (pessoas conhecidas no esporte) ----
        by_sport = {slug: [] for slug in slug_list}
        for member in members:
            for sport in member.favorite_sports.all():
                by_sport[sport.slug].append(member)

        for member in members:
            pool = set()
            for sport in member.favorite_sports.all():
                pool.update(by_sport[sport.slug])
            pool.discard(member)
            pool = list(pool)
            if pool:
                k = min(len(pool), random.randint(2, 6))
                member.connections.add(*random.sample(pool, k))

        # ---- Groups (com membros) ----
        groups_by_sport = {}
        for name, sport_slug, neighborhood, schedule, is_free, desc in GROUPS:
            group = SportGroup.objects.create(
                name=name, sport=sports[sport_slug], neighborhood=neighborhood,
                schedule=schedule, is_free=is_free, description=desc,
            )
            candidates = by_sport[sport_slug] or members
            k = min(len(candidates), random.randint(8, 16))
            group.members.set(random.sample(candidates, k))
            groups_by_sport.setdefault(sport_slug, []).append(group)

        # ---- Events (agendados para o mês que vem) ----
        ny = today.year + (1 if today.month == 12 else 0)
        nm = 1 if today.month == 12 else today.month + 1
        nlast = calendar.monthrange(ny, nm)[1]
        events_by_sport = {}
        for title, sport_slug, day, location, time_label in EVENTS:
            event = Event.objects.create(
                title=title, sport=sports[sport_slug],
                date=date(ny, nm, min(day, nlast)),
                location=location, time_label=time_label,
                group=(groups_by_sport.get(sport_slug) or [None])[0],
            )
            events_by_sport.setdefault(sport_slug, []).append(event)

        # ---- Participations (base das métricas) ----
        participations = []
        for member in members:
            for sport in member.favorite_sports.all():
                for _ in range(random.randint(4, 16)):
                    group = None
                    event = None
                    roll = random.random()
                    if roll < 0.5 and groups_by_sport.get(sport.slug):
                        group = random.choice(groups_by_sport[sport.slug])
                    elif roll < 0.7 and events_by_sport.get(sport.slug):
                        event = random.choice(events_by_sport[sport.slug])
                    participations.append(
                        Participation(
                            member=member, sport=sport, group=group, event=event,
                            date=today - timedelta(days=random.randint(1, 240)),
                        )
                    )
        Participation.objects.bulk_create(participations)

        # ---- Testimonials ----
        member_by_email = {m.email: m for m in members}
        for email, sport_slug, quote in TESTIMONIALS:
            member = member_by_email.get(email)
            if member:
                Testimonial.objects.create(
                    member=member, sport=sports[sport_slug], quote=quote
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Banco populado: "
                f"{Sport.objects.count()} modalidades, "
                f"{Member.objects.count()} usuários, "
                f"{SportGroup.objects.count()} grupos, "
                f"{Event.objects.count()} eventos, "
                f"{Participation.objects.count()} participações, "
                f"{Testimonial.objects.count()} depoimentos."
            )
        )
        self.stdout.write("Dica: crie um admin com  python manage.py createsuperuser")
