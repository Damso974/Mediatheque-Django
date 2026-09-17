import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import (
    Membre,
    Media,
    Livre,
    Dvd,
    Cd,
    JeuDePlateau,
    Emprunt,
)

from .forms import (
    MembreForm,
    LivreForm,
    DvdForm,
    CdForm,
    JeuDePlateauForm,
    EmpruntForm,
)


logger = logging.getLogger("bibliothecaire")


# =========================
# GESTION DES MEMBRES
# =========================

@login_required
def liste_membres(request):
    membres = Membre.objects.all()

    return render(
        request,
        "membres/liste_membres.html",
        {"membres": membres}
    )


@login_required
def creer_membre(request):
    if request.method == "POST":
        form = MembreForm(request.POST)

        if form.is_valid():
            membre = form.save()

            logger.info(
                "Création du membre : %s",
                membre.nom
            )

            return redirect("liste_membres")

    else:
        form = MembreForm()

    return render(
        request,
        "membres/creer_membre.html",
        {"form": form}
    )


@login_required
def modifier_membre(request, membre_id):
    membre = get_object_or_404(
        Membre,
        id=membre_id
    )

    if request.method == "POST":
        form = MembreForm(
            request.POST,
            instance=membre
        )

        if form.is_valid():
            membre = form.save()

            logger.info(
                "Modification du membre : %s",
                membre.nom
            )

            return redirect("liste_membres")

    else:
        form = MembreForm(instance=membre)

    return render(
        request,
        "membres/modifier_membre.html",
        {"form": form}
    )


@login_required
def supprimer_membre(request, membre_id):
    membre = get_object_or_404(
        Membre,
        id=membre_id
    )

    if request.method == "POST":
        logger.info(
            "Suppression du membre : %s",
            membre.nom
        )

        membre.delete()

        return redirect("liste_membres")

    return render(
        request,
        "membres/supprimer_membre.html",
        {"membre": membre}
    )


# =========================
# GESTION DES MÉDIAS
# =========================

@login_required
def liste_medias(request):
    medias = Media.objects.all()
    jeux = JeuDePlateau.objects.all()

    return render(
        request,
        "medias/liste_medias_bibliothecaire.html",
        {
            "medias": medias,
            "jeux": jeux,
        }
    )


@login_required
def creer_media(request):
    type_media = request.GET.get("type")

    formulaires = {
        "livre": LivreForm,
        "dvd": DvdForm,
        "cd": CdForm,
        "jeu": JeuDePlateauForm,
    }

    FormulaireSelectionne = formulaires.get(
        type_media
    )

    if FormulaireSelectionne is None:
        return render(
            request,
            "medias/choisir_type_media.html"
        )

    if request.method == "POST":
        form = FormulaireSelectionne(
            request.POST
        )

        if form.is_valid():
            media = form.save()

            logger.info(
                "Création d'un média : %s",
                media
            )

            return redirect(
                "liste_medias_bibliothecaire"
            )

    else:
        form = FormulaireSelectionne()

    return render(
        request,
        "medias/creer_media.html",
        {
            "form": form,
            "type_media": type_media,
        }
    )


@login_required
def modifier_media(request, media_id):
    media = get_object_or_404(
        Media,
        id=media_id
    )

    if hasattr(media, "livre"):
        objet = media.livre
        FormulaireSelectionne = LivreForm

    elif hasattr(media, "dvd"):
        objet = media.dvd
        FormulaireSelectionne = DvdForm

    elif hasattr(media, "cd"):
        objet = media.cd
        FormulaireSelectionne = CdForm

    else:
        return redirect(
            "liste_medias_bibliothecaire"
        )

    if request.method == "POST":
        form = FormulaireSelectionne(
            request.POST,
            instance=objet
        )

        if form.is_valid():
            media_modifie = form.save()

            logger.info(
                "Modification du média : %s",
                media_modifie
            )

            return redirect(
                "liste_medias_bibliothecaire"
            )

    else:
        form = FormulaireSelectionne(
            instance=objet
        )

    return render(
        request,
        "medias/modifier_media.html",
        {"form": form}
    )


@login_required
def supprimer_media(request, media_id):
    media = get_object_or_404(
        Media,
        id=media_id
    )

    if request.method == "POST":
        logger.info(
            "Suppression du média : %s",
            media
        )

        media.delete()

        return redirect(
            "liste_medias_bibliothecaire"
        )

    return render(
        request,
        "medias/supprimer_media.html",
        {"media": media}
    )


# =========================
# GESTION DES EMPRUNTS
# =========================

@login_required
def liste_emprunts(request):
    emprunts = Emprunt.objects.all()

    return render(
        request,
        "emprunts/liste_emprunts.html",
        {"emprunts": emprunts}
    )


@login_required
def creer_emprunt(request):
    message_erreur = None

    if request.method == "POST":
        form = EmpruntForm(request.POST)

        if form.is_valid():
            membre = form.cleaned_data["membre"]

            emprunts_membre = Emprunt.objects.filter(
                membre=membre
            )

            # Maximum de 3 emprunts simultanés
            if emprunts_membre.count() >= 3:
                message_erreur = (
                    "Ce membre possède déjà "
                    "3 emprunts."
                )

            # Vérification des emprunts en retard
            else:
                for emprunt in emprunts_membre:
                    if emprunt.est_en_retard():
                        message_erreur = (
                            "Ce membre possède "
                            "un emprunt en retard."
                        )
                        break

            # Création si aucune règle n'est violée
            if message_erreur is None:
                emprunt = form.save()

                media = emprunt.media
                media.disponible = False
                media.save()

                logger.info(
                    "Création d'un emprunt : "
                    "membre=%s, média=%s",
                    emprunt.membre,
                    emprunt.media
                )

                return redirect(
                    "liste_emprunts"
                )

    else:
        form = EmpruntForm()

    return render(
        request,
        "emprunts/creer_emprunt.html",
        {
            "form": form,
            "message_erreur": message_erreur,
        }
    )


@login_required
def retourner_emprunt(request, emprunt_id):
    emprunt = get_object_or_404(
        Emprunt,
        id=emprunt_id
    )

    if request.method == "POST":
        media = emprunt.media
        media.disponible = True
        media.save()

        logger.info(
            "Retour d'un média : "
            "membre=%s, média=%s",
            emprunt.membre,
            emprunt.media
        )

        emprunt.delete()

        return redirect(
            "liste_emprunts"
        )

    return render(
        request,
        "emprunts/retourner_emprunt.html",
        {"emprunt": emprunt}
    )