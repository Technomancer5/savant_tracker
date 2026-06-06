from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        # This dynamically loads ALL custom columns automatically
        fields = '__all__'
