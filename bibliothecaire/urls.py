from django.urls import path
from . import views


urlpatterns = [
    # Membres
    path(
        "membres/",
        views.liste_membres,
        name="liste_membres"
    ),
    path(
        "membres/creer/",
        views.creer_membre,
        name="creer_membre"
    ),
    path(
        "membres/<int:membre_id>/modifier/",
        views.modifier_membre,
        name="modifier_membre"
    ),
    path(
        "membres/<int:membre_id>/supprimer/",
        views.supprimer_membre,
        name="supprimer_membre"
    ),

    # Médias
    path(
        "medias/",
        views.liste_medias,
        name="liste_medias_bibliothecaire"
    ),
    path(
        "medias/creer/",
        views.creer_media,
        name="creer_media"
    ),
    path(
        "medias/<int:media_id>/modifier/",
        views.modifier_media,
        name="modifier_media"
    ),
    path(
        "medias/<int:media_id>/supprimer/",
        views.supprimer_media,
        name="supprimer_media"
    ),

    # Emprunts
    path(
        "emprunts/",
        views.liste_emprunts,
        name="liste_emprunts"
    ),
    path(
        "emprunts/creer/",
        views.creer_emprunt,
        name="creer_emprunt"
    ),
    path(
        "emprunts/<int:emprunt_id>/retourner/",
        views.retourner_emprunt,
        name="retourner_emprunt"
    ),
]