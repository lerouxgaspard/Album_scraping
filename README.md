# 🎵 Best Ever Albums Scraper

Scraper Python permettant de récupérer automatiquement les albums les mieux classés par décennie depuis besteveralbums.com, puis d’exporter les données en JSON et CSV pour analyse.

## 📌 Objectif du projet

L’objectif est de constituer une base de données structurée des albums les mieux classés :

Décennies couvertes : 1960s à 2020s

100 pages par décennie

Environ 7000 albums

Export des données en JSON et CSV

Ce projet peut servir pour :

Analyse musicale

Data visualisation

Machine learning

Études culturelles

Projets data personnels

## 🛠️ Technologies utilisées

Python 3

requests

BeautifulSoup4

pandas

json

AppScript

## 📂 Structure du projet

├── main.py

├── data.json

├── data.csv

└── README.md

## ⚙️ Installation

Cloner le repository :

git clone https://github.com/votre-username/besteveralbums-scraper.git
cd besteveralbums-scraper


Installer les dépendances :

pip install requests beautifulsoup4 pandas

## 🚀 Utilisation
### 1️⃣ Scraping des données

Lancer le script principal :

main.py


Le script :

1 - Scrape les albums **par décennie**

2 - Affiche la progression **page par page**

3 - Sauvegarde les données en **JSON**

4 - Exemple de fichier généré : **data.json**

5 - Convertit le fichier **data.json** en **data.csv**



## 📊 Données récupérées

Pour chaque album :

Décennie,
Titre de l’album,
Artiste,
Année de sortie,
Rang global,
Pays,
Nombre d’apparitions dans les charts,
Rang dans l’année,
Rang dans la décennie.

## 🧠 Fonctionnement du scraper

### Le script :

Parcourt chaque décennie via un code spécifique

Scrape 100 pages par décennie

Parse le HTML avec BeautifulSoup

Extrait les métriques depuis les blocs chart-stats

Stocke les données dans une liste

Génère un fichier JSON structuré avec métadonnées

Des pauses (time.sleep) sont intégrées pour éviter de surcharger le serveur.

## ⚠️ Limites

Dépend fortement de la structure HTML du site

Peut casser si le site change

Scraping long (~20–30 minutes)

Aucune gestion avancée d’erreurs réseau

📈 Améliorations possibles

Ajouter un système de retry automatique

Scraping asynchrone

Sauvegarde progressive pour éviter perte de données

Ajout d’une base de données SQL

Dashboard de visualisation

## 📜 Disclaimer

Ce projet est réalisé à des fins éducatives et analytiques.
Respecter les conditions d’utilisation du site source.

## 👨‍💻 Auteur

Projet de @Codeurfort et @lerouxgaspard réalisé dans une logique d’apprentissage data / scraping / structuration de données culturelles.
