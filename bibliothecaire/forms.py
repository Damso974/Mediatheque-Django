from django import forms

from .models import (
    Membre,
    Media,
    Livre,
    Dvd,
    Cd,
    JeuDePlateau,
    Emprunt,
)


class MembreForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ["nom"]


class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = [
            "titre",
            "auteur",
            "disponible",
        ]


class DvdForm(forms.ModelForm):
    class Meta:
        model = Dvd
        fields = [
            "titre",
            "realisateur",
            "disponible",
        ]


class CdForm(forms.ModelForm):
    class Meta:
        model = Cd
        fields = [
            "titre",
            "artiste",
            "disponible",
        ]


class JeuDePlateauForm(forms.ModelForm):
    class Meta:
        model = JeuDePlateau
        fields = [
            "nom",
            "createur",
        ]


class EmpruntForm(forms.ModelForm):
    class Meta:
        model = Emprunt
        fields = [
            "membre",
            "media",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["media"].queryset = Media.objects.filter(
            disponible=True
        )