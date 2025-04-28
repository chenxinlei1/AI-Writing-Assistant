# AI-Writing-Assistant


**Auteurs :** CHEN Siman & CHEN Xinlei

---

**AI Writing Assistant** est une application web basée sur FastAPI, permettant d'améliorer et de compléter des textes automatiquement. Le projet propose :

- **Interface web interactive :** Templates HTML modernes (Bootstrap), barre latérale pour l'historique, interactions fluides en JavaScript.
- **Correction intelligente :** Correction grammaticale, correction orthographique et complétion automatique des textes.
- **Gestion individuelle des utilisateurs :** Chaque utilisateur est identifié par un cookie unique pour un historique personnalisé.
- **Sauvegarde de l'historique :** Historique des textes traités stocké et consultable via l'interface (localStorage pour la session utilisateur).

---

## Prérequis

- **Docker**

Pour une installation manuelle :

- **Python 3.10** ou supérieur
- **Pip** pour installer les dépendances

- Packages Python :
  - FastAPI
  - Uvicorn
  - Jinja2
  - httpx
  - SymSpellPy
  - requests

---


##Installation avec Docker

```bash
docker build -t ai-writing-assistant .
```

##Installation manuelle

**1. Cloner le dépôt :**

```bash
git clone https://github.com/chenxinlei1/AI-Writing-Assistant.git
cd AI-Writing-Assistant
```

**2. Installer les dépendances Python :**

```bash
pip install fastapi uvicorn httpx symspellpy requests
```

---

## Lancement de l'application

Depuis la racine du projet, lancer :
```bash
uvicorn app:app --reload
```
Accéder ensuite à l'application via http://127.0.0.1:8000

---

## Fonctionnalités

**Correction grammaticale :** Détection et correction automatique des erreurs de grammaire en anglais.
**Correction orthographique :** Suggestions basées sur SymSpell pour les fautes de frappe.
**Complétion automatique :** Génération de la suite d'un texte via API de modèle de langage.
**Gestion de l'historique :**
L'utilisateur peut consulter toutes ses modifications précédentes via une barre latérale interactive.
Possibilité de recharger un ancien texte pour le modifier.
**Interface Responsive :**
Bootstrap 5 utilisé pour un rendu moderne et adaptatif.
Sidebar flottante et repliable (toggle).