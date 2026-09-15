# TaskMaster - Gestionnaire de Tâches Desktop

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PySide6](https://img.shields.io/badge/PySide6-6.6.0-green.svg)](https://www.qt.io/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**TaskMaster** est une application desktop de gestion de tâches développée avec **PySide6 (Qt pour Python)**. Elle offre une interface moderne et intuitive pour organiser vos tâches quotidiennes.

## 📸 Captures d'écran

*(À ajouter après l'implémentation complète de l'UI)*

## ✨ Fonctionnalités

- ✅ **Gestion complète des tâches** : Création, modification, suppression
- ✅ **Priorisation** : Niveaux de priorité de 1 (très faible) à 5 (critique)
- ✅ **Catégorisation** : Ajout de tags pour organiser les tâches
- ✅ **Dates limites** : Définition et suivi des échéances
- ✅ **Statut de complétion** : Marquage des tâches comme terminées
- ✅ **Recherche** : Recherche rapide dans les titres et descriptions
- ✅ **Filtrage** : Filtres par statut (toutes, en cours, terminées, en retard)
- ✅ **Thème sombre** : Interface moderne et agréable pour les yeux
- ✅ **Persistance** : Sauvegarde automatique des tâches au format JSON
- ✅ **Multiplateforme** : Fonctionne sur Windows, macOS et Linux

## 🛠 Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)

## 🚀 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/alnews2/EvaluationDeMistralCODE.git
cd EvaluationDeMistralCODE
```

### 2. Installer les dépendances

#### Avec Poetry (recommandé)

```bash
# Installer Poetry si ce n'est pas déjà fait
pip install poetry

# Installer les dépendances
poetry install
```

#### Avec pip

```bash
pip install -r requirements.txt
```

*(Note: Un fichier `requirements.txt` peut être généré avec `poetry export -f requirements.txt --output requirements.txt`)*

### 3. Installer les pré-commit hooks (optionnel mais recommandé)

```bash
pre-commit install
```

## 🏃‍♂️ Exécution

### Avec Poetry

```bash
poetry run python src/main.py
```

### Avec Python directement

```bash
python src/main.py
```

## 📦 Construction de l'application standalone

Pour créer un exécutable autonome (pour Windows, macOS ou Linux) :

### 1. Installer PyInstaller

```bash
poetry add pyinstaller --group dev
```

### 2. Construire l'application

#### Sur Windows

```bash
poetry run pyinstaller --name TaskMaster --windowed --onefile --icon assets/icon.ico src/main.py
```

#### Sur macOS

```bash
poetry run pyinstaller --name TaskMaster --windowed --onefile --icon assets/icon.icns src/main.py
```

#### Sur Linux

```bash
poetry run pyinstaller --name TaskMaster --windowed --onefile src/main.py
```

L'exécutable sera généré dans le dossier `dist/`.

## 🧪 Tests

### Exécuter tous les tests

```bash
poetry run pytest
```

### Exécuter les tests avec couverture de code

```bash
poetry run pytest --cov=src --cov-report=html
```

### Exécuter uniquement les tests unitaires

```bash
poetry run pytest tests/unit/
```

### Exécuter uniquement les tests d'intégration

```bash
poetry run pytest tests/integration/
```

## 📁 Structure du projet

```
EvaluationDeMistralCODE/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Point d'entrée de l'application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── controllers/        # Contrôleurs (logique de médiation)
│   │   │   └── task_controller.py
│   │   ├── models/             # Modèles de données
│   │   │   └── task.py
│   │   └── services/           # Services (logique métier)
│   │       └── task_service.py
│   └── ui/
│       ├── __init__.py
│       ├── dialogs/            # Boîtes de dialogue
│       │   └── task_dialog.py
│       ├── resources/          # Ressources (fichiers .ui, images)
│       ├── windows/            # Fenêtres principales
│       │   └── main_window.py
│       └── widgets/            # Composants UI réutilisables
├── tests/
│   ├── __init__.py
│   ├── unit/                  # Tests unitaires
│   │   ├── test_task.py
│   │   └── test_task_service.py
│   └── integration/           # Tests d'intégration
│       └── test_main_window.py
├── docs/                      # Documentation
│   ├── ARCHITECTURE.md        # Documentation de l'architecture
│   ├── DEVELOPMENT.md         # Guide de développement
│   └── USER_GUIDE.md          # Guide utilisateur
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # Pipeline CI/CD
├── .gitignore
├── .pre-commit-config.yaml   # Configuration des hooks pre-commit
├── CHANGELOG.md              # Historique des changements
├── pyproject.toml            # Configuration du projet (Poetry)
└── README.md                  # Ce fichier
```

## 🏗 Architecture

L'application suit une **architecture MVC (Model-View-Controller)** adaptée pour Qt :

```
┌─────────────────────────────────────────────────────────────┐
│                        MAIN WINDOW                              │
│  (src/ui/windows/main_window.py)                              │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                      TASK CONTROLLER                            │
│  (src/app/controllers/task_controller.py)                     │
│  - Gère les signaux/slots Qt                                   │
│  - Coordonne les interactions entre UI et services            │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                       TASK SERVICE                               │
│  (src/app/services/task_service.py)                           │
│  - Logique métier                                             │
│  - Persistance (JSON)                                         │
│  - Opérations CRUD                                            │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                         TASK MODEL                               │
│  (src/app/models/task.py)                                     │
│  - Structure de données                                      │
│  - Validation                                                │
└─────────────────────────────────────────────────────────────┘
```

### Couche Modèle (`src/app/models/`)
- **Responsabilité** : Définition des structures de données et de la logique métier pure.
- **Technologies** : Python dataclasses, typing
- **Exemple** : `Task` avec ses propriétés et méthodes

### Couche Service (`src/app/services/`)
- **Responsabilité** : Logique métier, persistance, opérations CRUD
- **Technologies** : JSON pour la persistance
- **Exemple** : `TaskService` gère le stockage et la récupération des tâches

### Couche Contrôleur (`src/app/controllers/`)
- **Responsabilité** : Médiation entre UI et services, gestion des signaux/slots Qt
- **Technologies** : PySide6 Signaux/Slots
- **Exemple** : `TaskController` émet des signaux pour les mises à jour de l'UI

### Couche UI (`src/ui/`)
- **Responsabilité** : Affichage et interaction utilisateur
- **Technologies** : PySide6 (QMainWindow, QDialog, etc.)
- **Exemple** : `MainWindow`, `TaskDialog`

## 📜 Documentation

- **[Architecture](docs/ARCHITECTURE.md)** : Détails techniques sur l'architecture de l'application
- **[Guide de développement](docs/DEVELOPMENT.md)** : Comment contribuer au projet
- **[Guide utilisateur](docs/USER_GUIDE.md)** : Comment utiliser TaskMaster

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. **Fork** le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/ma-fonctionnalité`)
3. **Commit** vos changements (`git commit -m 'Ajout de ma fonctionnalité'`)
4. **Push** vers la branche (`git push origin feature/ma-fonctionnalité`)
5. Ouvrez une **Pull Request**

### Règles de contribution

- Respectez le style de code existant (Black, Ruff)
- Ajoutez des tests pour les nouvelles fonctionnalités
- Mettez à jour le CHANGELOG.md
- Documentez votre code avec des docstrings
- Utilisez les hooks pre-commit avant de commiter

## 📄 Licence

Ce projet est sous licence **MIT** - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- [Qt Project](https://www.qt.io/) - Pour le framework Qt
- [Python Software Foundation](https://www.python.org/) - Pour le langage Python
- [Mistral AI](https://mistral.ai/) - Pour le développement initial

## 📞 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une **Issue** ou une **Discussion** sur GitHub.
