# Projet GNS3

**Auteur**: Hanqi Lin

---

## Fichiers GNS3

J'ai préparé des configurations pour 14 routeurs dans GNS3 et vérifié leur fonctionnement.

- **Accéder aux fichiers GNS3** : [Lien vers les fichiers GNS3](https://drive.google.com/drive/folders/1c0d5WCeL22s39kzXoAEFWXHlqXY4ZM_c)

---

## Intent

- **Emplacement** : `json/intent_14r.json`

Ce fichier contient toutes les informations de base nécessaires à la connexion des routeurs, constituant ainsi la première étape de la génération automatique du code.

---

## Fichiers de Configuration

### Script de Configuration Automatique

- **Emplacement** : `config_14routers.py`
- **Output** : `output/configuration_14r.json`

Ce script, considéré comme une extension du fichier d'intention, contient toutes les informations de configuration requises pour chaque routeur. Il implémente également la configuration automatique des adresses IP pour chaque interface.

---

## Génération Automatique du Code Cisco

- **Emplacement** : `cisco_command.py`
- **Output** : `output/router_{n}.json`

Le script Python génère automatiquement les commands cisco de configuration pour les 14 routeurs et les stocke dans le dossier `output`.

---

## Utilisation de Telnetlib

- **Emplacement** : `test_telent.py`

J'ai expérimenté avec le module `telnetlib`, en l'utilisant pour saisir directement du code dans les routeurs. L'expérience a été un succès. Cependant, par manque de temps, je n'ai pas pu compléter l'automatisation complète de la configuration des routeurs.

---

## Comment Utiliser le Code

Pour exécuter le code, installez Python et quelques bibliothèques de base. Les fichiers d'intention et les fichiers de configuration initiaux pour les routeurs sont disponibles dans le dossier `json`.

### Fichiers préalables nécessaires à l'exécution de chaque programme

- **Fichier de Fonctions** : `func.py` (situé dans le répertoire personnel)
- **Fichier de Configuration** : `json/intent_14r.json`
- **Génération de Code Cisco** : `output/configuration_14r.json`

Il est recommandé de télécharger l'intégralité du projet, puis de l'exploiter et de le déboguer pour plus de commodité.


