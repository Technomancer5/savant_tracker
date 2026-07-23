from django import forms

from .models import Project


STATUS_CHOICES = [
    ("", "Select status"),
    ("Active", "Active"),
    ("Pause", "Pause"),
    ("Backlog", "Backlog"),
    ("Completed", "Completed"),
]

PRIORITY_CHOICES = [
    ("", "Select priority"),
    ("Very High", "Very High"),
    ("High", "High"),
    ("Medium", "Medium"),
    ("Low", "Low"),
]


class ProjectForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
    )

    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        required=False,
    )

    class Meta:
        model = Project
        fields = "__all__"