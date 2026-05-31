"""Étape 03 — Catalogue en mémoire.

Les livres sont maintenant des dicts avec titre, auteur, annee, isbn et
date_ajout. Le menu gagne une option pour compter les livres.
"""

from datetime import date

livres: list[dict] = []

while True:
    print()
    print("==== Bibliothèque ====")
    print("(1) Ajouter un livre")
    print("(2) Afficher tous les livres")
    print("(3) Compter les livres")
    print("(q) Quitter")
    choix = input("Votre choix : ").strip().lower()

    if choix == "1":
        titre = input("Titre : ")
        auteur = input("Auteur : ")
        annee = int(input("Année : "))
        isbn = input("ISBN : ")
        livre = {
            "titre": titre,
            "auteur": auteur,
            "annee": annee,
            "isbn": isbn,
            "date_ajout": date.today().isoformat(),
        }
        livres.append(livre)
        print(f"✅ Ajouté le {livre['date_ajout']}.")
    elif choix == "2":
        if not livres:
            print("« Aucun livre dans le catalogue. »")
        else:
            for numero, livre in enumerate(livres, start=1):
                print(
                    f"{numero}. « {livre['titre']} » — {livre['auteur']} ({livre['annee']})"
                )
                print(
                    f"   ISBN : {livre['isbn']}   |   Ajouté le {livre['date_ajout']}"
                )
    elif choix == "3":
        total = len(livres)
        mot = "livre" if total < 2 else "livres"
        print(f"Le catalogue contient {total} {mot}.")
    elif choix == "q":
        print("À bientôt !")
        break
    else:
        print(f"❌ Choix inconnu : {choix!r}")
