from .models import Member


def current_member(request):
    """Expõe o usuário "logado" (via sessão) para todos os templates."""
    member = None
    mid = request.session.get("member_id")
    if mid:
        member = Member.objects.filter(pk=mid).first()
    return {"current_member": member}
