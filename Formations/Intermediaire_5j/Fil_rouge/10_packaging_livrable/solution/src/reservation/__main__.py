"""Point d'entrée CLI du système de réservation."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from sqlalchemy import create_engine

from reservation.service import ReservationService

logger = logging.getLogger("reservation")

DEFAULT_DB = Path("reservation.db")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="reservation",
        description="Système de réservation de salles de réunion.",
    )
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help="Chemin de la base SQLite")
    parser.add_argument("-v", "--verbose", action="store_true", help="Mode debug")

    sub = parser.add_subparsers(dest="commande", help="Commandes disponibles")

    # salles
    sub.add_parser("salles", help="Lister les salles")

    # reserver
    p_res = sub.add_parser("reserver", help="Créer une réservation")
    p_res.add_argument("--salle", required=True, help="Code de la salle")
    p_res.add_argument("--user", required=True, help="Email de l'utilisateur")
    p_res.add_argument("--date", required=True, help="Date ISO (ex: 2025-06-15T09:00)")
    p_res.add_argument("--duree", type=int, required=True, help="Durée en minutes")

    # reservations
    sub.add_parser("reservations", help="Lister les réservations")

    # annuler
    p_ann = sub.add_parser("annuler", help="Annuler une réservation")
    p_ann.add_argument("--id", type=int, required=True, help="ID de la réservation")

    # ajouter-salle
    p_salle = sub.add_parser("ajouter-salle", help="Ajouter une salle")
    p_salle.add_argument("--code", required=True)
    p_salle.add_argument("--nom", required=True)
    p_salle.add_argument("--capacite", type=int, required=True)
    p_salle.add_argument("--type", default="reunion")

    # ajouter-user
    p_user = sub.add_parser("ajouter-user", help="Ajouter un utilisateur")
    p_user.add_argument("--email", required=True)
    p_user.add_argument("--nom", required=True)
    p_user.add_argument("--role", default="user")

    return parser


def main(argv: list[str] | None = None) -> int:
    """Point d'entrée CLI."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    engine = create_engine(f"sqlite:///{args.db}")
    svc = ReservationService(engine)

    if args.commande == "salles":
        # Pour l'instant, pas de listing des salles dans le service simplifié
        print("(Fonctionnalité à étendre : listing des salles)")
    elif args.commande == "reserver":
        rid = svc.reserver(args.salle, args.user, args.date, args.duree)
        print(f"Réservation créée : id={rid}")
    elif args.commande == "reservations":
        resas = svc.lister_reservations()
        if not resas:
            print("Aucune réservation.")
        for r in resas:
            print(f"  [{r['id']}] {r['salle_code']} — {r['utilisateur_email']} "
                  f"le {r['date']} ({r['duree_minutes']} min)")
    elif args.commande == "annuler":
        ok = svc.annuler(args.id)
        print("Annulée." if ok else "Réservation introuvable.")
    elif args.commande == "ajouter-salle":
        svc.ajouter_salle(args.code, args.nom, args.capacite, args.type)
        print(f"Salle {args.code} ajoutée.")
    elif args.commande == "ajouter-user":
        svc.ajouter_utilisateur(args.email, args.nom, args.role)
        print(f"Utilisateur {args.email} ajouté.")
    else:
        parser.print_help()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
