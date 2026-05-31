"""Étape 04 — Recherche et tri.

Ajoute :
- une recherche case-insensitive sur titre et auteur,
- un tri par titre, auteur ou année lors de l'affichage.
"""

from datetime import date

livres: list[dict] = []


def _afficher(livre_list: list[dict]) -> None:
    for numero, livre in enumerate(livre_list, start=1):
        print(
            f"{numero}. « {livre['titre']} » — {livre['auteur']} ({livre['annee']})"
        )
        print(
            f"   ISBN : {livre['isbn']}   |   Ajouté le {livre['date_ajout']}"
        )


while True:
    print()
    print("==== Bibliothèque ====")
    print("(1) Ajouter un livre")
    print("(2) Afficher tous les livres")
    print("(3) Compter les livres")
    print("(4) Rechercher")
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
            critere = input("Trier par : (t)itre, (a)uteur, a(n)née : ").strip().lower()
            clefs = {
                "t": lambda livre: livre["titre"].casefold(),
                "a": lambda livre: livre["auteur"].casefold(),
                "n": lambda livre: livre["annee"],
            }
            if critere not in clefs:
                print(f"❌ Critère de tri inconnu : {critere!r}")
                continue
            tries = sorted(livres, key=clefs[critere])
            _afficher(tries)
    elif choix == "3":
        total = len(livres)
        mot = "livre" if total < 2 else "livres"
        print(f"Le catalogue contient {total} {mot}.")
    elif choix == "4":
        if not livres:
            print("« Aucun livre dans le catalogue. »")
            continue
        terme = input("Rechercher : ").strip().casefold()
        resultats = [
            livre
            for livre in livres
            if terme in livre["titre"].casefold() or terme in livre["auteur"].casefold()
        ]
        print(f"Résultats ({len(resultats)}) :")
        _afficher(resultats)
    elif choix == "q":
        print("À bientôt !")
        break
    else:
        print(f"❌ Choix inconnu : {choix!r}")
