# Etape 02 -- Systeme de plugins

## Contexte

Le pipeline doit appliquer des **transformations** aux donnees de capteurs (moyenne glissante, detection d'anomalies, conversion d'unites...). Plutot que de coder en dur la liste des transformations, vous allez creer un **systeme de plugins** extensible. N'importe qui peut ajouter un plugin sans modifier le code du pipeline.

## Consignes

1. Creer `src/pipeline/plugin_base.py` :
   - `TransformPlugin` : classe de base abstraite. Utilise `__init_subclass__` pour **auto-enregistrer** chaque sous-classe dans un registre de classe (`TransformPlugin._registry`).
   - Chaque plugin doit declarer un attribut de classe `name: str` (identifiant unique).
   - Methode abstraite `transform(self, readings: list[SensorReading]) -> list[SensorReading]`.
   - Methode de classe `get_plugin(name: str) -> type[TransformPlugin]` pour retrouver un plugin par son nom.
   - Methode de classe `list_plugins() -> list[str]` pour lister les noms disponibles.

2. Creer `src/pipeline/plugins/` avec :
   - `__init__.py` qui importe les plugins pour forcer leur enregistrement.
   - `moving_average.py` : plugin `"moving_average"` qui calcule la moyenne glissante de la temperature sur une fenetre configurable (passee au `__init__`).
   - `anomaly_detector.py` : plugin `"anomaly_detector"` qui marque les lectures dont la temperature s'ecarte de plus de N ecarts-types de la moyenne (N configurable).
   - `unit_converter.py` : plugin `"unit_converter"` qui convertit les temperatures de Celsius en Fahrenheit.

3. Adapter `src/pipeline/__init__.py` pour exporter `TransformPlugin`.

## Attendus

```python
plugin_cls = TransformPlugin.get_plugin("moving_average")
plugin = plugin_cls(window=3)
result = plugin.transform(readings)
```

## Criteres d'acceptation

- [ ] `__init_subclass__` enregistre automatiquement chaque sous-classe.
- [ ] Un plugin sans attribut `name` leve `TypeError` a la definition de la classe.
- [ ] `get_plugin` leve `KeyError` si le nom n'existe pas.
- [ ] Les trois plugins sont fonctionnels et testes.
- [ ] Le registre n'accepte pas deux plugins avec le meme nom (leve `ValueError`).
- [ ] `pytest tests/` est vert.

## Temps estime

1 h 30.

## Solution

Voir `solution/`.

## Pieges frequents

- **Oublier d'importer les modules de plugins** : si le module n'est pas importe, la classe n'est pas definie, et `__init_subclass__` n'est jamais appele.
- **Enregistrer `TransformPlugin` elle-meme** dans le registre : il faut exclure la classe de base.
- **Mutabilite du registre** : le registre est un dictionnaire de classe partage. Attention aux tests qui pourraient le polluer.
