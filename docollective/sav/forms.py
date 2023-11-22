from django import forms

from sav.models import Message


class MessageForm(forms.ModelForm):
    subject = forms.CharField(label="Objet", help_text="Merci de donner un maximum d'informations.", max_length=200)

    class Meta:
        model = Message
        fields = ["subject", "message"]


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["message"]
