"""Étape 02 — Menu interactif du gestionnaire de bibliothèque.

Boucle principale avec un menu (ajouter, lister, quitter).
Les livres sont stockés en mémoire dans une liste de tuples
``(titre, auteur, annee)``.
"""

livres: list[tuple[str, str, int]] = []

while True:
    print()
    print("==== Bibliothèque ====")
    print("(1) Ajouter un livre")
    print("(2) Afficher tous les livres")
    print("(q) Quitter")
    choix = input("Votre choix : ").strip().lower()

    if choix == "1":
        titre = input("Titre : ")
        auteur = input("Auteur : ")
        annee = int(input("Année : "))
        livres.append((titre, auteur, annee))
        print("✅ Ajouté !")
    elif choix == "2":
        if not livres:
            print("« Aucun livre dans le catalogue. »")
        else:
            for numero, (titre, auteur, annee) in enumerate(livres, start=1):
                print(f"{numero}. « {titre} » — {auteur} ({annee})")
    elif choix == "q":
        print("À bientôt !")
        break
    else:
        print(f"❌ Choix inconnu : {choix!r}")
