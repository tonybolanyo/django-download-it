from django import forms

from .models import ModelTestFile


class ModelFormTest(forms.ModelForm):

    class Meta:
        model = ModelTestFile
        fields = '__all__'
