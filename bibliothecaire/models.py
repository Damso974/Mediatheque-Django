from datetime import date, timedelta

from django.db import models


class Membre(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Media(models.Model):
    titre = models.CharField(max_length=200)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titre


class Livre(Media):
    auteur = models.CharField(max_length=150)


class Dvd(Media):
    realisateur = models.CharField(max_length=150)


class Cd(Media):
    artiste = models.CharField(max_length=150)


class JeuDePlateau(models.Model):
    nom = models.CharField(max_length=200)
    createur = models.CharField(max_length=150)

    def __str__(self):
        return self.nom


class Emprunt(models.Model):
    membre = models.ForeignKey(
        Membre,
        on_delete=models.CASCADE
    )

    media = models.ForeignKey(
        Media,
        on_delete=models.CASCADE
    )

    date_emprunt = models.DateField(auto_now_add=True)

    def date_limite(self):
        return self.date_emprunt + timedelta(days=7)

    def est_en_retard(self):
        return date.today() > self.date_limite()

    def __str__(self):
        return f"{self.membre} - {self.media}"