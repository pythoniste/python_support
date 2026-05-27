"""Logique métier — calcul de mensualité d'un emprunt à taux fixe.

Aucun code réseau. Module importé par les trois paires client/serveur.
"""


def calcul_mensualite(
    capital: float,
    taux_annuel: float,
    duree_en_mois: int,
    *,
    arrondi: bool = False,
) -> float:
    """Mensualité M = K · t/12 / (1 - (1 + t/12)^-n).

    Cas particulier : taux nul → M = K / n (remboursement linéaire).

    >>> round(calcul_mensualite(200_000, 0.0475, 300), 2)
    1140.23
    >>> calcul_mensualite(50_000, 0, 60, arrondi=True)
    833.33
    """
    if duree_en_mois <= 0:
        raise ValueError(f"Durée doit être strictement positive (reçu {duree_en_mois})")
    if capital < 0:
        raise ValueError(f"Capital doit être positif ou nul (reçu {capital})")
    if taux_annuel < 0:
        raise ValueError(f"Taux doit être positif ou nul (reçu {taux_annuel})")

    taux_mensuel = taux_annuel / 12
    if taux_mensuel == 0:
        resultat = capital / duree_en_mois
    else:
        resultat = (
            capital * taux_mensuel
            / (1 - (1 + taux_mensuel) ** -duree_en_mois)
        )
    return round(resultat, 2) if arrondi else resultat


if __name__ == "__main__":
    cas = [
        (200_000, 0.0475, 25 * 12, "Achat principal"),
        (100_000, 0.03,   20 * 12, "Investissement locatif"),
        (50_000,  0.0,    60,       "Prêt familial (sans intérêts)"),
    ]
    print(f"{'Capital':>10s} {'Taux':>8s} {'Durée':>8s} {'Mensualité':>12s}  Libellé")
    print("-" * 70)
    for K, t, n, libelle in cas:
        M = calcul_mensualite(K, t, n, arrondi=True)
        print(f"{K:>10d} {t:>8.4f} {n:>8d} {M:>12.2f}  {libelle}")
