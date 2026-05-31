"""Helper pédagogique pour les notebooks de python_support.

Ce module fournit trois fonctions principales :

- ``configurer(nom, session=None)`` — enregistre l'identité du stagiaire.
- ``verifier_et_reveler(notebook, exercice, tests, correction)`` — exécute les
  tests, affiche la correction si succès, envoie l'événement au serveur
  formateur en best-effort.
- ``etat()`` — affiche la configuration courante et l'état du buffer.

URL du serveur formateur hardcodée : ``https://notebooks.inspyration.net``

Mode hors ligne : si le serveur n'est pas joignable, les événements sont
bufferisés dans ``~/.python_support/buffer.jsonl`` et réémis automatiquement
quand la connexion revient. **La révélation de la correction ne dépend pas
du serveur** — elle est uniquement basée sur le résultat des tests locaux.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

SERVEUR: str = "https://notebooks.inspyration.net"
CONFIG_DIR: Path = Path.home() / ".python_support"
CONFIG_FILE: Path = CONFIG_DIR / "config.json"
BUFFER_FILE: Path = CONFIG_DIR / "buffer.jsonl"

_state: dict[str, Any] = {
    "nom": None,
    "session": None,
    "token": None,
    "serveur": SERVEUR,
    "tentatives": {},  # {(notebook, exercice): int}
}


# ─────────────────────────────────────────────────────────────────────────
# Gestion de la configuration locale
# ─────────────────────────────────────────────────────────────────────────


def _ensure_config_dir() -> None:
    CONFIG_DIR.mkdir(exist_ok=True)


def _charger_config_locale() -> None:
    """Charge la config depuis ~/.python_support/config.json si elle existe."""
    if not CONFIG_FILE.exists():
        return
    try:
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        for key in ("nom", "session", "token", "serveur"):
            if key in data:
                _state[key] = data[key]
    except (json.JSONDecodeError, OSError):
        pass


def _sauvegarder_config_locale() -> None:
    """Persiste la config dans ~/.python_support/config.json."""
    _ensure_config_dir()
    to_save = {
        "nom": _state["nom"],
        "session": _state["session"],
        "token": _state["token"],
        "serveur": _state["serveur"],
    }
    CONFIG_FILE.write_text(
        json.dumps(to_save, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


# ─────────────────────────────────────────────────────────────────────────
# Communication serveur
# ─────────────────────────────────────────────────────────────────────────


def _poster_json(url: str, payload: dict, headers: dict | None = None, timeout: float = 3.0) -> dict | None:
    """POST un payload JSON et retourne la réponse parsée, ou None en cas d'échec."""
    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json", **(headers or {})}
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            return json.loads(body) if body else {}
    except (urllib.error.URLError, OSError, json.JSONDecodeError, TimeoutError):
        return None


def _envoyer_event(event: dict) -> bool:
    """Envoie un événement au serveur. Retourne True si succès."""
    if not _state.get("token"):
        return False

    result = _poster_json(
        f"{_state['serveur']}/api/events",
        event,
        headers={"X-Student-Token": _state["token"]},
        timeout=2.0,
    )
    return result is not None


# ─────────────────────────────────────────────────────────────────────────
# Buffer hors ligne
# ─────────────────────────────────────────────────────────────────────────


def _bufferiser_event(event: dict) -> None:
    """Ajoute un événement au buffer local (une ligne JSON par événement)."""
    _ensure_config_dir()
    with BUFFER_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def _flush_buffer() -> tuple[int, int]:
    """Tente de renvoyer les événements bufferisés.

    Retourne ``(nb_envoyés, nb_restants)``. Si tous les événements sont
    envoyés, supprime le fichier buffer.
    """
    if not BUFFER_FILE.exists():
        return 0, 0

    lignes = BUFFER_FILE.read_text(encoding="utf-8").splitlines()
    restants: list[str] = []
    envoyes = 0

    for ligne in lignes:
        if not ligne.strip():
            continue
        try:
            event = json.loads(ligne)
        except json.JSONDecodeError:
            continue  # ligne corrompue, on la jette

        if _envoyer_event(event):
            envoyes += 1
        else:
            restants.append(ligne)

    if restants:
        BUFFER_FILE.write_text("\n".join(restants) + "\n", encoding="utf-8")
    else:
        BUFFER_FILE.unlink(missing_ok=True)

    return envoyes, len(restants)


# ─────────────────────────────────────────────────────────────────────────
# API publique
# ─────────────────────────────────────────────────────────────────────────


def configurer(nom: str, session: str | None = None) -> None:
    """Enregistre l'identité du stagiaire et rejoint une session si fournie.

    En mode solo (``session=None``), la configuration est purement locale et
    aucun événement n'est envoyé au serveur.

    Si ``session`` est fourni, le helper tente de rejoindre la session
    auprès du serveur formateur. En cas d'échec (serveur indisponible,
    session inconnue, etc.), le helper bascule en mode solo et affiche un
    message d'avertissement ; la révélation des corrections continue de
    fonctionner localement.
    """
    _state["nom"] = nom
    _state["session"] = session
    _state["token"] = None

    if not session:
        print(f"✅ Bonjour {nom}, mode solo (sans suivi formateur).")
        _sauvegarder_config_locale()
        return

    result = _poster_json(
        f"{SERVEUR}/api/sessions/{session}/join",
        {"nom": nom},
        timeout=5.0,
    )

    if result and "token" in result:
        _state["token"] = result["token"]
        print(f"✅ Bonjour {nom}, session « {session} » rejointe.")
        print(f"   Vos exercices seront suivis par le formateur.")
    else:
        print(f"⚠  Serveur indisponible ou session inconnue.")
        print(f"   Les corrections fonctionneront en mode hors ligne.")

    _sauvegarder_config_locale()


