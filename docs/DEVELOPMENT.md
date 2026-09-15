# Guide de Développement - TaskMaster

## 📋 Table des Matières

1. [Introduction](#introduction)
2. [Prérequis](#prérequis)
3. [Installation](#installation)
4. [Structure du Projet](#structure-du-projet)
5. [Conventions de Code](#conventions-de-code)
6. [Workflow de Développement](#workflow-de-développement)
7. [Tests](#tests)
8. [Documentation](#documentation)
9. [Gestion des Dépendances](#gestion-des-dépendances)
10. [Déploiement](#déploiement)
11. [Contribution](#contribution)

---

## 🚀 Introduction

Bienvenue dans le **Guide de Développement** de TaskMaster ! Ce document vous guidera à travers tout ce que vous devez savoir pour contribuer au projet, de la configuration initiale à la soumission de vos modifications.

---

## 📋 Prérequis

### Système

- **Système d'exploitation** : Windows 10+, macOS 10.15+, ou Linux (Ubuntu 20.04+, Fedora 36+, etc.)
- **Espace disque** : 1 Go minimum (pour les dépendances et les outils)
- **Mémoire** : 4 Go minimum (8 Go recommandé)

### Logiciels

| Logiciel | Version | Installation |
|----------|---------|-------------|
| Python | 3.10+ | [python.org](https://www.python.org/downloads/) |
| Git | 2.30+ | [git-scm.com](https://git-scm.com/) |
| Poetry | 1.6+ | `pip install poetry` |

---

## ⚙ Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/alnews2/EvaluationDeMistralCODE.git
cd EvaluationDeMistralCODE
```

### 2. Configurer l'environnement virtuel

Le projet utilise **Poetry** pour gérer les dépendances. Poetry créera automatiquement un environnement virtuel.

```bash
# Installer les dépendances (y compris celles de développement)
poetry install
```

### 3. Installer les hooks pre-commit

```bash
# Activer les hooks pre-commit
poetry run pre-commit install
```

### 4. Vérifier l'installation

```bash
# Exécuter les tests pour vérifier que tout fonctionne
poetry run pytest
```

---

## 📁 Structure du Projet

```
EvaluationDeMistralCODE/
├── src/
│   ├── __init__.py              # Initialisation du package
│   ├── main.py                  # Point d'entrée de l'application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── controllers/          # Contrôleurs
│   │   │   └── task_controller.py
│   │   ├── models/               # Modèles de données
│   │   │   └── task.py
│   │   └── services/             # Services
│   │       └── task_service.py
│   └── ui/
│       ├── __init__.py
│       ├── dialogs/              # Boîtes de dialogue
│       │   └── task_dialog.py
│       ├── resources/            # Ressources (fichiers .ui, images)
│       ├── windows/              # Fenêtres principales
│       │   └── main_window.py
│       └── widgets/              # Composants réutilisables
├── tests/
│   ├── __init__.py
│   ├── unit/                    # Tests unitaires
│   │   ├── __init__.py
│   │   ├── test_task.py
│   │   └── test_task_service.py
│   └── integration/             # Tests d'intégration
│       ├── __init__.py
│       └── test_main_window.py
├── docs/                        # Documentation
│   ├── ARCHITECTURE.md          # Architecture technique
│   ├── DEVELOPMENT.md           # Ce fichier
│   └── USER_GUIDE.md            # Guide utilisateur
├── .github/
│   └── workflows/
│       └── ci-cd.yml            # Pipeline CI/CD
├── .gitignore
├── .pre-commit-config.yaml     # Configuration des hooks
├── CHANGELOG.md                # Historique des changements
├── LICENSE                     # Licence du projet
├── pyproject.toml              # Configuration Poetry
└── README.md                   # Documentation principale
```

---

## 📜 Conventions de Code

### 1. Style de Code

#### Python

- **Nommage** :
  - Variables et fonctions : `snake_case`
  - Classes : `PascalCase`
  - Constantes : `UPPER_SNAKE_CASE`
  - Méthodes privées : `_private_method`
  - Méthodes protégées : `_protected_method` (par convention)

- **Imports** :
  - Imports relatifs pour les modules du projet
  - Imports absolus pour les dépendances externes
  - Groupez les imports par type (standard library, third-party, local)

- **Docstrings** :
  - Utilisez le format Google pour les docstrings
  - Documentez toutes les classes, méthodes et fonctions publiques

#### Exemple de Docstring

```python
"""Module pour la gestion des tâches."""

from typing import Optional


class TaskService:
    """
    Service pour la gestion des tâches.
    
    Ce service gère les opérations CRUD pour les tâches et assure
    leur persistance.
    
    Attributes:
        storage_path: Chemin vers le fichier de stockage.
    """
    
    def __init__(self, storage_path: str):
        """
        Initialise le service de tâches.
        
        Args:
            storage_path: Chemin vers le fichier JSON de stockage.
        """
        self.storage_path = storage_path
```

### 2. Typage

- Utilisez les **type hints** pour toutes les fonctions et méthodes
- Utilisez `Optional[T]` pour les valeurs qui peuvent être `None`
- Utilisez `Union[T1, T2]` pour les types multiples
- Utilisez `Any` uniquement si vraiment nécessaire

### 3. Longueur des Lignes

- **Maximum** : 88 caractères (configuré dans pyproject.toml)
- **Exception** : Les docstrings et commentaires peuvent être plus longs

### 4. Encodage

- **Encodage** : UTF-8
- **Fin de ligne** : LF (Unix-style)

---

## 🔄 Workflow de Développement

### 1. Créer une Nouvelle Fonctionnalité

1. **Créer une branche** :
   ```bash
   git checkout -b feature/nouvelle-fonctionnalite
   ```

2. **Développer la fonctionnalité** :
   - Suivre les conventions de code
   - Ajouter des tests
   - Mettre à jour la documentation si nécessaire

3. **Exécuter les tests** :
   ```bash
   poetry run pytest
   ```

4. **Exécuter le linting** :
   ```bash
   poetry run ruff check src/
   ```

5. **Formater le code** :
   ```bash
   poetry run black src/
   ```

6. **Commiter les changements** :
   ```bash
   git add .
   git commit -m "Ajout de la nouvelle fonctionnalité"
   ```

7. **Pousser la branche** :
   ```bash
   git push origin feature/nouvelle-fonctionnalite
   ```

8. **Ouvrir une Pull Request** :
   - Allez sur GitHub
   - Ouvrez une PR depuis votre branche
   - Décrivez vos changements
   - Attendez les revues

### 2. Corriger un Bug

1. **Créer une branche** :
   ```bash
   git checkout -b fix/description-du-bug
   ```

2. **Reproduire le bug** :
   - Ajouter un test qui reproduit le bug
   - Vérifier que le test échoue

3. **Corriger le bug** :
   - Modifier le code pour corriger le problème
   - Vérifier que le test passe

4. **Commiter et pousser** :
   ```bash
   git add .
   git commit -m "Correction du bug : description"
   git push origin fix/description-du-bug
   ```

5. **Ouvrir une Pull Request**

### 3. Mettre à Jour la Documentation

1. **Créer une branche** :
   ```bash
   git checkout -b docs/mise-a-jour-documentation
   ```

2. **Modifier la documentation** :
   - Mettre à jour les fichiers dans `docs/`
   - Mettre à jour le README.md si nécessaire

3. **Commiter et pousser** :
   ```bash
   git add .
   git commit -m "Mise à jour de la documentation"
   git push origin docs/mise-a-jour-documentation
   ```

4. **Ouvrir une Pull Request**

---

## 🧪 Tests

### Exécuter les Tests

#### Tous les tests

```bash
poetry run pytest
```

#### Tests avec couverture

```bash
poetry run pytest --cov=src --cov-report=html
```

#### Tests unitaires uniquement

```bash
poetry run pytest tests/unit/
```

#### Tests d'intégration uniquement

```bash
poetry run pytest tests/integration/
```

#### Test spécifique

```bash
poetry run pytest tests/unit/test_task.py::TestTaskModel::test_task_creation_with_defaults
```

### Écrire de Nouveaux Tests

#### Tests Unitaires

- Testez une seule unité de code (fonction, méthode, classe)
- Utilisez des mocks pour les dépendances externes
- Nommez les tests avec le préfixe `test_`

```python
# tests/unit/test_exemple.py
import pytest
from src.app.models.exemple import Exemple


class TestExemple:
    def test_creation(self):
        exemple = Exemple()
        assert exemple is not None
    
    def test_methode(self):
        exemple = Exemple()
        result = exemple.methode()
        assert result == "valeur attendue"
```

#### Tests d'Intégration

- Testez l'interaction entre plusieurs composants
- Utilisez pytest-qt pour les tests Qt

```python
# tests/integration/test_exemple.py
import pytest
from PySide6.QtWidgets import QApplication
from src.ui.windows.main_window import MainWindow


@pytest.fixture(scope="module")
def qapp():
    app = QApplication([])
    yield app
    app.quit()


def test_main_window_creation(qapp):
    window = MainWindow()
    assert window is not None
    window.close()
```

### Bonnes Pratiques pour les Tests

1. **Isolation** : Chaque test doit être indépendant
2. **Clarté** : Les tests doivent être faciles à comprendre
3. **Rapidité** : Les tests doivent s'exécuter rapidement
4. **Couverture** : Viser une couverture de 80%+
5. **Fixtures** : Utiliser des fixtures pour les ressources communes

---

## 📚 Documentation

### Mettre à Jour la Documentation

#### CHANGELOG.md

Mettez à jour le CHANGELOG pour chaque modification significative :

```markdown
## [Unreleased]

### Added
- Nouvelle fonctionnalité X

### Changed
- Modification de la fonctionnalité Y

### Fixed
- Correction du bug Z
```

#### Documentation Technique

- **ARCHITECTURE.md** : Mettez à jour si l'architecture change
- **DEVELOPMENT.md** : Mettez à jour ce guide si le workflow change
- **USER_GUIDE.md** : Mettez à jour pour les nouvelles fonctionnalités

#### Docstrings

- Toutes les classes, méthodes et fonctions publiques doivent avoir des docstrings
- Utilisez le format Google
- Incluez les types, paramètres et valeurs de retour

---

## 📦 Gestion des Dépendances

### Ajouter une Nouvelle Dépendance

#### Dépendance Principale

```bash
poetry add nom-de-la-dependance
```

#### Dépendance de Développement

```bash
poetry add --group dev nom-de-la-dependance
```

#### Spécifier une Version

```bash
poetry add "nom-de-la-dependance>=1.0.0,<2.0.0"
```

### Mettre à Jour les Dépendances

```bash
poetry update
```

### Verrouiller les Versions

```bash
poetry lock
```

### Exporter les Dépendances

Pour générer un fichier requirements.txt :

```bash
poetry export -f requirements.txt --output requirements.txt
```

---

## 🚀 Déploiement

### Construction de l'Application

#### Installer PyInstaller

```bash
poetry add --group dev pyinstaller
```

#### Construire pour Windows

```bash
poetry run pyinstaller --name TaskMaster --windowed --onefile --icon assets/icon.ico src/main.py
```

#### Construire pour macOS

```bash
poetry run pyinstaller --name TaskMaster --windowed --onefile --icon assets/icon.icns src/main.py
```

#### Construire pour Linux

```bash
poetry run pyinstaller --name TaskMaster --windowed --onefile src/main.py
```

### Pipeline CI/CD

Le projet utilise **GitHub Actions** pour l'intégration continue et le déploiement.

#### Workflow Principal

Le fichier `.github/workflows/ci-cd.yml` contient le pipeline CI/CD qui :

1. Exécute les tests sur chaque push et PR
2. Vérifie le linting
3. Construit l'application pour les différentes plateformes
4. *(À l'avenir : Déploie les artefacts)*

#### Personnalisation

Vous pouvez personnaliser le workflow en modifiant le fichier `ci-cd.yml`.

---

## 🤝 Contribution

### Processus de Contribution

1. **Fork** le projet
2. **Clone** votre fork
3. **Créez une branche** pour votre fonctionnalité/correction
4. **Commitez** vos changements
5. **Poussez** vers votre fork
6. **Ouvrez une Pull Request** vers le dépôt principal

### Règles de Contribution

1. **Respectez le style de code** : Utilisez Black et Ruff
2. **Ajoutez des tests** : Tous les nouveaux fonctionnalités doivent avoir des tests
3. **Documentez** : Mettez à jour la documentation si nécessaire
4. **Commits atomiques** : Chaque commit doit être une modification logique unique
5. **Messages de commit clairs** : Utilisez des messages descriptifs
6. **Passez les hooks pre-commit** : Exécutez `pre-commit run --all-files` avant de pousser

### Revues de Code

- Toutes les PR doivent être revues avant d'être fusionnées
- Attendez-vous à des commentaires et soyez prêt à faire des modifications
- Soyez respectueux et constructif dans vos commentaires

---

## 🛠 Outils de Développement

### Outils Intégrés

| Outil | Commande | Description |
|-------|----------|-------------|
| pytest | `poetry run pytest` | Exécuter les tests |
| ruff | `poetry run ruff check src/` | Linting du code |
| black | `poetry run black src/` | Formatage du code |
| mypy | `poetry run mypy src/` | Vérification des types |
| pre-commit | `poetry run pre-commit run` | Exécuter les hooks |

### Outils Externes

| Outil | Installation | Description |
|-------|-------------|-------------|
| Qt Designer | `poetry run pyside6-designer` | Conception d'interface |
| PyInstaller | `poetry add pyinstaller` | Construction d'exécutables |

---

## 📞 Support

### Problèmes Courants

#### Problème : PySide6 non trouvé

**Solution** :
```bash
poetry install
```

#### Problème : Erreurs de linting

**Solution** :
```bash
poetry run ruff check src/ --fix
poetry run black src/
```

#### Problème : Tests Qt échouent

**Solution** : Assurez-vous d'avoir une instance QApplication active.

### Où Demander de l'Aide

1. **Issues GitHub** : Ouvrez une issue pour les bugs ou questions
2. **Discussions GitHub** : Utilisez les discussions pour les questions générales
3. **Documentation** : Consultez les fichiers dans `docs/`

---

## 🎯 Bonnes Pratiques

### 1. Qualité du Code

- **Lisibilité** : Le code doit être facile à lire et à comprendre
- **Maintenabilité** : Le code doit être facile à modifier
- **Testabilité** : Le code doit être facile à tester
- **Documentation** : Le code doit être bien documenté

### 2. Performance

- **Évitez les opérations coûteuses** dans les méthodes appelées fréquemment
- **Utilisez le cache** pour les résultats des opérations coûteuses
- **Optimisez les E/S** : Minimisez les lectures/écritures de fichiers

### 3. Sécurité

- **Validation des entrées** : Validez toujours les données utilisateur
- **Gestion des erreurs** : Gérez les exceptions de manière appropriée
- **Protection des données** : Ne stockez pas de données sensibles en clair

---

## 📝 Checklist avant PR

- [ ] Le code suit les conventions de style (Black, Ruff)
- [ ] Tous les tests passent
- [ ] Les nouveaux fonctionnalités ont des tests
- [ ] La documentation est mise à jour
- [ ] Le CHANGELOG est mis à jour
- [ ] Les hooks pre-commit passent
- [ ] Les commits sont atomiques et ont des messages clairs
- [ ] La PR a une description claire

---

## 🎉 Conclusion

Merci de contribuer à **TaskMaster** ! En suivant ce guide, vous nous aidez à maintenir un code de haute qualité, bien testé et bien documenté.

N'hésitez pas à poser des questions ou à demander de l'aide si vous en avez besoin. Bonne contribution ! 🚀
