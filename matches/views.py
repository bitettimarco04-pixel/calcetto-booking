from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MatchForm, RegistrationForm
from .models import Match, Registration


@login_required
def create_match(request):
    if request.method == "POST":
        form = MatchForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            match.organizer = request.user
            match.save()
            return redirect("match_detail", token=match.share_token)
    else:
        form = MatchForm()
    return render(request, "matches/create_match.html", {"form": form})


def match_detail(request, token):
    match = get_object_or_404(Match, share_token=token)
    confirmed = match.registrations.filter(status=Registration.Status.CONFIRMED)
    waitlist = match.registrations.filter(status=Registration.Status.WAITLIST)

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.match = match
            if confirmed.count() >= match.max_players:
                registration.status = Registration.Status.WAITLIST
            registration.save()
            return redirect("match_detail", token=match.share_token)
    else:
        form = RegistrationForm()

    context = {
        "match": match,
        "form": form,
        "confirmed": confirmed,
        "waitlist": waitlist,
        "free_spots": match.max_players - confirmed.count(),
    }
    return render(request, "matches/match_detail.html", context)