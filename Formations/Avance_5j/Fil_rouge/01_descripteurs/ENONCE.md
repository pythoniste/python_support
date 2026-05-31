# Etape 01 -- Descripteurs

## Contexte

C'est la premiere demi-journee de la formation Avance. Vous venez de revoir les descripteurs (`__get__`, `__set__`, `__set_name__`). Le pipeline de donnees manipule des **enregistrements de capteurs** (temperature, humidite, pression) qui doivent etre valides avant tout traitement. Plutot que de repeter la logique de validation dans chaque setter, vous allez utiliser des **descripteurs reutilisables**.

## Consignes

1. Creer un module `src/pipeline/descriptors.py` contenant :
   - `Validated` : descripteur de base qui stocke la valeur dans `instance.__dict__` et appelle une methode abstraite `validate(value)`.
   - `RangeField(min_val, max_val)` : sous-classe de `Validated` qui verifie que la valeur est un `float` ou `int` compris dans `[min_val, max_val]`. Leve `ValueError` sinon.
   - `NonEmptyString` : sous-classe de `Validated` qui verifie que la valeur est un `str` non vide apres `strip()`.
   - `RegexField(pattern)` : sous-classe de `Validated` qui verifie qu'un `str` matche entierement un regex donne.

2. Creer un module `src/pipeline/models.py` contenant :
   - `SensorReading` : une classe utilisant ces descripteurs :
     ```python
     class SensorReading:
         sensor_id = RegexField(r"[A-Z]{2}-\d{4}")
         temperature = RangeField(-40.0, 85.0)
         humidity = RangeField(0.0, 100.0)
         pressure = RangeField(300.0, 1100.0)
     ```
   - Le `__init__` accepte les quatre champs en parametres et les affecte.
   - Un `__repr__` lisible.

3. Creer un module `src/pipeline/__init__.py` qui exporte `SensorReading`.

## Attendus

```python
r = SensorReading("AB-1234", 22.5, 45.0, 1013.25)
print(r)  # SensorReading(sensor_id='AB-1234', temperature=22.5, humidity=45.0, pressure=1013.25)

r.temperature = 100.0  # ValueError: 100.0 hors de [-40.0, 85.0]
r.sensor_id = ""        # ValueError: ne matche pas [A-Z]{2}-\d{4}
```

## Criteres d'acceptation

- [ ] `Validated` utilise `__set_name__` pour connaitre le nom de l'attribut.
- [ ] Les valeurs sont stockees dans `instance.__dict__[self.name]`, pas dans le descripteur.
- [ ] `RangeField` leve `ValueError` avec un message clair si la valeur est hors bornes.
- [ ] `NonEmptyString` leve `ValueError` si la chaine est vide ou seulement des espaces.
- [ ] `RegexField` utilise `re.fullmatch`.
- [ ] `SensorReading` fonctionne avec les quatre descripteurs.
- [ ] `pytest tests/` est vert.

## Temps estime

1 h 30.

## Solution

Voir `solution/`.

## Pieges frequents

- **Stocker la valeur dans le descripteur** au lieu de `instance.__dict__` : toutes les instances partagent alors la meme valeur.
- **Oublier `__set_name__`** : le descripteur ne connait pas le nom de l'attribut et ne peut pas stocker dans le bon slot du `__dict__`.
- **Utiliser `re.match` au lieu de `re.fullmatch`** : `match` ne verifie que le debut de la chaine.
- **Ne pas appeler `super().__init_subclass__`** si vous faites de l'heritage entre descripteurs.
