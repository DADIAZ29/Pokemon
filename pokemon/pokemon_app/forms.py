from django import forms

from .models import Pokemon, PokemonSprites


class PokemonSpritesForm(forms.ModelForm):
    class Meta:
        model = PokemonSprites
        fields = [
            "front_default",
            "back_default",
            "front_shiny",
            "back_shiny",
        ]
        widgets = {
            "front_default": forms.URLInput(attrs={"class": "form-control"}),
            "back_default": forms.URLInput(attrs={"class": "form-control"}),
            "front_shiny": forms.URLInput(attrs={"class": "form-control"}),
            "back_shiny": forms.URLInput(attrs={"class": "form-control"}),
        }


class PokemonForm(forms.ModelForm):
    class Meta:
        model = Pokemon
        fields = ["name", "height", "weight", "order"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "height": forms.NumberInput(attrs={"class": "form-control"}),
            "weight": forms.NumberInput(attrs={"class": "form-control"}),
            "order": forms.NumberInput(attrs={"class": "form-control"}),
        }
