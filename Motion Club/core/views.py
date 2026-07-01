from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import MemberEditForm, MemberForm
from .models import Event, Member, Sport, SportGroup, Testimonial


def _current_member(request):
    """O usuário 'logado' nesta sessão (protótipo sem auth real)."""
    mid = request.session.get("member_id")
    return Member.objects.filter(pk=mid).first() if mid else None


def _back(request):
    """Volta para a página de origem (campo hidden `next`) ou a home."""
    nxt = request.POST.get("next") or ""
    return redirect(nxt if nxt.startswith("/") else "home")


def home(request):
    """Landing — conteúdo do banco; marca grupos/eventos em que já estou inscrito."""
    today = timezone.localdate()
    events = list(
        Event.objects.select_related("sport").filter(date__gte=today).order_by("date")[:4]
    )
    if not events:
        events = list(Event.objects.select_related("sport").order_by("date")[:4])

    me = _current_member(request)
    context = {
        "sports": Sport.objects.all(),
        "groups": SportGroup.objects.select_related("sport").prefetch_related("members")[:6],
        "events": events,
        "testimonials": Testimonial.objects.select_related("member", "sport")[:3],
        "stats": {
            "members": Member.objects.count(),
            "groups": SportGroup.objects.count(),
            "sports": Sport.objects.count(),
        },
        "my_group_ids": list(me.sport_groups.values_list("id", flat=True)) if me else [],
        "my_event_ids": list(me.events_joined.values_list("id", flat=True)) if me else [],
        "my_sport_ids": list(me.favorite_sports.values_list("id", flat=True)) if me else [],
    }
    return render(request, "home.html", context)


def login_view(request):
    """Entrar por e-mail, ou via Google/Apple (botões funcionais — protótipo)."""
    if request.method == "POST":
        email = (request.POST.get("email") or "").strip()
        provider = request.POST.get("provider")  # 'google' | 'apple' | None
        member = Member.objects.filter(email__iexact=email).first()

        if provider:
            label = "Google" if provider == "google" else "Apple"
            if not email:
                messages.error(request, f"Informe o e-mail para continuar com {label}.")
                return redirect("login")
            created = False
            if not member:
                name = email.split("@")[0].replace(".", " ").replace("_", " ").title()
                member = Member.objects.create(name=name or "Novo atleta", email=email)
                created = True
            request.session["member_id"] = member.pk
            if created:
                messages.success(
                    request, f"Conta criada com {label}! Bem-vindo, {member.first_name}."
                )
            else:
                messages.success(request, f"Você entrou com {label}, {member.first_name}!")
            return redirect("member_detail", pk=member.pk)

        if member:
            request.session["member_id"] = member.pk
            messages.success(request, f"Bem-vindo de volta, {member.first_name}!")
            return redirect("member_detail", pk=member.pk)
        messages.error(request, "Não encontramos uma conta com esse e-mail. Crie a sua!")
        return redirect("member_create")
    return render(request, "login.html")


def logout_view(request):
    request.session.pop("member_id", None)
    messages.info(request, "Você saiu da sua conta.")
    return redirect("home")


def member_list(request):
    q = request.GET.get("q", "").strip()
    members = Member.objects.prefetch_related("favorite_sports").order_by("name")
    if q:
        members = members.filter(
            Q(name__icontains=q) | Q(email__icontains=q) | Q(city__icontains=q)
        )
    me = _current_member(request)
    connected_ids = list(me.connections.values_list("id", flat=True)) if me else []
    return render(
        request,
        "members/list.html",
        {"members": members, "q": q, "count": members.count(), "connected_ids": connected_ids},
    )


def member_detail(request, pk):
    member = get_object_or_404(
        Member.objects.prefetch_related("favorite_sports", "connections", "sport_groups"),
        pk=pk,
    )
    me = _current_member(request)
    breakdown = member.sports_breakdown()
    max_count = max((count for _, count in breakdown), default=1)
    context = {
        "member": member,
        "breakdown": breakdown,
        "max_count": max_count,
        "recent": member.participations.select_related("sport", "event", "group")[:8],
        "is_self": bool(me and me.pk == member.pk),
        "is_connected": bool(me and me.connections.filter(pk=member.pk).exists()),
    }
    return render(request, "members/detail.html", context)


def member_create(request):
    """Criar sua conta (com senha e foto PNG) e já entrar."""
    if request.method == "POST":
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save()
            request.session["member_id"] = member.pk
            messages.success(request, f"Conta criada! Bem-vindo, {member.first_name}.")
            return redirect(member.get_absolute_url())
    else:
        form = MemberForm()
    return render(request, "members/form.html", {"form": form})


def connect_view(request, pk):
    if request.method != "POST":
        return redirect("member_detail", pk=pk)
    me = _current_member(request)
    if not me:
        messages.error(request, "Entre na sua conta para se conectar com pessoas.")
        return redirect("login")
    target = get_object_or_404(Member, pk=pk)
    if target.pk == me.pk:
        messages.info(request, "Esse é o seu próprio perfil. 🙂")
    elif me.connections.filter(pk=target.pk).exists():
        me.connections.remove(target)
        messages.info(request, f"Você removeu a conexão com {target.first_name}.")
    else:
        me.connections.add(target)
        messages.success(request, f"Você se conectou com {target.first_name}!")
    nxt = request.POST.get("next") or ""
    return redirect(nxt) if nxt.startswith("/") else redirect("member_detail", pk=pk)


def join_group(request, pk):
    """Participar / sair de um grupo (A comunidade te espera)."""
    if request.method != "POST":
        return redirect("home")
    me = _current_member(request)
    if not me:
        messages.error(request, "Entre na sua conta para participar de um grupo.")
        return redirect("login")
    group = get_object_or_404(SportGroup, pk=pk)
    if group.members.filter(pk=me.pk).exists():
        group.members.remove(me)
        messages.info(request, f"Você saiu do grupo {group.name}.")
    else:
        group.members.add(me)
        messages.success(request, f"Você entrou no grupo {group.name}!")
    return _back(request)


def join_event(request, pk):
    """Inscrever / cancelar inscrição em um evento (Próximos eventos)."""
    if request.method != "POST":
        return redirect("home")
    me = _current_member(request)
    if not me:
        messages.error(request, "Entre na sua conta para se inscrever em um evento.")
        return redirect("login")
    event = get_object_or_404(Event, pk=pk)
    if event.attendees.filter(pk=me.pk).exists():
        event.attendees.remove(me)
        messages.info(request, f"Inscrição cancelada: {event.title}.")
    else:
        event.attendees.add(me)
        messages.success(request, f"Inscrição confirmada: {event.title}!")
    return _back(request)


def join_sport(request, slug):
    """Inscrever / sair de uma modalidade (favoritar o esporte)."""
    if request.method != "POST":
        return redirect("home")
    me = _current_member(request)
    if not me:
        messages.error(request, "Entre na sua conta para se inscrever em uma modalidade.")
        return redirect("login")
    sport = get_object_or_404(Sport, slug=slug)
    if me.favorite_sports.filter(pk=sport.pk).exists():
        me.favorite_sports.remove(sport)
        messages.info(request, f"Você saiu da modalidade {sport.name}.")
    else:
        me.favorite_sports.add(sport)
        messages.success(request, f"Você se inscreveu em {sport.name}!")
    return _back(request)


def member_edit(request):
    """Editar o próprio perfil."""
    me = _current_member(request)
    if not me:
        messages.error(request, "Entre na sua conta para editá-la.")
        return redirect("login")
    if request.method == "POST":
        form = MemberEditForm(request.POST, request.FILES, instance=me)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado!")
            return redirect(me.get_absolute_url())
    else:
        form = MemberEditForm(instance=me)
    return render(request, "members/edit.html", {"form": form, "member": me})


def account_delete(request):
    me = _current_member(request)
    if not me:
        messages.error(request, "Entre na sua conta primeiro.")
        return redirect("login")
    if request.method == "POST":
        name = me.first_name
        request.session.pop("member_id", None)
        me.delete()
        messages.success(request, f"Sua conta foi excluída. Até logo, {name}.")
        return redirect("home")
    return render(request, "members/confirm_delete.html", {"member": me})
