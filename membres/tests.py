from django.test import TestCase
from django.urls import reverse

from bibliothecaire.models import (
    Livre,
    JeuDePlateau,
)


class ConsultationMediaTests(TestCase):

    def test_consulter_liste_medias(self):
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
            reverse("liste_medias")
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