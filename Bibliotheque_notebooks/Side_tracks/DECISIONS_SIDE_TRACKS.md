# Decisions Side Tracks

Document de reference pour les choix techniques et pedagogiques des notebooks Side Tracks.

---

## 1. Choix de bibliotheques et justifications

### Calcul_scientifique (4 notebooks)

| Notebook | Bibliotheque | Justification |
|---|---|---|
| 01_Scipy_optimisation | `scipy.optimize` | Reference incontournable pour l'optimisation numerique en Python. Interface unifiee (`minimize`, `root`, `curve_fit`) qui couvre 95% des besoins. |
| 02_Scipy_interpolation | `scipy.interpolate` | Seule bibliotheque standard pour l'interpolation 1D/2D. `CubicSpline`, `interp1d`, `griddata` sont utilises quotidiennement en ingenierie et data science. |
| 03_Scipy_signal | `scipy.signal` | Standard de facto pour le traitement du signal en Python. Filtres IIR/FIR, FFT, detection de pics, spectrogrammes. Alternative a MATLAB Signal Processing Toolbox. |
| 04_Sympy_algebre | `sympy` | Unique bibliotheque de calcul formel mature en Python. Polynomes, matrices symboliques, derivees, integrales, LaTeX. Complementaire a NumPy/SciPy (exact vs numerique). |

**Alternatives ecartees :**
- `cvxpy` : trop specialise (optimisation convexe), pas assez generaliste pour une introduction.
- `mpmath` : precision arbitraire, mais `sympy` l'utilise deja en interne.
- `librosa` : analyse musicale, trop specifique pour un side track general sur le signal.

### GUI (2 notebooks)

| Notebook | Bibliotheque | Justification |
|---|---|---|
| 01_Tkinter_basics | `tkinter` | Inclus dans la bibliotheque standard Python. Zero dependance. Ideal pour les petites interfaces et le prototypage rapide. Indispensable a connaitre. |
| 02_PySide6_intro | `PySide6` | Binding officiel Qt (license LGPL). Ecosysteme le plus complet pour les applications desktop professionnelles. Widgets natifs, signaux/slots, MVC. |

**Alternatives ecartees :**
- `PyQt6` : quasi-identique a PySide6 mais license GPL (restrictive pour le commercial). PySide6 est le choix officiel Qt.
- `wxPython` : communaute plus petite, moins de ressources pedagogiques.
- `Kivy` : oriente mobile/multitouch, pas desktop classique.
- `Dear PyGui` : trop recent, API instable.

### Jeu_video (2 notebooks)

| Notebook | Bibliotheque | Justification |
|---|---|---|
| 01_Pygame_ce_intro | `pygame-ce` | Fork communautaire actif de Pygame. Bas niveau mais pedagogique : on comprend la boucle de jeu, le blitting, le delta time. Standard pour l'apprentissage. |
| 02_Arcade | `arcade` | API orientee objet plus moderne. Heritage de `Window`, `SpriteList` avec batching GPU, `View` pour les scenes. Bon complement a Pygame pour montrer l'approche haut niveau. |

**Alternatives ecartees :**
- `pyglet` : bon mais Arcade est construit dessus et offre une API plus ergonomique.
- `Panda3D` : 3D, trop complexe pour une introduction.
- `Ursina` : interessant mais trop jeune et pas assez documente.
- `Godot + Python` : necessiterait un editeur externe, hors scope notebook.

### XML_avance (3 notebooks)

| Notebook | Bibliotheque | Justification |
|---|---|---|
| 01_Xml_schemas | `lxml` + `xmlschema` | `lxml` est le standard performant pour XML en Python. `xmlschema` ajoute une API pythonique pour la validation et la conversion XML <-> dict/JSON. |
| 02_Sax_et_iterparse | `xml.sax` + `lxml.etree.iterparse` | `xml.sax` est dans la stdlib (zero dependance). `iterparse` est le meilleur compromis performance/ergonomie pour les gros fichiers. |
| 03_Xpath_et_xslt | `lxml` | Seule bibliotheque Python supportant XPath 1.0 et XSLT 1.0 de maniere complete et performante. |

**Alternatives ecartees :**
- `xml.etree.ElementTree` : trop limite (pas de XPath complet, pas de XSLT, pas de validation XSD).
- `saxon-c` : supporte XPath 3.0/XSLT 3.0 mais difficile a installer et peu pythonique.
- `defusedxml` : securite XML, mentionne en note mais pas un side track entier.

---

## 2. Ordre de priorite et raisonnement

