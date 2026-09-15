# Architecture Technique - TaskMaster

## 📋 Table des Matières

1. [Vue d'Ensemble](#vue-densemble)
2. [Architecture Globale](#architecture-globale)
3. [Couches Logicielles](#couches-logicielles)
4. [Flux de Données](#flux-de-données)
5. [Technologies Utilisées](#technologies-utilisées)
6. [Bonnes Pratiques](#bonnes-pratiques)
7. [Évolutivité](#évolutivité)

---

## 🏗 Vue d'Ensemble

**TaskMaster** est une application desktop de gestion de tâches développée avec **PySide6 (Qt pour Python)**. L'application suit une **architecture MVC (Model-View-Controller)** adaptée au framework Qt, avec une séparation claire des responsabilités entre les différentes couches.

### Objectifs de l'Architecture

- **Séparation des préoccupations** : Chaque couche a une responsabilité unique
- **Testabilité** : Facilité à tester chaque composant indépendamment
- **Maintenabilité** : Code clair, bien structuré et documenté
- **Évolutivité** : Conçue pour faciliter l'ajout de nouvelles fonctionnalités
- **Réutilisabilité** : Composants modulaire et réutilisables

---

## 🏛 Architecture Globale

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            APPLICATION LAYER                                │
│  (src/main.py)                                                              │
│  - Point d'entrée de l'application                                         │
│  - Initialisation de QApplication                                          │
│  - Configuration de l'injection de dépendances                             │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           PRESENTATION LAYER (UI)                          │
│  (src/ui/)                                                                  │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌───────────────────┐ │
│  │      WINDOWS         │  │       DIALOGS        │  │      WIDGETS       │ │
│  │  - MainWindow        │  │  - TaskDialog        │  │  - Réutilisables   │ │
│  │  - (Futures fenêtres) │  │  - (Autres dialogues) │  │  - Custom widgets   │ │
│  └─────────────────────┘  └─────────────────────┘  └───────────────────┘ │
│  ┌─────────────────────┐                                                    │
│  │      RESOURCES       │                                                    │
│  │  - Fichiers .ui      │  (Qt Designer)                                      │
│  │  - QSS (styles)      │                                                    │
│  │  - Images            │                                                    │
│  └─────────────────────┘                                                    │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼ (Signaux/Slots)
┌─────────────────────────────────────────────────────────────────────────┐
│                         CONTROLLER LAYER                                    │
│  (src/app/controllers/)                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │                      TaskController                                    │ │
│  │  - Gère les interactions entre UI et Services                        │ │
│  │  - Émet/réceptionne les signaux Qt                                    │ │
│  │  - Coordonne les opérations entre les couches                        │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          SERVICE LAYER                                       │
│  (src/app/services/)                                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │                      TaskService                                       │ │
│  │  - Logique métier                                                    │ │
│  │  - Opérations CRUD (Create, Read, Update, Delete)                     │ │
│  │  - Persistance des données                                           │ │
│  │  - Recherche et filtrage                                             │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           DATA LAYER (MODELS)                               │
│  (src/app/models/)                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │                      Task                                             │ │
│  │  - Structure de données (dataclass)                                  │ │
│  │  - Validation des données                                            │ │
│  │  - Méthodes utilitaires (sérialisation, etc.)                        │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         STORAGE LAYER                                      │
│  - JSON files (par défaut: ~/.taskmaster/tasks.json)                       │
│  - (Future: SQLite, PostgreSQL, etc.)                                     │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📦 Couches Logicielles

### 1. Presentation Layer (UI) - `src/ui/`

**Responsabilité** : Gestion de l'interface utilisateur et des interactions.

#### Composants

- **`windows/`** : Fenêtres principales de l'application
  - `main_window.py` : Fenêtre principale avec la liste des tâches
  
- **`dialogs/`** : Boîtes de dialogue modales
  - `task_dialog.py` : Dialogue pour créer/modifier des tâches
  
- **`widgets/`** : Composants UI réutilisables
  - *(À développer pour les composants personnalisés)*
  
- **`resources/`** : Fichiers de ressources
  - Fichiers `.ui` créés avec Qt Designer
  - Feuilles de style QSS
  - Images et icônes

#### Technologies

- **PySide6** : Bindings Python pour Qt6
- **Qt Designer** : Outil de conception d'interface graphique
- **QSS** : Feuilles de style CSS pour Qt

#### Bonnes Pratiques

1. **Séparation UI/Logique** : Les classes UI ne doivent contenir que du code lié à l'interface
2. **Signaux/Slots** : Utiliser le mécanisme Qt pour la communication entre composants
3. **Composants Réutilisables** : Créer des widgets personnalisés pour les éléments communs
4. **Thèmes** : Utiliser QSS pour un style cohérent dans toute l'application

---

### 2. Controller Layer - `src/app/controllers/`

**Responsabilité** : Médiation entre l'UI et les services, gestion de la logique de présentation.

#### Composants

- **`task_controller.py`** : Contrôleur pour la gestion des tâches
  - Reçoit les actions de l'utilisateur depuis l'UI
  - Appelle les méthodes appropriées du service
  - Émet des signaux pour mettre à jour l'UI
  - Gère les erreurs et les notifications

#### Fonctionnement

```python
# Exemple de flux dans le contrôleur
class TaskController(QObject):
    # Signaux pour notifier l'UI
    tasks_updated = Signal(list)
    error_occurred = Signal(str)
    
    def __init__(self, task_service: TaskService):
        self._task_service = task_service
    
    @Slot(str, str, int, str)
    def add_task(self, title: str, description: str, priority: int, tags: str):
        try:
            task = Task(title=title, description=description, priority=priority)
            created = self._task_service.add(task)
            self.tasks_updated.emit(self._task_service.get_all())
        except Exception as e:
            self.error_occurred.emit(str(e))
```

#### Bonnes Pratiques

1. **Injection de Dépendances** : Les services sont injectés dans le contrôleur
2. **Signaux/Slots** : Utiliser les signaux Qt pour notifier l'UI des changements
3. **Gestion des Erreurs** : Capturer les exceptions et notifier l'UI
4. **Logique Minimale** : Le contrôleur ne doit pas contenir de logique métier complexe

---

### 3. Service Layer - `src/app/services/`

**Responsabilité** : Logique métier, persistance et opérations sur les données.

#### Composants

- **`task_service.py`** : Service de gestion des tâches
  - Opérations CRUD (Create, Read, Update, Delete)
  - Persistance des données (JSON par défaut)
  - Recherche et filtrage
  - Gestion des erreurs

#### Fonctionnement

```python
class TaskService:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self._tasks = {}
        self._load_tasks()
    
    def add(self, task: Task) -> Task:
        self._tasks[task.id] = task
        self._save_tasks()
        return task
    
    def get_all(self) -> list[Task]:
        return list(self._tasks.values())
    
    def search(self, query: str) -> list[Task]:
        # Logique de recherche
        pass
```

#### Bonnes Pratiques

1. **Interface Claire** : Méthodes bien définies avec des contrats clairs
2. **Persistance Abstraite** : Le service ne sait pas comment les données sont stockées
3. **Gestion des Erreurs** : Lever des exceptions appropriées
4. **Performance** : Optimiser les opérations de lecture/écriture

---

### 4. Data Layer (Models) - `src/app/models/`

**Responsabilité** : Définition des structures de données et validation.

#### Composants

- **`task.py`** : Modèle de données pour une tâche
  - Utilisation de Python dataclasses
  - Validation des données
  - Méthodes utilitaires (sérialisation, etc.)

#### Fonctionnement

```python
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

@dataclass
class Task:
    id: UUID = field(default_factory=uuid4)
    title: str = ""
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    due_date: Optional[datetime] = None
    completed: bool = False
    priority: int = 3
    tags: list[str] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.title:
            raise ValueError("Task title cannot be empty")
    
    @property
    def is_overdue(self) -> bool:
        if self.due_date is None or self.completed:
            return False
        return self.due_date < datetime.now()
```

#### Bonnes Pratiques

1. **Immutabilité** : Les modèles doivent être immutables ou avoir des méthodes de modification claires
2. **Validation** : Valider les données dans `__post_init__`
3. **Sérialisation** : Implémenter des méthodes pour convertir vers/depuis des dictionnaires
4. **Typage** : Utiliser les type hints pour une meilleure maintenabilité

---

## 🔄 Flux de Données

### 1. Flux de Création de Tâche

```
Utilisateur
    │
    ▼ (Clic sur "Ajouter une tâche")
MainWindow._show_add_task_dialog()
    │
    ▼ (Affiche le dialogue)
TaskDialog
    │
    ▼ (Utilisateur remplit le formulaire)
TaskDialog._accept()
    │
    ▼ (Appel du contrôleur)
TaskController.add_task(title, description, priority, tags)
    │
    ▼ (Création du modèle)
TaskController → Task(title=title, description=description, ...)
    │
    ▼ (Appel du service)
TaskService.add(task)
    │
    ▼ (Persistance)
TaskService._save_tasks() → tasks.json
    │
    ▼ (Notification)
TaskController.tasks_updated.emit(tasks)
    │
    ▼ (Mise à jour UI)
MainWindow._on_tasks_updated(tasks)
    │
    ▼ (Affichage)
MainWindow._display_tasks(tasks)
```

### 2. Flux de Chargement Initial

```
Application Start
    │
    ▼
main.py → MainWindow(controller)
    │
    ▼
MainWindow.__init__()
    │
    ▼ (Appel initial)
MainWindow.controller.load_tasks()
    │
    ▼ (Appel du service)
TaskService.get_all()
    │
    ▼ (Chargement depuis le fichier)
TaskService._load_tasks() ← tasks.json
    │
    ▼ (Retour des données)
TaskController.tasks_updated.emit(tasks)
    │
    ▼ (Mise à jour UI)
MainWindow._on_tasks_updated(tasks)
```

### 3. Flux de Recherche

```
Utilisateur
    │
    ▼ (Saisie dans le champ de recherche)
MainWindow.search_input.textChanged
    │
    ▼
MainWindow._on_search_changed(text)
    │
    ▼ (Si texte non vide)
MainWindow.controller.search_tasks(text)
    │
    ▼ (Appel du service)
TaskService.search(query)
    │
    ▼ (Retour des résultats)
MainWindow._display_tasks(results)
```

---

## 🛠 Technologies Utilisées

### Langages et Frameworks

| Technologie | Version | Usage |
|-------------|---------|-------|
| Python | 3.10+ | Langage principal |
| PySide6 | 6.6.0+ | Bindings Qt pour Python |
| Qt6 | 6.6.0+ | Framework UI sous-jacent |

### Outils de Développement

| Outil | Usage |
|-------|-------|
| Poetry | Gestion des dépendances et packaging |
| pytest | Framework de test |
| pytest-qt | Plugin pytest pour les tests Qt |
| Ruff | Linting du code |
| Black | Formatage du code |
| mypy | Vérification des types (optionnel) |
| pre-commit | Hooks Git pour la qualité du code |

### Outils de Build et Déploiement

| Outil | Usage |
|-------|-------|
| PyInstaller | Création d'exécutables standalone |
| GitHub Actions | CI/CD |

---

## ✅ Bonnes Pratiques

### 1. Organisation du Code

- **Nommage** : Utiliser `snake_case` pour les fichiers et variables, `PascalCase` pour les classes
- **Structure** : Suivre la structure de dossiers définie
- **Imports** : Imports relatifs dans le package, imports absolus pour les dépendances externes

### 2. Gestion des Dépendances

- **Poetry** : Utiliser Poetry pour gérer les dépendances
- **Groupes** : Séparer les dépendances de développement (`dev-dependencies`) des dépendances principales
- **Versions** : Spécifier des versions minimales pour éviter les problèmes de compatibilité

### 3. Tests

- **Couverture** : Viser une couverture de code élevée (80%+)
- **Types de tests** :
  - Tests unitaires pour les modèles et services
  - Tests d'intégration pour les contrôleurs
  - Tests UI pour les fenêtres et dialogues (avec pytest-qt)
- **Isolation** : Utiliser des fixtures pour isoler les tests

### 4. Documentation

- **Docstrings** : Tous les modules, classes et méthodes publics doivent avoir des docstrings
- **Type Hints** : Utiliser les annotations de type pour toutes les fonctions et méthodes
- **Commentaires** : Éviter les commentaires évidents, privilégier le code auto-documenté

### 5. Gestion des Erreurs

- **Exceptions** : Lever des exceptions appropriées avec des messages clairs
- **Gestion** : Capturer les exceptions au niveau approprié (contrôleurs pour l'UI)
- **Notifications** : Notifier l'utilisateur des erreurs de manière claire et utile

### 6. Performance

- **Chargement paresseux** : Charger les données uniquement quand nécessaire
- **Cache** : Mettre en cache les résultats des opérations coûteuses
- **Batch** : Regrouper les opérations de persistance pour réduire les E/S

---

## 🚀 Évolutivité

### Ajout de Nouvelles Fonctionnalités

1. **Nouvelle Entité** (ex: Projets)
   - Créer un nouveau modèle dans `src/app/models/`
   - Créer un nouveau service dans `src/app/services/`
   - Créer un nouveau contrôleur dans `src/app/controllers/`
   - Ajouter l'UI dans `src/ui/`
   - Connecter les signaux/slots

2. **Nouvelle Fonctionnalité sur Entité Existante** (ex: Rappels pour les tâches)
   - Étendre le modèle `Task` avec les nouveaux champs
   - Mettre à jour le service pour gérer la nouvelle logique
   - Étendre le contrôleur avec les nouvelles actions
   - Mettre à jour l'UI pour afficher les nouvelles informations

3. **Nouveau Type de Stockage** (ex: Base de données SQLite)
   - Implémenter une nouvelle classe de service qui étend `TaskService`
   - Remplacer l'instance du service dans `main.py`
   - *(À l'avenir: utiliser un pattern Repository pour plus de flexibilité)*

### Exemples d'Extensions Futures

| Fonctionnalité | Complexité | Couches à Modifier |
|---------------|------------|---------------------|
| Catégories de tâches | Moyenne | Modèle, Service, UI |
| Rappels/Notifications | Élevée | Service, UI, Intégration système |
| Synchronisation cloud | Élevée | Service, Configuration |
| Collaboratif (multi-utilisateurs) | Très Élevée | Toutes, Architecture |
| Statistiques avancées | Moyenne | Service, UI |
| Import/Export (CSV, etc.) | Faible | Service, UI |

---

## 📊 Métriques de Qualité

### Complexité Cyclomatique
- **Objectif** : Maintenir une complexité cyclomatique ≤ 10 pour les méthodes
- **Outils** : Ruff peut détecter les méthodes trop complexes

### Couverture de Code
- **Objectif** : 80%+ de couverture
- **Outils** : pytest-cov pour mesurer la couverture

### Detter (Dette Technique)
- **Objectif** : Minimiser la dette technique
- **Pratiques** : Revues de code, refactoring régulier

---

## 🔧 Configuration et Environnement

### Variables d'Environnement

| Variable | Description | Valeur par défaut |
|----------|-------------|------------------|
| `TASKMASTER_STORAGE_PATH` | Chemin vers le fichier de stockage | `~/.taskmaster/tasks.json` |
| `TASKMASTER_LOG_LEVEL` | Niveau de journalisation | `INFO` |

### Configuration Qt

```python
# Dans main.py
app = QApplication(sys.argv)
app.setApplicationName("TaskMaster")
app.setOrganizationName("MistralAI")
app.setOrganizationDomain("mistral.ai")
```

---

## 🎯 Conclusion

L'architecture de **TaskMaster** a été conçue pour être :

- **Modulaire** : Chaque composant a une responsabilité unique
- **Testable** : Facilité à tester chaque couche indépendamment
- **Maintenable** : Code clair et bien documenté
- **Évolutive** : Conçue pour faciliter l'ajout de nouvelles fonctionnalités
- **Robuste** : Gestion appropriée des erreurs et validation des données

Cette architecture suit les **meilleures pratiques** de l'industrie et permet une **maintenance à long terme** du projet.
