from django import forms


class DownloadForm(forms.Form):
    since = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    till = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
