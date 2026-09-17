

from django.shortcuts import render
from bibliothecaire.models import Media, JeuDePlateau


def liste_medias(request):
    medias = Media.objects.all()
    jeux = JeuDePlateau.objects.all()

    return render(
        request,
        "liste_medias.html",
        {
            "medias": medias,
            "jeux": jeux,
        }
    )


