# Guide Utilisateur - TaskMaster

## 📖 Table des Matières

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Premières Étapes](#premières-étapes)
4. [Interface Utilisateur](#interface-utilisateur)
5. [Gestion des Tâches](#gestion-des-tâches)
6. [Fonctionnalités Avancées](#fonctionnalités-avancées)
7. [Préférences](#préférences)
8. [Dépannage](#dépannage)
9. [FAQ](#faq)

---

## 🎯 Introduction

**TaskMaster** est une application desktop de gestion de tâches conçue pour vous aider à organiser votre travail et votre vie quotidienne. Avec TaskMaster, vous pouvez facilement créer, modifier, suivre et organiser vos tâches.

### Pourquoi TaskMaster ?

- **Simple et intuitif** : Interface facile à utiliser
- **Puissant** : Fonctionnalités avancées pour une gestion efficace
- **Personnalisable** : Adaptez l'application à vos besoins
- **Multiplateforme** : Fonctionne sur Windows, macOS et Linux
- **Hors ligne** : Vos données sont stockées localement

---

## 💾 Installation

### Prérequis

- **Système d'exploitation** : Windows 10+, macOS 10.15+, ou Linux (Ubuntu 20.04+, etc.)
- **Espace disque** : 50 Mo minimum
- **Mémoire** : 512 Mo minimum

### Installation Standard

1. **Télécharger l'application** :
   - Allez sur la page des [releases GitHub](https://github.com/alnews2/EvaluationDeMistralCODE/releases)
   - Téléchargez la version adaptée à votre système

2. **Installer** :
   - **Windows** : Double-cliquez sur le fichier `.exe` et suivez les instructions
   - **macOS** : Ouvrez le fichier `.dmg` et glissez TaskMaster dans Applications
   - **Linux** :
     - Rendez le fichier exécutable : `chmod +x TaskMaster`
     - Exécutez : `./TaskMaster`

### Installation depuis le Code Source

Si vous préférez construire l'application vous-même :

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/alnews2/EvaluationDeMistralCODE.git
   cd EvaluationDeMistralCODE
   ```

2. **Installer les dépendances** :
   ```bash
   pip install poetry
   poetry install
   ```

3. **Exécuter l'application** :
   ```bash
   poetry run python src/main.py
   ```

4. **Créer un exécutable** (optionnel) :
   ```bash
   poetry add pyinstaller
   poetry run pyinstaller --name TaskMaster --windowed --onefile src/main.py
   ```

---

## 🚀 Premières Étapes

### Premier Lancement

1. **Lancez TaskMaster** :
   - Double-cliquez sur l'icône de l'application
   - Ou exécutez la commande depuis le terminal

2. **Interface de bienvenue** :
   - La première fois que vous lancez TaskMaster, vous verrez une interface vide
   - Vous pouvez commencer à ajouter des tâches immédiatement

### Ajouter Votre Première Tâche

1. Cliquez sur le bouton **"Ajouter une tâche"** dans la barre d'outils
2. Ou utilisez le raccourci clavier **Ctrl+N** (Windows/Linux) ou **Cmd+N** (macOS)
3. Remplissez le formulaire :
   - **Titre** (obligatoire) : Donnez un nom à votre tâche
   - **Description** (optionnel) : Ajoutez des détails
   - **Priorité** : Sélectionnez un niveau de 1 (très faible) à 5 (critique)
   - **Date limite** : Définissez une échéance si nécessaire
   - **Tags** : Ajoutez des étiquettes pour catégoriser

4. Cliquez sur **OK** pour sauvegarder

---

## 🖥 Interface Utilisateur

### Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────────┐
│  TaskMaster                    [-] [□] [X]                        │
├─────────────────────────────────────────────────────────────────┤
│  Fichier  Édition  Affichage  Aide                              │
├─────────────────────────────────────────────────────────────────┤
│  [Ajouter une tâche] [Rechercher : __________] [Toutes] [En cours]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Mes tâches                                          3 tâche(s)  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                     │
│  [✓] +───────────────────────────────────────────────+ [Mod]    │
│      │ Acheter des courses                        │ [Sup]    │
│      │ Priorité: Élevée  Tags: maison, urgent     │          │
│      │ Échéance: 15/10/2024                      │          │
│  [ ] +───────────────────────────────────────────────+ [Mod]    │
│      │ Appeler le médecin                       │ [Sup]    │
│      │ Priorité: Moyenne  Tags: santé           │          │
│  [ ] +───────────────────────────────────────────────+ [Mod]    │
│      │ Préparer la réunion                      │ [Sup]    │
│      │ Priorité: Critique                       │          │
│                                                                     │
│  ─────────────────────────────────────────────────────────────  │
│                                                                     │
├─────────────────────────────────────────────────────────────────┤
│  Prêt                                                            │
└─────────────────────────────────────────────────────────────────┘
```

### Barre de Menu

- **Fichier** :
  - Nouvelle tâche (Ctrl+N)
  - Quitter (Ctrl+Q)

- **Édition** :
  - *(Fonctionnalités d'édition à venir)*

- **Affichage** :
  - *(Options d'affichage à venir)*

- **Aide** :
  - À propos : Affiche les informations sur l'application

### Barre d'Outils

- **Ajouter une tâche** : Ouvre le dialogue de création
- **Rechercher** : Filtre les tâches par mot-clé
- **Filtres** :
  - **Toutes** : Affiche toutes les tâches
  - **En cours** : Affiche les tâches non terminées
  - **Terminées** : Affiche les tâches complétées
  - **En retard** : Affiche les tâches dont la date limite est dépassée

### Zone Principale

- **Liste des tâches** : Affiche toutes les tâches filtrées
- **Compteur de tâches** : Affiche le nombre total de tâches

### Barre de Statut

- Affiche des messages d'information et d'erreur

---

## 📋 Gestion des Tâches

### Créer une Tâche

1. **Méthode 1** : Cliquez sur **"Ajouter une tâche"** dans la barre d'outils
2. **Méthode 2** : Utilisez le raccourci **Ctrl+N** (Windows/Linux) ou **Cmd+N** (macOS)
3. **Méthode 3** : Sélectionnez **Fichier → Nouvelle tâche** dans le menu

4. Remplissez le formulaire :
   - **Titre** (obligatoire) : Nom de la tâche
   - **Description** : Détails supplémentaires
   - **Priorité** : Niveau d'importance (1-5)
   - **Date limite** : Date butoir (optionnelle)
   - **Tags** : Étiquettes séparées par des virgules

5. Cliquez sur **OK** pour sauvegarder

### Modifier une Tâche

1. Cliquez sur le bouton **Modifier** de la tâche concernée
2. Modifiez les informations nécessaires
3. Cliquez sur **OK** pour sauvegarder les modifications

### Marquer une Tâche comme Terminée

1. Cochez la case à gauche de la tâche
2. La tâche sera automatiquement marquée comme terminée
3. Vous pouvez décocher la case pour la réactiver

### Supprimer une Tâche

1. Cliquez sur le bouton **Supprimer** de la tâche concernée
2. Confirmez la suppression dans la boîte de dialogue
3. La tâche sera définitivement supprimée

### Rechercher des Tâches

1. Utilisez le champ **Rechercher** dans la barre d'outils
2. Tapez un mot-clé (recherche dans le titre et la description)
3. Les résultats s'affichent instantanément

### Filtrer les Tâches

Utilisez les boutons de filtre dans la barre d'outils :

- **Toutes** : Affiche toutes les tâches
- **En cours** : Affiche uniquement les tâches non terminées
- **Terminées** : Affiche uniquement les tâches complétées
- **En retard** : Affiche les tâches non terminées dont la date limite est dépassée

---

## ⭐ Fonctionnalités Avancées

### Priorités

TaskMaster utilise un système de priorité à 5 niveaux :

| Niveau | Libellé | Couleur (à venir) |
|--------|---------|------------------|
| 1 | Très faible | Gris |
| 2 | Faible | Bleu clair |
| 3 | Moyenne | Bleu |
| 4 | Élevée | Orange |
| 5 | Critique | Rouge |

### Tags

- Utilisez des tags pour catégoriser vos tâches
- Séparez les tags par des virgules dans le champ Tags
- Exemples : `travail, urgent, maison, personnel`
- Vous pouvez filtrer par tag dans une future version

### Dates Limites

- Définissez une date limite pour vos tâches
- Les tâches avec une date limite apparaissent avec une indication visuelle
- Les tâches en retard (date limite dépassée et non terminées) sont mises en évidence

### Statistiques

L'onglet **Statistiques** (en développement) affichera :
- Nombre total de tâches
- Nombre de tâches terminées/non terminées
- Répartition par priorité
- Répartition par tag
- Tâches par période

---

## ⚙ Préférences

*(À venir dans une future version)*

Les préférences suivantes seront disponibles :

- **Thème** : Choisir entre thème clair et thème sombre
- **Langue** : Changer la langue de l'interface
- **Emplacement de stockage** : Définir où les données sont sauvegardées
- **Notifications** : Activer/désactiver les notifications
- **Rappels** : Configurer des rappels pour les tâches

---

## 🔧 Dépannage

### Problèmes Courants

#### L'application ne démarre pas

**Solutions** :
1. Vérifiez que votre système répond aux prérequis
2. Essayez de redémarrer votre ordinateur
3. Réinstallez l'application

#### Les tâches ne sont pas sauvegardées

**Solutions** :
1. Vérifiez que vous avez les permissions d'écriture dans le dossier de stockage
2. Le fichier de stockage par défaut est `~/.taskmaster/tasks.json`
3. Essayez de redémarrer l'application

#### L'interface semble corrompue

**Solutions** :
1. Essayez de redimensionner la fenêtre
2. Changez de thème (si disponible)
3. Réinstallez l'application

#### Problèmes de performance

**Solutions** :
1. Si vous avez beaucoup de tâches, essayez de filtrer pour réduire le nombre affiché
2. Vérifiez que votre système a suffisamment de mémoire
3. Fermez d'autres applications gourmandes

### Fichiers de Log

*(À venir dans une future version)*

Les fichiers de log seront disponibles dans :
- Windows : `%APPDATA%\TaskMaster\logs\`
- macOS : `~/Library/Application Support/TaskMaster/logs/`
- Linux : `~/.config/TaskMaster/logs/`

---

## ❓ FAQ

### Q: Comment puis-je sauvegarder mes données ?

**R** : Vos données sont automatiquement sauvegardées dans un fichier JSON local. Par défaut, le fichier se trouve dans `~/.taskmaster/tasks.json`. Vous pouvez copier ce fichier pour le sauvegarder.

### Q: Puis-je synchroniser mes tâches entre plusieurs appareils ?

**R** : Pour l'instant, TaskMaster est une application locale et ne propose pas de synchronisation cloud. Cependant, vous pouvez copier manuellement votre fichier de données entre appareils. Une fonctionnalité de synchronisation cloud est prévue pour une future version.

### Q: Comment puis-je importer des tâches depuis une autre application ?

**R** : Une fonctionnalité d'import/export (CSV, JSON) est prévue pour une future version. Pour l'instant, vous devez ajouter manuellement vos tâches.

### Q: Puis-je utiliser TaskMaster sur mon téléphone ?

**R** : TaskMaster est actuellement une application desktop. Une version mobile (Android/iOS) est envisagée pour le futur.

### Q: Comment puis-je contribuer au développement de TaskMaster ?

**R** : Consultez le [Guide de Développement](DEVELOPMENT.md) pour savoir comment contribuer au projet.

### Q: J'ai trouvé un bug. Que dois-je faire ?

**R** : Ouvrez une **Issue** sur [GitHub](https://github.com/alnews2/EvaluationDeMistralCODE/issues) avec une description détaillée du problème, les étapes pour le reproduire, et votre environnement (système d'exploitation, version de l'application, etc.).

### Q: Comment puis-je obtenir de l'aide ?

**R** : Vous pouvez :
1. Consulter ce guide utilisateur
2. Consulter la documentation technique dans le dossier `docs/`
3. Ouvrir une **Issue** sur GitHub pour les problèmes techniques
4. Ouvrir une **Discussion** sur GitHub pour les questions générales

---

## 📚 Ressources Supplémentaires

- [Site Web](https://github.com/alnews2/EvaluationDeMistralCODE) : Dépôt GitHub du projet
- [Documentation Technique](docs/ARCHITECTURE.md) : Détails sur l'architecture
- [Guide de Développement](docs/DEVELOPMENT.md) : Comment contribuer
- [Changelog](CHANGELOG.md) : Historique des versions

---

## 📝 Notes de Version

Consultez le fichier [CHANGELOG.md](CHANGELOG.md) pour voir les dernières améliorations et corrections.

---

## 🤝 Remerciements

Merci d'utiliser **TaskMaster** ! Nous espérons que cette application vous aidera à mieux organiser votre travail et votre vie quotidienne.

N'hésitez pas à partager vos retours, suggestions et idées pour améliorer TaskMaster.

---

## 📜 Licence

TaskMaster est distribué sous la licence **MIT**. Consultez le fichier [LICENSE](LICENSE) pour plus de détails.

---

*© 2024 Mistral AI. Tous droits réservés.*
