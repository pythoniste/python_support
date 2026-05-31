"""Tests du service — étape 10."""

def test_reserver(service):
    service.ajouter_salle("REU-A301", "Everest", 10, "reunion")
    service.ajouter_utilisateur("alice@test.fr", "Alice")
    rid = service.reserver("REU-A301", "alice@test.fr", "2025-06-15T09:00", 60)
    assert isinstance(rid, int)


def test_lister(service):
    service.ajouter_salle("REU-A301", "Everest", 10, "reunion")
    service.ajouter_utilisateur("alice@test.fr", "Alice")
    service.reserver("REU-A301", "alice@test.fr", "2025-06-15T09:00", 60)
    assert len(service.lister_reservations()) == 1


def test_annuler(service):
    service.ajouter_salle("REU-A301", "Everest", 10, "reunion")
    service.ajouter_utilisateur("alice@test.fr", "Alice")
    rid = service.reserver("REU-A301", "alice@test.fr", "2025-06-15T09:00", 60)
    assert service.annuler(rid) is True
    assert service.annuler(9999) is False
