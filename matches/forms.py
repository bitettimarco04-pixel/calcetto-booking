from django import forms

from .models import Match


class MatchForm(forms.ModelForm):
    starts_at = forms.DateTimeField(
        label="Data e ora",
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
        ),
        input_formats=["%Y-%m-%dT%H:%M"],
    )

    class Meta:
        model = Match
        fields = ["location", "starts_at", "max_players", "visibility"]
        labels = {
            "location": "Luogo",
            "max_players": "Numero di giocatori",
            "visibility": "Visibilità",
        }