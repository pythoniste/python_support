#!/usr/bin/env python3
"""Demo : sous-commandes dispatchées via set_defaults(func=...).

À exécuter :

    python3 04_demo_sous_commandes.py ajouter "écrire un rapport"
    python3 04_demo_sous_commandes.py ajouter "appeler Bob" --priorite 3
    python3 04_demo_sous_commandes.py lister
    python3 04_demo_sous_commandes.py lister --toutes
    python3 04_demo_sous_commandes.py finir 1
    python3 04_demo_sous_commandes.py --help
    python3 04_demo_sous_commandes.py ajouter --help

Observer :
- chaque sous-commande a sa propre page d'aide ;
- l'attribut `args.func` est utilisé pour dispatcher en une ligne ;
- la sous-commande est obligatoire (required=True).
"""
import argparse


def cmd_ajouter(args):
    print(f"[ajouter] tâche : {args.texte!r} (priorité {args.priorite})")


def cmd_lister(args):
    cible = "toutes" if args.toutes else "actives"
    print(f"[lister] affichage des tâches {cible}")


def cmd_finir(args):
    print(f"[finir] tâche numéro {args.id} marquée comme terminée")


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="demo_sous_commandes",
        description="Mini-démo d'une CLI à sous-commandes.",
    )
    subs = parser.add_subparsers(dest="commande", required=True)

    p_add = subs.add_parser("ajouter", help="ajouter une tâche")
    p_add.add_argument("texte", help="description courte de la tâche")
    p_add.add_argument("--priorite", "-p", type=int, default=1,
                       help="priorité numérique (par défaut : 1)")
    p_add.set_defaults(func=cmd_ajouter)

    p_list = subs.add_parser("lister", help="afficher les tâches")
    p_list.add_argument("--toutes", action="store_true",
                        help="inclut aussi les tâches terminées")
    p_list.set_defaults(func=cmd_lister)

    p_done = subs.add_parser("finir", help="marquer une tâche terminée")
    p_done.add_argument("id", type=int, help="numéro de la tâche")
    p_done.set_defaults(func=cmd_finir)

    return parser


def main():
    parser = construire_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