Les side tracks existants (priorite 1-2) couvraient deja les domaines les plus demandes en formation :

| Priorite | Dossiers | Raisonnement |
|---|---|---|
| **P1** (forte demande) | CLI_et_TUI, Cryptographie_avancee, Web_backend | Utilises dans presque toutes les formations intermediaires/avancees. |
| **P2** (demande moderee) | Data_science, Data_visualization, Multimedia, PDF_avance, Systeme_et_Reseau | Specifiques a certains profils (data, devops, bureautique). |
| **P3** (niches) | **Calcul_scientifique**, **GUI**, **Jeu_video**, **XML_avance** | Profils specialises : ingenieurs, scientifiques, developpeurs desktop, integrateurs. |

### Justification de la priorite 3

- **Calcul_scientifique** : demande par les formations ingenieur et recherche. SciPy et SymPy sont des complements naturels a NumPy.
- **GUI** : demande ponctuelle mais forte quand elle arrive. Tkinter pour le prototypage, PySide6 pour les apps serieuses.
- **Jeu_video** : excellent pour l'engagement des debutants. Souvent demande en ecoles et bootcamps.
- **XML_avance** : demande en entreprise (systemes legacy, EDI, SOAP). Moins glamour mais indispensable pour certains profils.

---

## 3. Ce qui est teaser vs approfondissement

### Teasers (introduction, donne envie d'aller plus loin)

| Notebook | Teasers |
|---|---|
| Pygame CE | La structure du jeu est montree mais les jeux complets depassent le cadre (physique, particules, niveaux). |
| Arcade | Les tilemaps et cameras sont mentionnees mais pas approfondies (necessite Tiled editor). |
| PySide6 | QML et Qt Designer sont mentionnes comme pistes mais pas couverts. |
| SymPy | Les equations differentielles et la logique symbolique sont hors scope. |

### Approfondissements (couverture complete ou quasi-complete)

| Notebook | Couverture |
|---|---|
| SciPy optimisation | Couverture exhaustive de `scipy.optimize` : scalaire, multi-dim, contraintes, bornes, curve fitting, moindres carres. |
| SciPy interpolation | Toutes les methodes majeures : interp1d, CubicSpline, PCHIP, Akima, griddata, RegularGridInterpolator, UnivariateSpline. |
| SciPy signal | FFT, filtres IIR/FIR, peaks, convolution, reechantillonnage, Welch, spectrogramme. |
| Tkinter | Couverture complete des widgets, layouts, events, menus, dialogs, ttk. |
| XSD validation | DTD, XSD, RelaxNG, validation lxml et xmlschema, conversion dict/JSON. |
| SAX/iterparse | DOM vs SAX vs iterparse, handlers, filtrage, liberation memoire, statistiques streaming. |
| XPath/XSLT | XPath (axes, predicats, fonctions, namespaces), XSLT (templates, params, apply-templates, modes). |

---

## 4. Suggestions d'ajouts futurs

### Court terme (si demande)

| Dossier | Notebook potentiel | Description |
|---|---|---|
| Calcul_scientifique | `05_Scipy_integration.ipynb` | Integration numerique (quad, dblquad, odeint). |
| Calcul_scientifique | `06_Scipy_linalg.ipynb` | Algebre lineaire numerique (SVD, LU, Cholesky, sparse). |
| GUI | `03_Flet_apps.ipynb` | Flet (Flutter pour Python) : apps web/desktop/mobile. |
| Jeu_video | `03_Pyxel.ipynb` | Pyxel : retro gaming 8-bit, API ultra-simple. |
| XML_avance | `04_Defusedxml.ipynb` | Securite XML (XXE, billion laughs, defusedxml). |

### Moyen terme (evolution du marche)

| Dossier | Notebook potentiel | Description |
|---|---|---|
| Calcul_scientifique | `07_JAX_intro.ipynb` | JAX : autodiff + compilation JIT, alternative a NumPy pour le ML. |
| GUI | `04_Textual_desktop.ipynb` | Textual en mode desktop (au-dela du TUI). |
| Jeu_video | `04_Godot_python.ipynb` | GDScript vs Python dans Godot (si le binding murit). |

### Long terme (veille)

- **WebAssembly GUI** : Pyodide + frameworks web pourrait rendre les GUI desktop obsoletes.
- **GPU computing** : CuPy, RAPIDS -- si la demande en formation augmente.
- **Quantum computing** : Qiskit, Cirq -- trop tot pour un side track generaliste.

---

*Document cree le 2026-04-14. Mis a jour a chaque ajout de side track.*
