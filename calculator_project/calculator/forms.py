from django import forms


class CalculatorForm(forms.Form):
    button = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )