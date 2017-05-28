from django import forms

from .models import TestModelFile


class TestModelForm(forms.ModelForm):

    class Meta:
        model = TestModelFile
        fields = '__all__'
