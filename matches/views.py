from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MatchForm
from .models import Match


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
    return render(request, "matches/match_detail.html", {"match": match})