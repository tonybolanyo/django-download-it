from django import forms

from .models import ModelTestFile, ModelTestMultipleMime, ModelTestSizeFile


class ModelFormTest(forms.ModelForm):

    class Meta:
        model = ModelTestFile
        fields = '__all__'


class MultipleMimeFormTest(forms.ModelForm):

    class Meta:
        model = ModelTestMultipleMime
        fields = '__all__'


class ModelFormSizeTest(forms.ModelForm):

    class Meta:
        model = ModelTestSizeFile
        fields = '__all__'


