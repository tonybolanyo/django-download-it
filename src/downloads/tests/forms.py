from django import forms

from .models import ModelTestFile, ModelTestMultipleMime


class ModelFormTest(forms.ModelForm):

    class Meta:
        model = ModelTestFile
        fields = '__all__'


class MultipleMimeFormTest(forms.ModelForm):

    class Meta:
        model = ModelTestMultipleMime
        fields = '__all__'