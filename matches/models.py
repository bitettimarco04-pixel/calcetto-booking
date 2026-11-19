import uuid

from django.conf import settings
from django.db import models


class Match(models.Model):
    class Visibility(models.TextChoices):
        PRIVATE = "private", "Privata (solo con link)"
        PUBLIC = "public", "Pubblica"

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="matches",
    )
    location = models.CharField(max_length=200)
    starts_at = models.DateTimeField()
    max_players = models.PositiveIntegerField(default=10)
    visibility = models.CharField(
        max_length=10, choices=Visibility.choices, default=Visibility.PRIVATE
    )
    share_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["starts_at"]

    def __str__(self):
        return f"{self.location} - {self.starts_at:%d/%m/%Y %H:%M}"


class Registration(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = "confirmed", "Confermato"
        WAITLIST = "waitlist", "In lista d'attesa"
        CANCELLED = "cancelled", "Cancellato"

    match = models.ForeignKey(
        Match, on_delete=models.CASCADE, related_name="registrations"
    )
    guest_name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.CONFIRMED
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.guest_name} ({self.get_status_display()})"