def verifier_et_reveler(
    notebook: str,
    exercice: int,
    tests: Callable[[], None],
    correction: str | None = None,
) -> None:
    """Exécute ``tests`` et affiche la correction uniquement en cas de succès.

    ``tests`` est une fonction sans argument qui lève ``AssertionError`` en
    cas d'échec. Elle voit les variables du kernel (namespace IPython).

    En cas de succès : affiche un message de réussite, affiche la correction
    (si fournie), et envoie un événement « success » au serveur formateur
    (best-effort).

    En cas d'échec : affiche le message d'erreur et encourage à réessayer.
    La correction reste cachée. Un événement « failure » est envoyé.
    """
    try:
        from IPython.display import Markdown, display
    except ImportError:
        # Fallback si on n'est pas dans IPython
        def display(obj: object) -> None:
            print(obj)

        def Markdown(text: str) -> str:  # type: ignore[misc]
            return text

    key = (notebook, exercice)
    tentatives_dict: dict = _state["tentatives"]
    tentatives_dict[key] = tentatives_dict.get(key, 0) + 1
    n_tentatives = tentatives_dict[key]

    event_base = {
        "notebook": notebook,
        "exercice": exercice,
        "tentatives": n_tentatives,
        "timestamp": datetime.now(UTC).isoformat(),
    }

    # Tentative d'exécution des tests
    try:
        tests()
    except AssertionError as e:
        message = (str(e) or "assertion échouée")[:200]
        event = {**event_base, "status": "failure", "message": message}

        if not _envoyer_event(event) and _state.get("token"):
            _bufferiser_event(event)

        print(f"❌ Pas encore (tentative {n_tentatives}) : {message}")
        print("   Réessayez — vous êtes sur la bonne voie.")
        return
    except Exception as e:
        message = f"{type(e).__name__}: {str(e)[:180]}"
        event = {**event_base, "status": "failure", "message": message}

        if not _envoyer_event(event) and _state.get("token"):
            _bufferiser_event(event)

        print(f"❌ Erreur inattendue : {message}")
        print("   Vérifiez votre code avant de réessayer.")
        return

    # Succès
    event = {**event_base, "status": "success"}
    envoye = _envoyer_event(event)
    if not envoye and _state.get("token"):
        _bufferiser_event(event)

    # Indicateur de transport
    if _state.get("token"):
        suffixe = " 🟢" if envoye else " 🟡 (bufferisé)"
    else:
        suffixe = ""

    print(
        f"✅ Bravo ! Exercice {exercice} réussi en {n_tentatives} "
        f"tentative(s).{suffixe}"
    )

    # Flush best-effort du buffer
    if _state.get("token") and envoye:
        try:
            flushed, _ = _flush_buffer()
            if flushed:
                print(f"   📬 {flushed} événement(s) bufferisé(s) ont été envoyés.")
        except Exception:
            pass

    # Affichage de la correction
    if correction:
        display(
            Markdown(
                "**Proposition de correction :**\n\n```python\n"
                + correction.strip()
                + "\n```"
            )
        )


def marquer_tentative(notebook: str, exercice: int, message: str | None = None) -> None:
    """Signale au serveur formateur qu'un exercice a été tenté.

    Contrairement à ``verifier_et_reveler``, cette fonction n'évalue rien :
    elle envoie simplement un événement ``attempt`` (best-effort). Utile
    pour les exercices sans tests automatiques.
    """
    key = (notebook, exercice)
    tentatives_dict: dict = _state["tentatives"]
    tentatives_dict[key] = tentatives_dict.get(key, 0) + 1
    n_tentatives = tentatives_dict[key]

    event: dict[str, Any] = {
        "notebook": notebook,
        "exercice": exercice,
        "status": "attempt",
        "tentatives": n_tentatives,
        "timestamp": datetime.now(UTC).isoformat(),
    }
    if message:
        event["message"] = message[:200]

    if not _state.get("token"):
        print(f"📝 Exercice {exercice} marqué comme tenté (mode solo, non transmis).")
        return

    envoye = _envoyer_event(event)
    if not envoye:
        _bufferiser_event(event)

    suffixe = "🟢" if envoye else "🟡 (bufferisé)"
    print(f"📝 Exercice {exercice} marqué comme tenté {suffixe}")


def etat() -> None:
    """Affiche l'état de la configuration courante."""
    print(f"Stagiaire : {_state.get('nom') or '(non configuré)'}")
    print(f"Session   : {_state.get('session') or '(mode solo)'}")
    print(f"Serveur   : {_state.get('serveur')}")
    print(f"Jeton     : {'✅ présent' if _state.get('token') else '❌ absent'}")

    if BUFFER_FILE.exists():
        try:
            lignes = BUFFER_FILE.read_text(encoding="utf-8").splitlines()
            n = sum(1 for ligne in lignes if ligne.strip())
            if n:
                print(f"Buffer    : {n} événement(s) en attente d'envoi")
        except OSError:
            pass


# ─────────────────────────────────────────────────────────────────────────
# Auto-chargement au premier import
# ─────────────────────────────────────────────────────────────────────────

_charger_config_locale()
