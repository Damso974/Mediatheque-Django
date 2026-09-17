from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import (
    Membre,
    Media,
    Livre,
    Dvd,
    Cd,
    JeuDePlateau,
    Emprunt,
)

from .models import Membre
from datetime import date, timedelta
from .forms import EmpruntForm


class MembreTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="bibliothecaire",
            password="motdepasse_test"
        )

        self.client.login(
            username="bibliothecaire",
            password="motdepasse_test"
        )

    def test_creer_membre(self):
        response = self.client.post(
            reverse("creer_membre"),
            {
                "nom": "Jean Dupont"
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertTrue(
            Membre.objects.filter(
                nom="Jean Dupont"
            ).exists()
        )

    def test_liste_membres(self):
        Membre.objects.create(
            nom="Jean Dupont"
        )

        response = self.client.get(
            reverse("liste_membres")
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertContains(
            response,
            "Jean Dupont"
        )

    def test_modifier_membre(self):
        membre = Membre.objects.create(
            nom="Jean Dupont"
        )

        response = self.client.post(
            reverse(
                "modifier_membre",
                args=[membre.id]
            ),
            {
                "nom": "Jean Martin"
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )

        membre.refresh_from_db()

        self.assertEqual(
            membre.nom,
            "Jean Martin"
        )

    def test_supprimer_membre(self):
        membre = Membre.objects.create(
            nom="Jean Dupont"
        )

        response = self.client.post(
            reverse(
                "supprimer_membre",
                args=[membre.id]
            )
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertFalse(
            Membre.objects.filter(
                id=membre.id
            ).exists()
        )

class MediaTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="bibliothecaire",
            password="motdepasse_test"
        )

        self.client.login(
            username="bibliothecaire",
            password="motdepasse_test"
        )

    def test_creer_livre(self):
        response = self.client.post(
            reverse("creer_media") + "?type=livre",
            {
                "titre": "Le Petit Prince",
                "auteur": "Antoine de Saint-Exupéry",
                "disponible": True,
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertTrue(
            Livre.objects.filter(
                titre="Le Petit Prince"
            ).exists()
        )

    def test_creer_dvd(self):
        response = self.client.post(
            reverse("creer_media") + "?type=dvd",
            {
                "titre": "Matrix",
                "realisateur": "Wachowski",
                "disponible": True,
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertTrue(
            Dvd.objects.filter(
                titre="Matrix"
            ).exists()
        )

    def test_creer_cd(self):
        response = self.client.post(
            reverse("creer_media") + "?type=cd",
            {
                "titre": "Thriller",
                "artiste": "Michael Jackson",
                "disponible": True,
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertTrue(
            Cd.objects.filter(
                titre="Thriller"
            ).exists()
        )

    def test_creer_jeu_de_plateau(self):
        response = self.client.post(
            reverse("creer_media") + "?type=jeu",
            {
                "nom": "Catan",
                "createur": "Klaus Teuber",
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertTrue(
            JeuDePlateau.objects.filter(
                nom="Catan"
            ).exists()
        )

    def test_liste_medias(self):
        Livre.objects.create(
            titre="Le Petit Prince",
            auteur="Antoine de Saint-Exupéry",
            disponible=True,
        )

        JeuDePlateau.objects.create(
            nom="Catan",
            createur="Klaus Teuber",
        )

        response = self.client.get(
            reverse("liste_medias_bibliothecaire")
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertContains(
            response,
            "Le Petit Prince"
        )

        self.assertContains(
            response,
            "Catan"
        )
class EmpruntTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="bibliothecaire",
            password="motdepasse_test"
        )

        self.client.login(
            username="bibliothecaire",
            password="motdepasse_test"
        )

        self.membre = Membre.objects.create(
            nom="Jean Dupont"
        )

        self.livre = Livre.objects.create(
            titre="Le Petit Prince",
            auteur="Antoine de Saint-Exupéry",
            disponible=True,
        )

    def test_creer_emprunt(self):
        response = self.client.post(
            reverse("creer_emprunt"),
            {
                "membre": self.membre.id,
                "media": self.livre.id,
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertTrue(
            Emprunt.objects.filter(
                membre=self.membre,
                media=self.livre,
            ).exists()
        )

        self.livre.refresh_from_db()

        self.assertFalse(
            self.livre.disponible
        )

    def test_maximum_trois_emprunts(self):
        medias = []

        for numero in range(4):
            media = Livre.objects.create(
                titre=f"Livre {numero}",
                auteur="Auteur",
                disponible=True,
            )

            medias.append(media)

        for media in medias[:3]:
            Emprunt.objects.create(
                membre=self.membre,
                media=media,
            )

            media.disponible = False
            media.save()

        response = self.client.post(
            reverse("creer_emprunt"),
            {
                "membre": self.membre.id,
                "media": medias[3].id,
            }
        )

        self.assertEqual(
            Emprunt.objects.filter(
                membre=self.membre
            ).count(),
            3
        )

        self.assertContains(
            response,
            "Ce membre possède déjà 3 emprunts."
        )

    def test_emprunt_interdit_si_retard(self):
        ancien_media = Livre.objects.create(
            titre="Ancien livre",
            auteur="Auteur",
            disponible=False,
        )

        emprunt = Emprunt.objects.create(
            membre=self.membre,
            media=ancien_media,
        )

        emprunt.date_emprunt = (
            date.today() - timedelta(days=8)
        )
        emprunt.save()

        nouveau_media = Livre.objects.create(
            titre="Nouveau livre",
            auteur="Auteur",
            disponible=True,
        )

        response = self.client.post(
            reverse("creer_emprunt"),
            {
                "membre": self.membre.id,
                "media": nouveau_media.id,
            }
        )

        self.assertEqual(
            Emprunt.objects.filter(
                membre=self.membre
            ).count(),
            1
        )

        self.assertContains(
            response,
            "Ce membre possède un emprunt en retard."
        )

        nouveau_media.refresh_from_db()

        self.assertTrue(
            nouveau_media.disponible
        )

    def test_retourner_emprunt(self):
        emprunt = Emprunt.objects.create(
            membre=self.membre,
            media=self.livre,
        )

        self.livre.disponible = False
        self.livre.save()

        response = self.client.post(
            reverse(
                "retourner_emprunt",
                args=[emprunt.id]
            )
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.livre.refresh_from_db()

        self.assertTrue(
            self.livre.disponible
        )

        self.assertFalse(
            Emprunt.objects.filter(
                id=emprunt.id
            ).exists()
        )

        def test_jeu_de_plateau_non_empruntable(self):
            jeu = JeuDePlateau.objects.create(
                nom="Catan",
                createur="Klaus Teuber"
            )

            form = EmpruntForm()

            medias_disponibles = (
                form.fields["media"].queryset
            )

            self.assertNotIn(
                jeu,
                medias_disponibles
            )
from django.test import TestCase

# Create your tests here.
