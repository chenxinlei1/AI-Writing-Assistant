# **Cahier des Charges – AI English Writing Assistant**  

## **1. Objectif**  

Développer une application d’assistance à l’écriture en anglais, accessible via une interface web, qui permettra aux utilisateurs :  

- De rédiger des textes en anglais avec une correction linguistique avancée  
- D’obtenir des suggestions contextuelles pour améliorer leur écriture  
- De bénéficier d’une complétion automatique pour accélérer la rédaction  

## **2. Besoins**  

- Développer une application web intégrant les fonctionnalités d’assistance à l’écriture
- Implémenter des outils de **correction grammaticale** et **orthographique** basés sur un modèle NLP avancé  
- Intégrer un **système de complétion automatique** intelligent pour suggérer des phrases ou reformulations  
- Mettre en place un système de **stockage et consultation des textes précédemment corrigés** (base de données ou stockage local)  
- Concevoir une interface ergonomique et responsive, adaptée aux mobiles et aux ordinateurs  

## **3. Public Cible**  

L’application vise plusieurs catégories d’utilisateurs :  

- **Étudiants et universitaires** : Pour améliorer leurs travaux académiques  
- **Professionnels** : Pour optimiser la rédaction d’e-mails et de rapports  
- **Apprenants en anglais (EFL/ESL)** : Pour perfectionner leur maîtrise de la langue écrite  
- **Rédacteurs et blogueurs** : Pour fluidifier et clarifier leurs écrits


## **4. Méthodes existantes**

Parmi les outils les plus utilisés aujourd’hui dans le domaine de l’assistance à l’écriture en anglais figurent Grammarly, DeepL Write et Quillbot.

**Grammarly** propose des corrections précises et des reformulations contextuelles, mais reste un outil propriétaire, limité à l’anglais, sans possibilité de personnalisation ni de déploiement local.


**DeepL Write** excelle dans la reformulation fluide et naturelle, mais ne prend en charge que l’anglais et l’allemand. Il n’est ni personnalisable ni auto-hébergeable.

**Quillbot** se concentre sur la paraphrase et la synthèse, avec un support limité aux utilisateurs anglophones. Il est également fermé et non personnalisable.


## **5. Fonctionnalités associées**

Un champ de texte permettra aux utilisateurs de saisir un texte en anglais à corriger ou à améliorer.

Trois boutons seront disponibles sous ce champ :

- **Correction grammaticale** : Détecte et corrige les erreurs grammaticales. (LanguageTool)
- **Correction orthographique** : Corrige les fautes d’orthographe. (SymSpell) 
- **Complétion automatique** : Propose des suggestions contextuelles pour compléter ou reformuler le texte. (GPT-2)

